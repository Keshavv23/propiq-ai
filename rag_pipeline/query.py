import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
from rag_pipeline.chroma_client import get_collection

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(
    query: str,
    city: str = None,
    max_price: float = None,
    bedrooms: int = None,
    n_results: int = 5,
) -> list:
    """Search listings using semantic similarity."""
    collection = get_collection()

    # build where filter
    where = {}
    conditions = []
    if city:
        conditions.append({"city": {"$eq": city}})
    if bedrooms:
        conditions.append({"bedrooms": {"$eq": bedrooms}})
    if max_price:
        conditions.append({"price": {"$lte": max_price}})

    if len(conditions) == 1:
        where = conditions[0]
    elif len(conditions) > 1:
        where = {"$and": conditions}

    # embed the query
    query_embedding = model.encode([query]).tolist()[0]

    # search
    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        kwargs["where"] = where

    try:
        results = collection.query(**kwargs)
    except Exception:
        # fallback if filters return no results — search without filters
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

    listings = []
    if results and results["metadatas"]:
        for i, meta in enumerate(results["metadatas"][0]):
            listings.append({
                "title": meta.get("title"),
                "city": meta.get("city"),
                "locality": meta.get("locality"),
                "property_type": meta.get("property_type"),
                "bedrooms": meta.get("bedrooms"),
                "price": meta.get("price"),
                "area_sqft": meta.get("area_sqft"),
                "similarity_score": round(1 - results["distances"][0][i], 3),
            })

    return listings


if __name__ == "__main__":
    # quick test
    results = semantic_search("2BHK flat near mall under 50 lakhs in Indore")
    for r in results:
        print(f"{r['title']} — ₹{r['price']/100000:.0f}L — score: {r['similarity_score']}")