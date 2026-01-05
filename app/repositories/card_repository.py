from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.all_models import TarotCard
from app.schemas.schemas import TarotCardDetail

class CardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_cards(self) -> List[TarotCard]:
        """Fetches all tarot cards from the database."""
        result = await self.db.execute(select(TarotCard))
        return result.scalars().all()

    async def get_card_by_id(self, card_id: int) -> Optional[TarotCard]:
        """Fetches a specific card by its ID."""
        result = await self.db.execute(
            select(TarotCard).filter(TarotCard.id == card_id)
        )
        return result.scalar_one_or_none()
