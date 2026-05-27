from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class Agency(Base):
    __tablename__ = "agencies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(20))
    city = Column(String(100))
    plan = Column(String(20), default="free")
    created_at = Column(DateTime, default=datetime.utcnow)
    listings = relationship("Listing", back_populates="agency")

class Listing(Base):
    __tablename__ = "listings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agencies.id"))
    title = Column(String(300), nullable=False)
    description = Column(Text)
    city = Column(String(100))
    locality = Column(String(100))
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqft = Column(Float)
    property_type = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    agency = relationship("Agency", back_populates="listings")

class Lead(Base):
    __tablename__ = "leads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"))
    name = Column(String(200))
    phone = Column(String(20))
    email = Column(String(200))
    budget_min = Column(Float)
    budget_max = Column(Float)
    timeline = Column(String(50))
    score = Column(Float, default=0.0)
    qualified = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)