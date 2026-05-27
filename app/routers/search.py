from fastapi import APIRouter, Query
from typing import Optional
from rag_pipeline.query import semantic_search

router = APIRouter()

@router.get("/")
def smart_search(
    q: str = Query(..., description="Natural language search query"),
    city: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    n: int = Query(5, le=20),
):
    """
    Semantic property search.
    Example: /search/?q=spacious flat near school with parking&city=Indore&max_price=6000000
    """
    results = semantic_search(
        query=q,
        city=city,
        max_price=max_price,
        bedrooms=bedrooms,
        n_results=n,
    )
    return {
        "query": q,
        "total": len(results),
        "results": results,
    }