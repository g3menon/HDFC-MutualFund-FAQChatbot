"""
Phase 3 — Retriever

Query interface for retrieving relevant chunks from the Pinecone vector store.
"""

import logging
from typing import Optional

from phase3.vectorstore.store import VectorStore
from phase3.vectorstore.embedder import Embedder
from phase3.vectorstore.config import DEFAULT_TOP_K, MAX_TOP_K

logger = logging.getLogger("phase3")


class Retriever:
    """Retrieves relevant chunks from Pinecone."""

    def __init__(self, store: Optional[VectorStore] = None):
        self.store = store or VectorStore()
        self._embedder = None

    @property
    def embedder(self) -> Embedder:
        """Lazy-init the embedder."""
        if self._embedder is None:
            self._embedder = Embedder()
        return self._embedder

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        fund_filter: Optional[str] = None,
        chunk_type_filter: Optional[str] = None,
    ) -> list[dict]:
        if not query or not query.strip():
            logger.warning("Empty query received")
            return []

        top_k = max(1, min(top_k, MAX_TOP_K))
        filter_dict = self._build_filter(fund_filter, chunk_type_filter)

        query_embedding = self.embedder.embed_text(query)

        try:
            results = self.store.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict if filter_dict else None
            )
        except Exception as e:
            logger.error(f"Pinecone query failed: {e}")
            return []

        return self._parse_results(results)

    def _build_filter(
        self,
        fund_filter: Optional[str],
        chunk_type_filter: Optional[str],
    ) -> Optional[dict]:
        conditions = {}
        if fund_filter:
            conditions["fund_id"] = {"$eq": fund_filter}
        if chunk_type_filter:
            conditions["chunk_type"] = {"$eq": chunk_type_filter}
        
        return conditions if conditions else None

    def _parse_results(self, raw_results) -> list[dict]:
        parsed = []
        if not raw_results or not raw_results.matches:
            return parsed

        for match in raw_results.matches:
            metadata = match.metadata or {}
            score = match.score

            parsed.append({
                "chunk_id": match.id,
                "content": metadata.get("content", ""),
                "fund_id": metadata.get("fund_id", ""),
                "fund_name": metadata.get("fund_name", ""),
                "source_url": metadata.get("source_url", ""),
                "chunk_type": metadata.get("chunk_type", ""),
                "metadata_tags": metadata.get("metadata_tags", ""),
                "last_updated": metadata.get("last_updated", ""),
                "distance": 1 - score, # Approximate distance representation
                "similarity_score": round(score, 4),
            })

        return parsed

    def get_store_stats(self) -> dict:
        return {
            "collection_name": self.store.index_name,
            "vector_count": self.store.get_collection_count(),
            "embedding_model": self.embedder.model_name,
            "embedding_dimension": self.embedder.get_dimension(),
        }
