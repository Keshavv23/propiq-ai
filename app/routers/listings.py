from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orm import Listing, Agency
from app.services.cache import cache_get, cache_set, cache_delete_pattern
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class ListingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    city: str
    locality: str
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: float
    property_type: str
    agency_id: str

class ListingOut(BaseModel):
    id: uuid.UUID
    title: str
    city: str
    locality: str
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: float
    property_type: str
    description: Optional[str]
    is_active: bool
    agency_id: Optional[uuid.UUID]

    class Config:
        from_attributes = True


@router.get("/", response_model=list[ListingOut])
def get_listings(
    city: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    locality: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    # build cache key from query params
    cache_key = f"listings:{city}:{property_type}:{min_price}:{max_price}:{bedrooms}:{locality}:{limit}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    q = db.query(Listing).filter(Listing.is_active == True)
    if city:
        q = q.filter(Listing.city.ilike(f"%{city}%"))
    if property_type:
        q = q.filter(Listing.property_type == property_type)
    if min_price:
        q = q.filter(Listing.price >= min_price)
    if max_price:
        q = q.filter(Listing.price <= max_price)
    if bedrooms:
        q = q.filter(Listing.bedrooms == bedrooms)
    if locality:
        q = q.filter(Listing.locality.ilike(f"%{locality}%"))

    results = q.limit(limit).all()

    # serialize and cache for 5 minutes
    serialized = [
        {
            "id": str(r.id),
            "title": r.title,
            "city": r.city,
            "locality": r.locality,
            "price": r.price,
            "bedrooms": r.bedrooms,
            "bathrooms": r.bathrooms,
            "area_sqft": r.area_sqft,
            "property_type": r.property_type,
            "description": r.description,
            "is_active": r.is_active,
            "agency_id": str(r.agency_id) if r.agency_id else None,
        }
        for r in results
    ]
    cache_set(cache_key, serialized, ttl=300)
    return results


@router.get("/city/{city}", response_model=list[ListingOut])
def get_listings_by_city(city: str, db: Session = Depends(get_db)):
    listings = db.query(Listing).filter(
        Listing.city.ilike(f"%{city}%"),
        Listing.is_active == True
    ).all()
    if not listings:
        raise HTTPException(status_code=404, detail=f"No listings found in {city}")
    return listings


@router.get("/{listing_id}", response_model=ListingOut)
def get_listing(listing_id: str, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.post("/", response_model=ListingOut)
def create_listing(data: ListingCreate, db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.id == data.agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    listing = Listing(**data.model_dump())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    # invalidate cache
    cache_delete_pattern("listings:*")
    return listing


@router.delete("/{listing_id}")
def delete_listing(listing_id: str, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    listing.is_active = False
    db.commit()
    cache_delete_pattern("listings:*")
    return {"message": "Listing deactivated", "id": listing_id}