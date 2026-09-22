from typing import Any

from app.core.config import settings
from app.ml.vectorizer import chroma_vectorizer


async def create_embedding(text: str) -> list[float] | None:
    if not settings.AZURE_OPENAI_ENDPOINT or not settings.AZURE_OPENAI_API_KEY:
        return None

    from openai import AsyncAzureOpenAI

    client = AsyncAzureOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    )
    response = await client.embeddings.create(
        model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
    )
    return response.data[0].embedding


async def index_document(document_id: str, text: str, metadata: dict[str, Any]) -> None:
    embedding = await create_embedding(text)
    if embedding:
        chroma_vectorizer.add_document_with_embedding(document_id, text, metadata, embedding)
    else:
        chroma_vectorizer.add_document(document_id, text, metadata)


def search_documents(query: str, n_results: int = 5) -> dict[str, Any]:
    return chroma_vectorizer.search_documents(query, n_results)


async def index_answer(document_id: str, question: str, answer: str, metadata: dict[str, Any]) -> None:
    text = f"Question RH: {question}\nRéponse validée: {answer}"
    await index_document(document_id, text, metadata)
