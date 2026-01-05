from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    readings = relationship("Reading", back_populates="user")

class TarotCard(Base):
    __tablename__ = "tarot_cards"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String, unique=True)
    name_kr = Column(String)
    image_url = Column(String)
    suit = Column(String) # Major, Wands, Cups...
    number = Column(Integer)
    element = Column(String)
    keywords = Column(JSON) # {upright: [], reversed: []}
    description = Column(Text)

class Reading(Base):
    __tablename__ = "readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    question = Column(Text, nullable=True)
    spread_type = Column(String, default="three_card")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="readings")
    details = relationship("ReadingDetail", back_populates="reading")

class ReadingDetail(Base):
    __tablename__ = "reading_details"

    id = Column(Integer, primary_key=True, index=True)
    reading_id = Column(UUID(as_uuid=True), ForeignKey("readings.id"))
    card_id = Column(Integer, ForeignKey("tarot_cards.id"))
    position_index = Column(Integer)
    is_reversed = Column(Boolean, default=False)
    
    reading = relationship("Reading", back_populates="details")
    card = relationship("TarotCard")
