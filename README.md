# ResearchPilot 🔬

**Advanced Agentic AI-Powered Research Intelligence Engine**

ResearchPilot is a sophisticated, full-stack AI research platform designed to provide balanced, evidence-based insights. Unlike traditional search engines, it utilizes a **Multi-Agent Debate Pipeline** to analyze information from both academic and web sources, providing a truly comprehensive perspective.

---

## ✨ Key Features

- **🛡️ Resilience & Reliability**: Built-in LLM fallback mechanism. If one provider (Groq, OpenAI, Gemini, OpenRouter) fails, the system automatically switches to another to ensure uninterrupted analysis.
- **⚖️ Multi-Agent Debate**: Uses a 5-agent pipeline (Pro vs. Con) to critically evaluate research evidence and synthesize a balanced executive summary.
- **🔍 Hybrid Retrieval (RAG)**: Integrates real-time data from **arXiv**, **Semantic Scholar**, **PubMed**, and **Google Search** (via Serper.dev).
- **💎 Premium Perplexity-Style UI**: A state-of-the-art dark-glass interface featuring animated reasoning "thought" bubbles and high-impact hero result cards.
- **⚡ High Performance**: Powered by **Groq Llama-3.3 70B** for near-instantaneous reasoning and response generation.

---

## 🚀 Quick Start

### 1. Backend

```bash
cd backend

# Copy and fill in your API keys
cp .env.example .env

# Install dependencies and start
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to start researching.

---

## 🧩 Agentic Architecture

ResearchPilot operates as a coordinated "Intelligence Unit":

1.  **Query Refiner (OpenAI)**: Transmutes vague queries into precise academic research questions.
2.  **Hybrid Retrieval**: Concurrently pulls data from Academic (arXiv, SS, PubMed) and Web (Google Search) sources.
3.  **The Debate (Groq/Gemini/OpenRouter)**:
    -   **Pro Agents**: Focus on direct and systemic benefits.
    -   **Con Agents**: Focus on direct and systemic risks/limitations.
4.  **Moderator (OpenAI)**: Synthesizes the 4-way debate into a single, high-fidelity Executive Summary.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18 · TypeScript · TailwindCSS · Lucide Icons |
| **Backend** | Python · FastAPI · SSE Streaming · Pydantic |
| **Intelligence** | Groq (Llama-3) · OpenAI (GPT-4o) · Google (Gemini) · OpenRouter |
| **Data Storage** | Supabase · PostgreSQL · pgvector |
| **Search** | Serper.dev · arXiv API · Semantic Scholar API |

---

## 🔑 Environment Variables

| Variable | Description |
| :--- | :--- |
| `GROQ_API_KEY` | High-speed Llama-3.3 reasoning. |
| `OPENAI_API_KEY` | Precision synthesis and query refinement. |
| `GOOGLE_API_KEY` | Diverse research perspective via Gemini. |
| `OPENROUTER_API_KEY` | Access to 100+ open-source models. |
| `SERPER_API_KEY` | Google Search integration for web insights. |

---

## 📁 Project Structure

```text
ResearchPilot/
├── backend/
│   ├── agents/          # Agent Logic (Pro/Con/Moderator/fallback)
│   ├── retrieval/       # Multi-source API clients (ArXiv/Google/PubMed)
│   ├── database.py      # Supabase & Vector Storage
│   └── models.py        # Pydantic Schemas
└── frontend/
    ├── src/components/  # Premium UI (ReasoningPipeline/SettingsModal)
    └── src/pages/       # Glassmorphic Routing
```

Developed with ❤️ for researchers who value balance over bias.
