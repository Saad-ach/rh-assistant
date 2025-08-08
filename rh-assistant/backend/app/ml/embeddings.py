from sentence_transformers import SentenceTransformer

class EmbeddingsGenerator:
    def __init__(self, model_name: str = "paraphrase-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

embeddings_generator = EmbeddingsGenerator()
