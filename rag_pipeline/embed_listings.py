import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_pipeline.chroma_client import get_collection
from app.database import SessionLocal
from app.models.orm import Listing

def build_listing_text(listing) -> str:
    price_in_lakhs = listing.price / 100000
    return (
        f"{listing.title}. "
        f"Located in {listing.locality}, {listing.city}. "
        f"Property type: {listing.property_type}. "
        f"{listing.bedrooms} bedroom, {listing.bathrooms} bathroom. "
        f"Area: {listing.area_sqft} square feet. "
        f"Price: {price_in_lakhs:.1f} lakhs rupees. "
        f"{listing.description or ''}"
    )

def embed_all_listings():
    db = SessionLocal()
    collection = get_collection()
    try:
        listings = db.query(Listing).filter(Listing.is_active == True).all()
        print(f"Embedding {len(listings)} listings...")
        ids = []
        texts = []
        metadatas = []
        for listing in listings:
            text = build_listing_text(listing)
            ids.append(str(listing.id))
            texts.append(text)
            metadatas.append({
                "city": listing.city or "",
                "locality": listing.locality or "",
                "property_type": listing.property_type or "",
                "bedrooms": listing.bedrooms or 0,
                "price": listing.price or 0,
                "area_sqft": listing.area_sqft or 0,
                "title": listing.title,
            })
        collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
        )
        print(f"Done! {len(ids)} listings embedded.")
    finally:
        db.close()

if __name__ == "__main__":
    embed_all_listings()