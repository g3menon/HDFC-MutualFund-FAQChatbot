# 🏦 HDFC Mutual Fund RAG Chatbot

An intelligent **Retrieval-Augmented Generation (RAG)** chatbot that answers user queries about select HDFC Mutual Funds using real-time data from [IndMoney](https://www.indmoney.com/mutual-funds/amc/hdfc-mutual-fund).

## 🎯 Supported Funds

| Fund Name | Risk Level |
|-----------|------------|
| HDFC Banking & Financial Services Fund | Very High |
| HDFC Pharma and Healthcare Fund | Very High |
| HDFC Housing Opportunities Fund | Very High |
| HDFC Manufacturing Fund | Very High |
| HDFC Transportation and Logistics Fund | Very High |

## 💬 Sample Queries

- "What is the expense ratio of HDFC Pharma and Healthcare Fund?"
- "Is there an ELSS lock-in for HDFC Banking Fund?"
- "What is the minimum SIP amount?"
- "What is the exit load?"
- "What is the riskometer/benchmark?"
- "How to download capital-gains statement?"

## 🏗️ Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the complete phase-wise architecture.

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Data Collection (Web Scraping) | ✅ Complete |
| Phase 2 | Data Processing & Chunking | ✅ Complete |
| Phase 3 | Vector Store & Embedding | ✅ Complete |
| Phase 4 | RAG Pipeline & LLM Integration | ✅ Complete |
| Phase 5 | Chat UI (Frontend/FastAPI) | ✅ Complete |
| Phase 6 | Integration Testing & Guardrails | ✅ Complete |
| Phase 7 | Data Refresh Scheduler | ✅ Complete |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Chrome (for Playwright web scraping)
- Google Gemini API key
- Pinecone API key (Free Tier)

### Setup

```bash
# Clone the repository
git clone https://github.com/g3menon/GenAIBootcamp_Milestone1.git
cd GenAIBootcamp_Milestone1

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
playwright install

# Configure environment
# Edit .env with your GEMINI_API_KEY and PINECONE_API_KEY
```

### Run Server

This project is optimized for a **Free Forever** cloud deployment using Vercel, Google Gemini, and Pinecone Serverless.

```bash
# Launch the backend server
uvicorn phase5.backend.main:app --host 127.0.0.1 --port 8000
```
Navigate to `http://127.0.0.1:8000` to interact with the UI locally.

### Data Refresh

The system uses an orchestrated pipeline to scrape fresh data, generate Gemini embeddings, and sync them to Pinecone. In production (Vercel), this is triggered via Vercel Cron at 10:00 AM daily.

```bash
# Run the pipeline manually to populate Pinecone the first time
python -m phase3.run_vectorstore --rebuild
```

## 📄 License

This project is for educational purposes as part of the GenAI Bootcamp.
