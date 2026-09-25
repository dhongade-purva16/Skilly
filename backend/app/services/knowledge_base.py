from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models import KnowledgeResource, KnowledgeChunk
from app.services.embedding_service import embedding_service

def chunk_text(text: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Deterministic chunking by length with overlap."""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chunk_size
        chunks.append(text[start:end])
        start += max_chunk_size - overlap
    return chunks

def ingest_resource(
    db: Session,
    title: str,
    content: str, # Full text content to be chunked
    resource_type: str,
    provider: str,
    source_url: str,
    skill_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    estimated_duration: Optional[str] = None,
    trust_status: str = "pending",
    metadata: Optional[Dict[str, Any]] = None
) -> KnowledgeResource:
    
    # Check if resource already exists by source_url
    resource = db.query(KnowledgeResource).filter(KnowledgeResource.source_url == source_url).first()
    if not resource:
        resource = KnowledgeResource(
            title=title,
            description=content[:200] + "..." if len(content) > 200 else content,
            resource_type=resource_type,
            provider=provider,
            source_url=source_url,
            skill_id=skill_id,
            difficulty=difficulty,
            estimated_duration=estimated_duration,
            trust_status=trust_status,
            metadata_json=metadata
        )
        db.add(resource)
        db.commit()
        db.refresh(resource)
    else:
        # Update existing
        resource.title = title
        resource.resource_type = resource_type
        resource.provider = provider
        resource.skill_id = skill_id
        resource.difficulty = difficulty
        resource.estimated_duration = estimated_duration
        resource.trust_status = trust_status
        resource.metadata_json = metadata
        db.commit()
        
        # Delete old chunks
        db.query(KnowledgeChunk).filter(KnowledgeChunk.knowledge_resource_id == resource.id).delete()
        db.commit()

    # Create chunks
    chunks_text = chunk_text(content)
    
    for i, c_text in enumerate(chunks_text):
        embedding = embedding_service.embed_text(c_text)
        chunk = KnowledgeChunk(
            knowledge_resource_id=resource.id,
            chunk_index=i,
            content=c_text,
            embedding=embedding,
            metadata_json={"source": provider, "resource_type": resource_type}
        )
        db.add(chunk)
    
    db.commit()
    return resource
