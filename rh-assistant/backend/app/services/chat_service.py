from datetime import datetime
from typing import Any

from app.ml.llm_engine import LLM_UNAVAILABLE, llm_engine
from app.services.document_index import search_documents
from app.core.config import settings
import re
import unicodedata


_STOP_WORDS = {
    "avec", "dans", "des", "les", "une", "pour", "que", "qui", "sur", "aux",
    "du", "de", "la", "le", "et", "est", "sont", "comment", "quelle", "quelles",
    "quel", "quels", "ein", "eine", "einer", "der", "die", "das", "und", "für",
    "mit", "von", "wie", "was", "sind", "où", "ou", "puis", "peux", "peut",
    "trouver", "find", "where", "company", "entreprise",
}

_TOPIC_ALIASES = {
    "reglement_interieur": (
        "reglement", "règlement", "interieur", "intérieur", "house rules",
        "betriebsordnung", "ordnung",
    ),
    "conges": (
        "conge", "congé", "conges", "congés", "vacances", "urlaub",
        "leave", "absence",
    ),
    "frais": (
        "frais", "remboursement", "depense", "dépense", "deplacement",
        "déplacement", "rembourse", "expense", "reimbursement",
    ),
    "formation": (
        "formation", "training", "kurs", "schulung", "apprentissage",
    ),
    "teletravail": (
        "teletravail", "télétravail", "travail", "distance", "remote",
        "hybride", "mobile arbeit",
    ),
    "paie": (
        "paie", "salaire", "remuneration", "rémunération", "bulletin",
        "paye", "gehalt", "lohn", "payroll",
    ),
}


def _terms(value: str) -> set[str]:
    normalized = _normalize(value)
    return {
        term[:8]
        for term in re.findall(r"[A-Za-z]{4,}", normalized)
        if term not in _STOP_WORDS
    }

