from typing import List
from app.schemas.knowledge import KnowledgeResourceResponse

class KnowledgeReranker:
    """
    Abstraction for future complex reranking (e.g. CrossEncoder, BGE reranker).
    Currently implemented as a simple vector similarity sort.
    """
    def rerank(self, query: str, resources: List[KnowledgeResourceResponse]) -> List[KnowledgeResourceResponse]:
        # Currently, the resources are already sorted by vector similarity from pgvector.
        # So we just return them. In the future, this can re-score them.
        return sorted(resources, key=lambda r: r.similarity_score, reverse=True)

knowledge_reranker = KnowledgeReranker()
