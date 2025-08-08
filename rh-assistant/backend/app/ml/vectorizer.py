import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings
from app.ml.embeddings import embeddings_generator

class ChromaVectorizer:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name="hr_documents",
            embedding_function=self.embedding_function
        )

    def add_document(self, doc_id: str, document: str, metadata: dict):
        self.collection.upsert(
            documents=[document],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def search_documents(self, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

chroma_vectorizer = ChromaVectorizer()