def _normalize(value: str) -> str:
    # Some legacy Chroma entries contain replacement characters where an
    # accented letter was decoded incorrectly; map them before comparison.
    value = value.replace("\ufffd", "e")
    value = re.sub(r"(?<=[a-z])\?(?=[a-z])", "e", value.lower())
    normalized = unicodedata.normalize("NFKD", value.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _is_relevant(query: str, document: str, distance: float) -> bool:
    lexical_score = _lexical_score(query, document)
    topic_score = _topic_score(query, document)
    minimum_matches = 2 if len(_terms(query)) >= 2 else 1
    return lexical_score >= minimum_matches or (topic_score > 0 and lexical_score >= 1)


def _lexical_score(query: str, document: str) -> int:
    query_terms = _terms(query)
    document_terms = _terms(document)
    return sum(
        1 for query_term in query_terms
        if any(document_term.startswith(query_term[:4]) or query_term.startswith(document_term[:4])
               for document_term in document_terms)
    )


def _topic_score(query: str, document: str) -> int:
    normalized_query = _normalize(query)
    normalized_document = _normalize(document)
    score = 0
    for aliases in _TOPIC_ALIASES.values():
        query_has_topic = any(_normalize(alias) in normalized_query for alias in aliases)
        document_has_topic = any(_normalize(alias) in normalized_document for alias in aliases)
        if query_has_topic and document_has_topic:
            score += 1
    return score


def _topic_excerpt(query: str, document: str) -> str:
    """Return the section matching the question instead of the whole corpus."""
    normalized_query = _normalize(query)
    sections = [section.strip() for section in re.split(r"\n\s*\n", document) if section.strip()]
    matching_sections = []
    for section in sections:
        normalized_section = _normalize(section)
        score = sum(
            1
            for aliases in _TOPIC_ALIASES.values()
            for alias in aliases
            if _normalize(alias) in normalized_query and _normalize(alias) in normalized_section
        )
        if score:
            matching_sections.append((score, section))
    if matching_sections:
        return max(matching_sections, key=lambda item: item[0])[1]
    return document


def _confidence_score(query: str, documents: list[str], distances: list[float]) -> float:
    """Estimate answer reliability from retrieval evidence, not document count."""
    if not documents:
        return 0.0
    query_terms = _terms(query)
    best_document = documents[0]
    lexical_coverage = (
        _lexical_score(query, best_document) / max(len(query_terms), 1)
    )
    topic_signal = min(_topic_score(query, best_document) / 2, 1.0)
    distance = distances[0] if distances else settings.DOCUMENT_RELEVANCE_DISTANCE
    semantic_signal = max(
        0.0,
        1.0 - (float(distance) / max(settings.DOCUMENT_RELEVANCE_DISTANCE, 1.0)),
    )
    corroboration = min((len(documents) - 1) / 3, 1.0)
    score = (
        0.45 * min(lexical_coverage, 1.0)
        + 0.25 * topic_signal
        + 0.20 * semantic_signal
        + 0.10 * corroboration
    )
    return round(min(max(score, 0.0), 0.98), 2)


class ChatService:
    def __init__(self) -> None:
        self._memory_cache: dict[str, dict[str, Any]] = {}

    async def process_chat_query(self, db, chat_query) -> dict[str, Any]:
        started_at = datetime.now()
        # Bump the cache namespace when relevance rules change so an old
        # out-of-context answer cannot be reused.
        cache_key = f"relevance-v4:{chat_query.session_id}:{chat_query.message}"
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]

        # Search the complete demo corpus so a relevant FAQ is not hidden by
        # semantically similar but incorrect documents.
        search_results = search_documents(chat_query.message, n_results=20)
        candidates = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0]
        relevant_indexes = [
            index
            for index, distance in enumerate(distances)
            if _is_relevant(chat_query.message, candidates[index], distance)
        ]
        relevant_indexes.sort(
            key=lambda index: (
                _topic_score(chat_query.message, candidates[index]),
                _lexical_score(chat_query.message, candidates[index]),
                -distances[index],
            ),
            reverse=True,
        )
        documents = [candidates[index] for index in relevant_indexes]
        metadatas = [metadatas[index] for index in relevant_indexes]
        relevant_distances = [distances[index] for index in relevant_indexes]
        context_parts = []
        sources = []

        for index, document in enumerate(documents):
            metadata = metadatas[index] if index < len(metadatas) else {}
            source = metadata.get("filename") or metadata.get("source", "EUBIA HR document")
            context_parts.append(f"[{source}]\n{_topic_excerpt(chat_query.message, document)}")
            sources.append(source)

        context = "\n\n".join(context_parts)
        prompt = (
            f"Question: {chat_query.message}\n\n"
            f"Documents RH EUBIA disponibles:\n{context or 'Aucun document pertinent trouvé.'}\n\n"
            "Réponds de façon concise, opérationnelle et bilingue si nécessaire. "
            "Cite les noms des documents utilisés. Ne crée jamais une règle RH absente des documents."
        )
        if documents:
            response = await llm_engine.get_completion(prompt)
            if response.startswith(LLM_UNAVAILABLE):
                response = (
                    "Voici l'information trouvée dans la base documentaire EUBIA :\n\n"
                    f"{_topic_excerpt(chat_query.message, documents[0])}"
                )
        else:
            response = (
                "Je ne trouve pas encore de réponse fiable à cette question dans "
                "la base documentaire EUBIA. Votre demande a été transmise à "
                "l'administrateur RH pour validation."
            )
        elapsed = (datetime.now() - started_at).total_seconds()
        requires_validation = len(documents) == 0
        if requires_validation:
            from app.models import models

            db.add(
                models.HRQuestion(
                    question=chat_query.message,
                    proposed_response=response,
                    confidence_score=0.0,
                    status="pending",
                    asked_by=str(chat_query.user_id),
                )
            )
            db.commit()
        confidence_score = _confidence_score(
            chat_query.message,
            documents,
            relevant_distances,
        )
        result = {
            "response": response,
            "confidence_score": confidence_score,
            "sources": sources,
            "requires_validation": requires_validation,
            "validation_status": "pending" if requires_validation else "not_required",
            "response_time": elapsed,
            "timestamp": datetime.now(),
        }
        self._memory_cache[cache_key] = result
        return result


chat_service = ChatService()
