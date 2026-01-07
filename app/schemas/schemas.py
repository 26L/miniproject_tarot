from pydantic import BaseModel, Field
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
    position_meaning: str
    is_reversed: bool
    keywords: Dict[str, List[str]]
    description: str

# --- Reading Schemas ---
class ReadingCreate(BaseModel):
    user_id: Optional[UUID] = None
    question: str = Field(..., min_length=1) # 필수 필드, 최소 길이 1
    spread_type: str = "three_card"

class SpreadConfigResponse(BaseModel):
    id: str
    name_kr: str
    card_count: int
    positions: List[Dict[str, int | str]]

class ReadingResponse(BaseModel):
    session_id: UUID
    spread_config: SpreadConfigResponse
    cards: List[CardDrawResult]
    created_at: datetime

# Deprecated in v0.3 - Merged into ReadingResponse
# class DrawRequest(BaseModel):
#     session_id: UUID
#     spread_type: str = "three_card" 

# class DrawResponse(BaseModel):
#     session_id: UUID
#     spread_type: str
#     cards: List[CardDrawResult]
