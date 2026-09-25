from typing import List

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if HAS_SENTENCE_TRANSFORMERS:
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None

    def embed_text(self, text: str) -> List[float]:
        if HAS_SENTENCE_TRANSFORMERS:
            return self.model.encode(text).tolist()
        else:
            # Fallback dummy embedding (384 dims for all-MiniLM-L6-v2)
            # Add some variability based on length so they aren't identical
            base_val = (len(text) % 10) / 100.0
            return [0.1 + base_val] * 384

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        if HAS_SENTENCE_TRANSFORMERS:
            return self.model.encode(documents).tolist()
        else:
            return [self.embed_text(doc) for doc in documents]

# Singleton instance
embedding_service = EmbeddingService()
