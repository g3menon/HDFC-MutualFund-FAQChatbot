"""
Phase 3 — Embedder

Generates vector embeddings for text chunks using Google Gemini.
Uses text-embedding-004 (768-dimension).
"""

import logging
from google import genai
from phase3.vectorstore.config import EMBEDDING_MODEL, GEMINI_API_KEY, EMBEDDING_DIMENSION

logger = logging.getLogger("phase3")


class Embedder:
    """Generates embeddings using a Gemini model."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self.api_key = GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        self.client = genai.Client(api_key=self.api_key)

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text string."""
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=text
        )
        return response.embeddings[0].values

    def embed_texts(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.models.embed_content(
                model=self.model_name,
                contents=batch
            )
            for e in response.embeddings:
                embeddings.append(e.values)
        return embeddings

    def get_dimension(self) -> int:
        """Return embedding dimension."""
        return EMBEDDING_DIMENSION
