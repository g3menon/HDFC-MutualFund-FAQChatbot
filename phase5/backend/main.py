import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Ensure the root directory is in the Python path
# On Vercel, the root is usually /var/task
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from phase4.rag.pipeline import RAGPipeline
from phase4.rag.config import SUPPORTED_FUNDS

from phase7.scheduler.status_tracker import read_status
# Removed start_scheduler import to avoid heavy transitive imports (playwright) on startup

app = FastAPI(title="HDFC Mutual Fund API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        try:
            # Load environment variables explicitly for Vercel if .env exists
            # (Vercel usually provides them via os.environ, so this is for local/other envs)
            from dotenv import load_dotenv
            load_dotenv()
            
            pipeline = RAGPipeline()
            print("RAG Pipeline initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize RAG pipeline: {e}")
            raise HTTPException(status_code=500, detail=f"Pipeline initialization failed: {str(e)}")
    return pipeline

# Removed @app.on_event("startup") to prevent cold-start timeouts on Vercel

@app.get("/")
def read_root():
    return {"message": "HDFC Mutual Fund RAG API is live. Use /api/chat for queries."}

from typing import Optional, List

class ChatRequest(BaseModel):
    query: str
    fund_filter: Optional[str] = None
    user_id: Optional[str] = None
    chat_history: List[dict] = []

@app.post("/api/chat")
def chat(request: ChatRequest):
    p = get_pipeline()
    try:
        response = p.generate_response(request.query, request.chat_history)
        return {
            "response": response,
            "sources": [],
            "timestamp": "2026-03-03T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health():
    status = read_status()
    last_refresh = status.get("last_run", "2026-03-03T00:00:00Z")
    return {"status": "ok", "last_data_refresh": last_refresh, "scheduler": status}

@app.get("/api/funds")
def funds():
    return [{"fund_name": f} for f in SUPPORTED_FUNDS]

@app.get("/api/suggestions")
def suggestions():
    return [
        "What is the expense ratio of HDFC Manufacturing Fund?",
        "What is the exit load for HDFC Pharma and Healthcare Fund?",
        "What is the minimum SIP amount for HDFC Banking & Financial Services Fund?",
        "How to download capital gains statement?"
    ]

# Serve static files for the frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

