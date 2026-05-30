from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orm import Agency, Listing, Lead
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

# ── Schemas ───────────────────────────────────────────────────

class AgencyCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None

class AgencyUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    plan: Optional[str] = None

class AgencyOut(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    phone: Optional[str]
    city: Optional[str]
    plan: str

    class Config:
        from_attributes = True

# ── Endpoints ─────────────────────────────────────────────────

@router.post("/", response_model=AgencyOut)
def create_agency(data: AgencyCreate, db: Session = Depends(get_db)):
    existing = db.query(Agency).filter(Agency.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    agency = Agency(**data.model_dump())
    db.add(agency)
    db.commit()
    db.refresh(agency)
    return agency


@router.get("/", response_model=list[AgencyOut])
def get_agencies(db: Session = Depends(get_db)):
    return db.query(Agency).all()


@router.get("/{agency_id}", response_model=AgencyOut)
def get_agency(agency_id: str, db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency


@router.put("/{agency_id}", response_model=AgencyOut)
def update_agency(agency_id: str, data: AgencyUpdate, db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(agency, field, value)
    db.commit()
    db.refresh(agency)
    return agency


@router.get("/{agency_id}/listings")
def get_agency_listings(agency_id: str, db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    listings = db.query(Listing).filter(
        Listing.agency_id == agency_id,
        Listing.is_active == True
    ).all()
    return {
        "agency": agency.name,
        "total_listings": len(listings),
        "listings": listings
    }


@router.get("/{agency_id}/leads")
def get_agency_leads(agency_id: str, db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")

    # get all listing IDs for this agency
    listing_ids = [l.id for l in db.query(Listing).filter(
        Listing.agency_id == agency_id
    ).all()]

    # get leads linked to this agency's listings OR unlinked leads
    leads = db.query(Lead).filter(
        (Lead.listing_id.in_(listing_ids)) | (Lead.listing_id == None)
    ).all()

    return {
        "agency": agency.name,
        "total_leads": len(leads),
        "qualified_leads": sum(1 for l in leads if l.qualified),
        "leads": leads
    }