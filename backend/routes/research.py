"""
Research API routes – SSE streaming research analysis pipeline.
"""
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models import ResearchRequest
from agents.orchestrator import ResearchOrchestrator

router = APIRouter()
orchestrator = ResearchOrchestrator()


async def _sse_generator(request: ResearchRequest):
    """Async generator that wraps the orchestrator pipeline as SSE events."""
    try:
        async for event in orchestrator.run(request):
            payload = json.dumps(event, default=str)
            yield f"data: {payload}\n\n"
    except Exception as e:
        error_payload = json.dumps({"event": "error", "data": {"message": str(e)}})
        yield f"data: {error_payload}\n\n"
    finally:
        yield "data: {\"event\": \"done\", \"data\": {}}\n\n"


@router.post("/analyze")
async def analyze_research(request: ResearchRequest):
    """
    Stream a full research analysis pipeline via Server-Sent Events.
    Events: step | result | error | done
    """
    if len(request.query.strip()) < 5:
        raise HTTPException(status_code=422, detail="Query too short. Please be more specific.")

    return StreamingResponse(
        _sse_generator(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@router.get("/history")
async def get_history(user_id: str, limit: int = 20):
    """Fetch saved research history for a user."""
    import database
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
        
    queries = await database.get_queries(limit=limit, user_id=user_id)
    
    # Optional: fetch analysis for these queries if needed, 
    # but returning the queries is a good start.
    return {"queries": queries}

