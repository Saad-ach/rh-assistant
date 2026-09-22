import httpx

from app.core.config import settings


LLM_UNAVAILABLE = "Le service LLM EUBIA n'est pas encore configuré."

class LLMEngine:
    def __init__(self, model: str | None = None):
        self.model = model or settings.OLLAMA_MODEL

    async def get_completion(self, prompt: str, temperature: float = 0.7) -> str:
        provider = settings.LLM_PROVIDER.strip().lower()
        if provider == "ollama":
            return await self._get_ollama_completion(prompt, temperature)
        if provider == "azure_openai":
            return await self._get_azure_completion(prompt, temperature)
        return LLM_UNAVAILABLE

    async def _get_ollama_completion(self, prompt: str, temperature: float) -> str:
        if not settings.OLLAMA_BASE_URL or not self.model:
            return LLM_UNAVAILABLE

        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Tu es l'assistant RH officiel d'EUBIA. Réponds dans la langue "
                        "de la question. Utilise uniquement le contexte fourni. Si le "
                        "contexte ne contient pas la réponse, dis-le explicitement. "
                        "Ne crée jamais de règle RH."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "options": {"temperature": temperature},
        }
        try:
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT_SECONDS) as client:
                response = await client.post(
                    f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat",
                    json=payload,
                )
            response.raise_for_status()
            content = response.json().get("message", {}).get("content", "")
            return content.strip() or LLM_UNAVAILABLE
        except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError, ValueError):
            return LLM_UNAVAILABLE

    async def _get_azure_completion(self, prompt: str, temperature: float) -> str:
        if not settings.AZURE_OPENAI_ENDPOINT or not settings.AZURE_OPENAI_API_KEY:
            return LLM_UNAVAILABLE
        from openai import AsyncAzureOpenAI

        client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        )
        response = await client.chat.completions.create(
            model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es l'assistant RH officiel d'EUBIA. Réponds en allemand ou "
                        "français selon la question. Utilise uniquement le contexte fourni "
                        "et indique clairement quand une information manque."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return (response.choices[0].message.content or "").strip() or LLM_UNAVAILABLE

llm_engine = LLMEngine()
