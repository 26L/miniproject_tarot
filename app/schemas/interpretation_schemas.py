from typing import List
from pydantic import BaseModel
from app.schemas.schemas import CardDrawResult

class InterpretationRequest(BaseModel):
    session_id: str
    question: str
    spread_type: str
    selected_cards: List[CardDrawResult]
