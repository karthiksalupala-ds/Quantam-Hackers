"""
ResearchPilot – FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from routes import research, papers, queries

settings = get_settings()

app = FastAPI(
    title="ResearchPilot API",
    description="Agentic AI-Powered Research Intelligence Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(research.router, prefix="/research", tags=["Research"])
app.include_router(papers.router, prefix="/papers", tags=["Papers"])
app.include_router(queries.router, prefix="/queries", tags=["Queries"])


@app.get("/", tags=["health"])
async def root():
    return {
        "service": "ResearchPilot API",
        "version": "1.0.0",
        "status": "operational",
        "demo_mode": settings.is_demo,
        "llm_provider": settings.llm_provider,
        "embedding_provider": settings.embedding_provider,
    }


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
