"""
Phase 3 — Tests for Embedder, Store, and Retriever

Covers T3.1–T3.10 from the architecture test cases.
"""

import sys
import json
import logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest

# Suppress noisy logs during tests
logging.basicConfig(level=logging.WARNING)


# ─── Embedder Tests ─────────────────────────────────────────────────
class TestEmbedder:
    """Test embedding generation."""

    @pytest.fixture(scope="class")
    def embedder(self):
        from phase3.vectorstore.embedder import Embedder
        return Embedder()

    def test_embed_single_text(self, embedder):
        """Embedding a single text produces a list of floats."""
        vec = embedder.embed_text("What is the expense ratio?")
        assert isinstance(vec, list)
        assert len(vec) == 3072
        assert all(isinstance(v, float) for v in vec)

    def test_embed_dimension(self, embedder):
        """Embedding dimension matches expected (3072 for Gemini)."""
        dim = embedder.get_dimension()
        assert dim == 3072

    def test_embed_batch(self, embedder):
        """Batch embedding produces correct number of vectors."""
        texts = ["text one", "text two", "text three"]
        vecs = embedder.embed_texts(texts)
        assert len(vecs) == 3
        assert all(len(v) == 3072 for v in vecs)


# ─── Store Tests ─────────────────────────────────────────────────────
class TestStore:
    """Test Pinecone store operations."""

    @pytest.fixture(scope="class")
    def store(self):
        """Create a temporary store for testing."""
        from phase3.vectorstore.store import VectorStore
        return VectorStore(index_name="test-index-tmp")

    @pytest.fixture
    def sample_chunks(self):
        return [
            {
                "chunk_id": "test_fund_overview",
                "fund_id": "test_fund",
                "fund_name": "Test Fund",
                "source_url": "https://example.com",
                "chunk_type": "overview",
                "metadata_tags": ["fund_name", "category"],
                "content": "Test Fund is an equity mutual fund.",
                "last_updated": "2026-01-01T00:00:00"
            }
        ]

    def test_pinecone_index_ready(self, store):
        """T3.2: Pinecone index ready."""
        assert store.index is not None
        assert store.index_name == "test-index-tmp"

    def test_build_index(self, store, sample_chunks):
        """Building index adds vectors."""
        count = store.build_index(chunks=sample_chunks, force_rebuild=True)
        assert count == 1
        # Cleanup
        store.delete_collection()

