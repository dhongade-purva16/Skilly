from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.models import KnowledgeResource, KnowledgeChunk
from app.services.embedding_service import embedding_service
from app.schemas.knowledge import KnowledgeResourceResponse

def retrieve_resources_for_skill(
    db: Session,
    query: str,
    skill_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    top_k: int = 3
) -> List[KnowledgeResourceResponse]:
    
    # 1. Embed query
    query_embedding = embedding_service.embed_text(query)

    # 2. Vector search query using pgvector operator <->
    # We only want approved resources
    
    # Because vector queries are sensitive, we'll construct the filter parts
    filter_clause = "kr.trust_status = 'approved'"
    params = {"query_embedding": str(query_embedding)}
    
    if skill_id is not None:
        filter_clause += " AND (kr.skill_id = :skill_id OR kr.skill_id IS NULL)"
        params["skill_id"] = skill_id
        
    if difficulty:
        filter_clause += " AND kr.difficulty = :difficulty"
        params["difficulty"] = difficulty

    sql = text(f"""
        SELECT 
            kr.id as resource_id,
            kr.title,
            kr.resource_type,
            kr.provider,
            kr.difficulty,
            kr.source_url,
            kr.estimated_duration,
            1 - (kc.embedding <=> CAST(:query_embedding AS vector)) as similarity_score
        FROM knowledge_chunks kc
        JOIN knowledge_resources kr ON kr.id = kc.knowledge_resource_id
        WHERE {filter_clause}
        ORDER BY kc.embedding <=> CAST(:query_embedding AS vector)
        LIMIT :top_k
    """)
    params["top_k"] = top_k

    results = db.execute(sql, params).fetchall()

    # Post-process to group by resource_id (since multiple chunks might match, we just take the best one)
    seen_resources = set()
    unique_results = []
    
    for row in results:
        if row.resource_id not in seen_resources:
            seen_resources.add(row.resource_id)
            unique_results.append(KnowledgeResourceResponse(
                resource_id=row.resource_id,
                title=row.title,
                resource_type=row.resource_type,
                provider=row.provider,
                difficulty=row.difficulty,
                source_url=row.source_url,
                estimated_duration=row.estimated_duration,
                similarity_score=float(row.similarity_score)
            ))
            
    return unique_results
