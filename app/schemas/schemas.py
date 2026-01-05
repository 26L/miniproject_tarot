from pydantic import BaseModel
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime

# --- Card Schemas ---
class TarotCardBase(BaseModel):
    card_id: int
    name_en: str
    name_kr: str
    image_url: str
    suit: str
    number: int
    
class TarotCardDetail(TarotCardBase):
    element: str
    keywords: Dict[str, List[str]]
    description: str

class CardDrawResult(TarotCardBase):
    position_index: int
    is_reversed: bool

# --- Reading Schemas ---
class ReadingCreate(BaseModel):
    user_id: Optional[UUID] = None
    question: Optional[str] = None
    spread_type: str = "three_card"

class ReadingResponse(BaseModel):
    session_id: UUID
    status: str
    created_at: datetime

class DrawRequest(BaseModel):
    session_id: UUID
    spread_type: str = "three_card" # Used to determine how many cards to draw if not strictly defined by session

class DrawResponse(BaseModel):
    session_id: UUID
    spread_type: str
    cards: List[CardDrawResult]
