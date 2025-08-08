import asyncio
from datetime import datetime
from typing import List, Optional

import openai
from sqlalchemy.orm import Session
import aioredis
import json

from app.core.config import settings
from app.ml.llm_engine import llm_engine
from app.ml.vectorizer import chroma_vectorizer
from app.models import schemas, models
from app.services import hr_service # type: ignore
from loguru import logger

class ChatService:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)

    async def get_cached_response(self, session_id: str, message: str) -> Optional[schemas.ChatResponse]:
        cache_key = f"chat:{session_id}:{message}"
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for session {session_id}, message {message}")
            return schemas.ChatResponse(**json.loads(cached_data))
        return None

    async def set_cached_response(self, session_id: str, message: str, response: schemas.ChatResponse):
        cache_key = f"chat:{session_id}:{message}"
        await self.redis.set(cache_key, response.model_dump_json(), ex=3600)  # Cache for 1 hour
        logger.info(f"Cache set for session {session_id}, message {message}")

    async def process_chat_query(
        self, db: Session, chat_query: schemas.ChatQuery
    ) -> schemas.ChatResponse:
        start_time = datetime.now()

        cached_response = await self.get_cached_response(chat_query.session_id, chat_query.message)
        if cached_response:
            return cached_response

        # 1. Semantic Search in HR Documents
        search_results = hr_service.search_hr_documents(chat_query.message)
        sources = [doc.metadata.get("source", "N/A") for doc in search_results.get("metadatas", [{}])[0]]
        context = "\n".join(search_results.get("documents", [""])[0])

        # 2. LLM Interaction
        prompt = f"""
        You are an intelligent HR assistant. Answer the following question based on the provided HR documents. 
        If the answer is not in the documents, state that you don't have enough information.

        HR Documents Context:
        {context}

        User Query: {chat_query.message}
        """
        
        llm_response_text = await llm_engine.get_completion(prompt)

        # 3. Confidence Score Calculation (Placeholder - needs advanced implementation)
        confidence_score = self._calculate_confidence_score(llm_response_text, context) # type: ignore

        # 4. Two-phase HR Validation (if confidence is low or specific query type)
        requires_validation = False
        validation_status = None

        if confidence_score < 0.7 or chat_query.query_type == "sensitive":  # Example threshold
            requires_validation = True
            validation_entry = schemas.HRValidationCreate(
                query=chat_query.message,
                proposed_response=llm_response_text,
                confidence_score=confidence_score,
                hr_feedback=None,
                approved=None,
            )
            hr_service.create_hr_validation(db, validation_entry)
            validation_status = "pending"
            llm_response_text = "Votre requête nécessite une validation par un expert RH. La réponse sera disponible après approbation."

        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()

        chat_response = schemas.ChatResponse(
            response=llm_response_text,
            confidence_score=confidence_score,
            sources=sources,
            requires_validation=requires_validation,
            validation_status=validation_status,
            response_time=response_time,
            timestamp=datetime.now(),
        )
        
        await self.set_cached_response(chat_query.session_id, chat_query.message, chat_response)
        return chat_response

    def _calculate_confidence_score(self, response: str, context: str) -> float:
        # This is a placeholder. A real implementation would involve:
        # - Analyzing semantic similarity between response and context
        # - Checking for direct quotes or factual consistency
        # - Using sentiment analysis or other NLP techniques
        # For now, a simple heuristic:
        if "Désolé, je n'ai pas pu générer de réponse" in response:
            return 0.1
        if len(context) > 50 and len(response) > 50:  # Basic check if context was substantial
            return 0.85
        return 0.5

chat_service = ChatService()
