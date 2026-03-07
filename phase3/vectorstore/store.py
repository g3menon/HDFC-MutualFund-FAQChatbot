"""
Phase 3 — Pinecone Store

Handles creating, populating, and querying the Pinecone collection.
"""

import json
import logging
import time
from pathlib import Path
from typing import Optional

from pinecone import Pinecone, ServerlessSpec

from phase3.vectorstore.config import (
    PINECONE_API_KEY, PINECONE_INDEX_NAME, PROCESSED_CHUNKS_FILE, EMBEDDING_DIMENSION
)
from phase3.vectorstore.embedder import Embedder

logger = logging.getLogger("phase3")


class VectorStore:
    """Manages Pinecone index for HDFC Mutual Fund chunks."""

    def __init__(self, index_name: str = PINECONE_INDEX_NAME):
        self.index_name = index_name
        self._pc = None
        self._index = None
        self._embedder = None

    @property
    def pc(self):
        """Lazy-init Pinecone client."""
        if self._pc is None:
            if not PINECONE_API_KEY:
                raise ValueError("PINECONE_API_KEY is missing from environment variables.")
            self._pc = Pinecone(api_key=PINECONE_API_KEY)
            logger.info("Pinecone client initialized")
        return self._pc

    @property
    def index(self):
        """Get or create the collection."""
        if self._index is None:
            if self.index_name not in self.pc.list_indexes().names():
                logger.info(f"Creating Pinecone index '{self.index_name}'...")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=EMBEDDING_DIMENSION,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                while not self.pc.describe_index(self.index_name).status['ready']:
                    time.sleep(1)
            self._index = self.pc.Index(self.index_name)
            logger.info(f"Pinecone index '{self.index_name}' ready")
        return self._index

    @property
    def embedder(self) -> Embedder:
        """Lazy-init embedder."""
        if self._embedder is None:
            self._embedder = Embedder()
        return self._embedder

    def load_chunks(self, chunks_file: str | Path = PROCESSED_CHUNKS_FILE) -> list[dict]:
        """Load processed chunks from Phase 2 output."""
        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        logger.info(f"Loaded {len(chunks)} chunks from {chunks_file}")
        return chunks

    def build_index(self, chunks: Optional[list[dict]] = None, force_rebuild: bool = False):
        if chunks is None:
            chunks = self.load_chunks()

        if force_rebuild:
            try:
                self.pc.delete_index(self.index_name)
                self._index = None
                logger.info(f"Deleted existing Pinecone index '{self.index_name}'")
                
                # Wait before recreating
                time.sleep(5)
            except Exception:
                pass

        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        documents = [c["content"] for c in chunks]
        embeddings = self.embedder.embed_texts(documents)

        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = chunk["chunk_id"]
            metadata = {
                "fund_id": chunk.get("fund_id", ""),
                "fund_name": chunk.get("fund_name", ""),
                "chunk_type": chunk.get("chunk_type", ""),
                "content": chunk.get("content", ""),
                "source_url": chunk.get("source_url", ""),
                "last_updated": chunk.get("last_updated", ""),
            }
            tags = chunk.get("metadata_tags", [])
            if tags:
                metadata["metadata_tags"] = ",".join(tags)

            vectors.append((chunk_id, embedding, metadata))

        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)

        logger.info(f"✅ Indexed {len(vectors)} vectors in '{self.index_name}'")
        return len(vectors)

    def get_collection_count(self) -> int:
        return self.index.describe_index_stats().total_vector_count

    def collection_exists(self) -> bool:
        try:
            return self.index_name in self.pc.list_indexes().names()
        except Exception:
            return False

    def delete_collection(self):
        try:
            self.pc.delete_index(self.index_name)
            self._index = None
            logger.info(f"Collection '{self.index_name}' deleted")
        except Exception as e:
            logger.warning(f"Could not delete collection: {e}")
