from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orm import Lead, Listing
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

# ── Schemas ───────────────────────────────────────────────────

class LeadCreate(BaseModel):
    listing_id: str
    name: str
    phone: str
    email: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    timeline: Optional[str] = None  # immediate | 3months | 6months | exploring

class LeadOut(BaseModel):
    id: uuid.UUID
    listing_id: Optional[uuid.UUID]
    name: str
    phone: str
    email: Optional[str]
    budget_min: Optional[float]
    budget_max: Optional[float]
    timeline: Optional[str]
    score: float
    qualified: bool
    notes: Optional[str]

    class Config:
        from_attributes = True

# ── Endpoints ─────────────────────────────────────────────────

@router.post("/", response_model=LeadOut)
def create_lead(data: LeadCreate, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == data.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    # basic auto score before AI scorer is built
    score = 0.0
    if data.timeline == "immediate":
        score += 40
    elif data.timeline == "3months":
        score += 25
    elif data.timeline == "6months":
        score += 10

    if data.budget_min and data.budget_max:
        score += 30
    elif data.budget_max:
        score += 15

    if data.email:
        score += 10

    if data.phone:
        score += 20

    qualified = score >= 50

    lead = Lead(
        **data.model_dump(),
        score=score,
        qualified=qualified
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("/", response_model=list[LeadOut])
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()


@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}/qualify")
def qualify_lead(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.qualified = True
    db.commit()
    return {"message": "Lead manually qualified", "id": lead_id}