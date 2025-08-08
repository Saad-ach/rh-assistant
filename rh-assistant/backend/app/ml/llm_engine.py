import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

class LLMEngine:
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    async def get_completion(self, prompt: str, temperature: float = 0.7) -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Log the error and potentially re-raise or return a default message
            print(f"Error getting completion from OpenAI: {e}")
            return "Désolé, je n'ai pas pu générer de réponse pour le moment."

llm_engine = LLMEngine()
