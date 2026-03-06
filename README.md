# ResearchPilot 🔬
**Agentic AI-Powered Research Intelligence Engine**

ResearchPilot is a full-stack AI system that retrieves academic papers from arXiv, Semantic Scholar, and PubMed, then runs a 9-agent reasoning pipeline to produce structured, evidence-based research insights.

---

## Quick Start

### 1. Backend

```bash
cd backend

# Copy and fill in your environment variables
copy .env.example .env

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for Swagger UI.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

---

## Environment Variables (`.env`)

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq Llama-3.3-70B (recommended, free tier available) |
| `OPENAI_API_KEY` | Optional | OpenAI GPT-4o-mini fallback |
| `OPENROUTER_API_KEY` | Optional | OpenRouter multi-model access |
| `GOOGLE_API_KEY` | Optional | Gemini 1.5 Flash |
| `SUPABASE_URL` | Optional | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Optional | Supabase service role key |
| `LLM_PROVIDER` | Optional | `groq` \| `openai` \| `openrouter` \| `gemini` (default: `groq`) |
| `EMBEDDING_PROVIDER` | Optional | `huggingface` \| `openai` (default: `huggingface`) |

> **Note**: If no LLM key is configured, the system auto-enables **Demo Mode** (returns placeholder responses).

---

## Supabase Setup (Optional but Recommended)

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. In the **SQL Editor**, run:
   ```sql
   -- Copy contents of: backend/db/migrations/001_initial.sql
   ```
3. Set `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` in your `.env`

> Without Supabase, the system uses an in-memory vector store for the session.

---

## Architecture

```
User Query
    │
    ▼
Orchestrator (FastAPI SSE stream)
    │
    ├─► Query Refiner Agent      → Precise academic question
    ├─► Planner Agent            → Research strategy
    ├─► RAG Retrieval            → arXiv + Semantic Scholar + PubMed
    ├─► Pro Agent                → Supporting arguments
    ├─► Con Agent                → Counterarguments
    ├─► Evidence Analyzer        → Evidence strength score
    ├─► Contradiction Detector   → Conflicting findings
    ├─► Critic Agent             → Argument quality review
    ├─► Gap Detector             → Unexplored research areas
    └─► Moderator Agent          → Final balanced insight
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript + TailwindCSS + Vite |
| Backend | Python + FastAPI + SSE streaming |
| LLM | Groq Llama-3.3-70B (primary) |
| Embeddings | HuggingFace all-MiniLM-L6-v2 (default, free) |
| Database | Supabase PostgreSQL + pgvector |
| Paper Sources | arXiv · Semantic Scholar · PubMed |

---

## Project Structure

```
ResearchPilot/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings
│   ├── models.py            # Pydantic models
│   ├── database.py          # Supabase client
│   ├── agents/              # 9 reasoning agents + orchestrator
│   ├── retrieval/           # arXiv, SS, PubMed clients + embeddings
│   ├── routes/              # API endpoints
│   └── db/migrations/       # SQL migration for Supabase
└── frontend/
    └── src/
        ├── components/      # Navbar, SearchBar, ReasoningPipeline, etc.
        ├── pages/           # HomePage, AnalysisPage
        └── lib/             # API client, TypeScript types
```
