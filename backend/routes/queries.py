"""
Queries API – retrieve research query history.
"""
from fastapi import APIRouter, HTTPException
from typing import List
import database

router = APIRouter(prefix="/api/queries", tags=["queries"])


@router.get("/", response_model=List[dict])
async def list_queries(limit: int = 20):
    """List recent research queries."""
    return await database.get_queries(limit=limit)
