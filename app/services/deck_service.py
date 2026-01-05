from typing import List
from uuid import uuid4
from datetime import datetime
from app.core.shuffler import Shuffler
from app.repositories.card_repository import CardRepository
from app.schemas.schemas import CardDrawResult, ReadingResponse, DrawResponse

class DeckService:
    def __init__(self):
        self.repo = CardRepository()
        # In-memory session store for prototype (Replace with Redis/DB later)
        self.sessions = {} 

    def create_session(self, user_id=None) -> ReadingResponse:
        session_id = uuid4()
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "deck": self.repo.get_all_cards(), # Full deck
            "drawn": []
        }
        return ReadingResponse(
            session_id=session_id,
            status="shuffled",
            created_at=self.sessions[session_id]["created_at"]
        )

    def draw_cards(self, session_id, count: int) -> List[CardDrawResult]:
        session_str_id = str(session_id)
        # Handle UUID vs String key match (simplification for prototype)
        session = None
        for k, v in self.sessions.items():
            if str(k) == str(session_id):
                session = v
                break
        
        if not session:
            # Fallback: Create new session if not found (for stateless testing)
            full_deck = self.repo.get_all_cards()
            session = {"deck": full_deck}
        
        # Shuffle logic: Always shuffle before drawing in this model, or shuffle once at start.
        # Here we shuffle the remaining deck
        current_deck = session["deck"]
        shuffled_deck = Shuffler.shuffle(current_deck)
        
        drawn_cards = []
        for i in range(count):
            if not shuffled_deck:
                break
            card = shuffled_deck.pop()
            
            # Random reversal
            is_reversed = Shuffler.pick_card([True, False])
            
            drawn_cards.append(CardDrawResult(
                **card.model_dump(),
                position_index=i,
                is_reversed=is_reversed
            ))
            
        # Update session (mock)
        session["deck"] = shuffled_deck
        return drawn_cards

deck_service = DeckService()
