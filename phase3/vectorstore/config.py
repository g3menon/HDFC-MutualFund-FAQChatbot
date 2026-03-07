"""
Phase 3 — Configuration

Model names, collection config, paths for vector store.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root .env if it exists
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv() # Fallback to standard search

# ─── Embedding Model ───────────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
EMBEDDING_DIMENSION = 3072

# ─── Pinecone ──────────────────────────────────────────────────────
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "hdfc-mutual-funds")

# ─── Paths ─────────────────────────────────────────────────────────
PROCESSED_CHUNKS_FILE = Path(__file__).resolve().parent.parent.parent / "phase2" / "data" / "processed" / "processed_chunks.json"

# ─── Retrieval Defaults ────────────────────────────────────────────
DEFAULT_TOP_K = 3
MAX_TOP_K = 10

# ─── Gemini Model (for reference by other phases) ─────────────────
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
