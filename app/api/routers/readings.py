from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import ReadingCreate, ReadingResponse
from app.services.deck_service import DeckService
from app.core.database import get_db

router = APIRouter()

@router.post("", response_model=ReadingResponse)
async def create_reading(
    request: ReadingCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new tarot reading session.
    This single endpoint shuffles, draws cards, and returns the initial state.
    """
    service = DeckService(db)
    try:
        reading_result = await service.create_reading_session(
            question=request.question,
            spread_type=request.spread_type,
            user_id=request.user_id
        )
        return ReadingResponse(**reading_result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # In a real app, log this error
        print(f"Error creating reading: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")