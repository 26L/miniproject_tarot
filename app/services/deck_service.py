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

    async def create_reading_session(self, question: str, spread_type: str, user_id=None) -> dict:
        """
        Creates a session, shuffles, draws cards, and returns the result.
        """
        session_id = uuid4()
        
        # 1. Get Spread Info
        spread = spread_service.get_spread(spread_type)
        if not spread:
            raise ValueError(f"Unknown spread type: {spread_type}")
        
        # 2. Get & Shuffle Cards
        all_cards = await self.repo.get_all_cards()
        shuffled_deck = Shuffler.shuffle(all_cards)
        
        # 3. Draw Cards
        drawn_cards_result = []
        count = spread.card_count
        for i in range(count):
            if not shuffled_deck:
                break
            card = shuffled_deck.pop()
            is_reversed = Shuffler.pick_card([True, False])
            pos_meaning = spread.positions[i].meaning if i < len(spread.positions) else f"Position {i+1}"
            
            drawn_cards_result.append(CardDrawResult(
                card_id=card.id,
                name_en=card.name_en,
                name_kr=card.name_kr,
                image_url=card.image_url,
                suit=card.suit,
                number=card.number,
                position_index=i,
                position_meaning=pos_meaning,
                is_reversed=is_reversed,
                keywords=card.keywords,
                description=card.description
            ))
        
        # 4. Store session data (in-memory)
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "question": question,
            "spread_type": spread_type,
            "drawn_cards": [card.model_dump() for card in drawn_cards_result],
            "deck": shuffled_deck, # Remaining deck
        }
        
        # 5. Prepare response
        spread_config_response = {
            "id": spread.id,
            "name_kr": spread.name_kr,
            "card_count": spread.card_count,
            "positions": [p.model_dump() for p in spread.positions]
        }

        return {
            "session_id": session_id,
            "spread_config": spread_config_response,
            "cards": drawn_cards_result,
            "created_at": self.sessions[session_id]["created_at"]
        }

# Note: We can't have a global deck_service instance anymore because it needs a DB session.
# We will inject it in the routers.
