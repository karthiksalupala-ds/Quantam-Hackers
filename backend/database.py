"""
Supabase client wrapper with pgvector search support.
"""
import json
from typing import List, Optional
from supabase import create_client, Client
from config import get_settings
from models import ResearchPaper

settings = get_settings()


def get_supabase() -> Optional[Client]:
    if not settings.supabase_url or not settings.supabase_service_key:
        return None
    return create_client(settings.supabase_url, settings.supabase_service_key)


# ── Paper Storage ──────────────────────────────────────────────

async def store_paper(paper: ResearchPaper, embedding: List[float]) -> Optional[str]:
    client = get_supabase()
    if not client:
        return None
    try:
        result = client.table("research_papers").upsert({
            "title": paper.title,
            "abstract": paper.abstract,
            "content": paper.content,
            "source": paper.source,
            "url": paper.url,
            "authors": json.dumps(paper.authors),
            "year": paper.year,
            "citations": paper.citations,
            "embedding": embedding,
        }, on_conflict="title").execute()
        if result.data:
            return result.data[0].get("id")
    except Exception as e:
        print(f"[DB] Error storing paper: {e}")
    return None


async def similarity_search(embedding: List[float], limit: int = 10) -> List[ResearchPaper]:
    client = get_supabase()
    if not client:
        return []
    try:
        result = client.rpc("match_papers", {
            "query_embedding": embedding,
            "match_count": limit,
            "match_threshold": 0.5,
        }).execute()
        papers = []
        for row in result.data or []:
            papers.append(ResearchPaper(
                id=str(row.get("id", "")),
                title=row.get("title", ""),
                abstract=row.get("abstract", ""),
                content=row.get("content", ""),
                source=row.get("source", ""),
                url=row.get("url"),
                authors=json.loads(row.get("authors", "[]")),
                year=row.get("year"),
                citations=row.get("citations"),
            ))
        return papers
    except Exception as e:
        print(f"[DB] Similarity search error: {e}")
        return []


# ── Query Storage ───────────────────────────────────────────────

async def store_query(user_query: str, refined_query: str) -> Optional[str]:
    client = get_supabase()
    if not client:
        return None
    try:
        result = client.table("research_queries").insert({
            "user_query": user_query,
            "refined_query": refined_query,
        }).execute()
        if result.data:
            return result.data[0].get("id")
    except Exception as e:
        print(f"[DB] Error storing query: {e}")
    return None


async def store_analysis(query_id: str, analysis: dict) -> bool:
    client = get_supabase()
    if not client:
        return False
    try:
        client.table("research_analysis").insert({
            "query_id": query_id,
            "supporting_arguments": analysis.get("supporting_arguments", ""),
            "counter_arguments": analysis.get("counterarguments", ""),
            "evidence_score": analysis.get("evidence_score", 0),
            "final_insight": analysis.get("final_insight", ""),
        }).execute()
        return True
    except Exception as e:
        print(f"[DB] Error storing analysis: {e}")
        return False


async def get_queries(limit: int = 20) -> List[dict]:
    client = get_supabase()
    if not client:
        return []
    try:
        result = client.table("research_queries").select("*").order(
            "timestamp", desc=True
        ).limit(limit).execute()
        return result.data or []
    except Exception as e:
        print(f"[DB] Error fetching queries: {e}")
        return []
