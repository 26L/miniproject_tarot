from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.shuffler import Shuffler
from app.repositories.card_repository import CardRepository
from app.services.spread_service import spread_service
from app.schemas.schemas import CardDrawResult, ReadingResponse

class DeckService:
    def __init__(self, db: AsyncSession):
        self.repo = CardRepository(db)
        # Session storage is still in-memory for now, but uses DB cards
        self.sessions = {} 

    async def create_session(self, user_id=None) -> ReadingResponse:
        session_id = uuid4()
        all_cards = await self.repo.get_all_cards()
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "deck": all_cards,
            "drawn": []
        }
        return ReadingResponse(
            session_id=session_id,
            status="shuffled",
            created_at=self.sessions[session_id]["created_at"]
        )

    async def draw_cards(self, session_id: str, spread_type: str) -> List[CardDrawResult]:
        # Retrieve spread configuration
        spread = spread_service.get_spread(spread_type)
        if not spread:
            raise ValueError(f"Unknown spread type: {spread_type}")
            
        count = spread.card_count
        
        # Handle session lookup
        session = None
        for k, v in self.sessions.items():
            if str(k) == str(session_id):
                session = v
                break
        
        if not session:
            # Fallback for stateless testing or lost sessions
            all_cards = await self.repo.get_all_cards()
            session = {"deck": all_cards}
        
        current_deck = session["deck"]
        shuffled_deck = Shuffler.shuffle(current_deck)
        
        drawn_cards = []
        for i in range(count):
            if not shuffled_deck:
                break
            card = shuffled_deck.pop()
            is_reversed = Shuffler.pick_card([True, False])
            
            # Map position meaning from spread config
            pos_meaning = spread.positions[i].meaning if i < len(spread.positions) else f"Position {i+1}"
            
            # TarotCard model from DB has slightly different attributes than Pydantic schema
            # We convert it here
            drawn_cards.append(CardDrawResult(
                card_id=card.id,
                name_en=card.name_en,
                name_kr=card.name_kr,
                image_url=card.image_url,
                suit=card.suit,
                number=card.number,
                position_index=i,
                position_meaning=pos_meaning, # New field added to schema below
                is_reversed=is_reversed,
                keywords=card.keywords,
                description=card.description
            ))
            
        session["deck"] = shuffled_deck
        return drawn_cards

# Note: We can't have a global deck_service instance anymore because it needs a DB session.
# We will inject it in the routers.
