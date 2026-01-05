from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import ReadingCreate, ReadingResponse, DrawRequest, DrawResponse
from app.services.deck_service import DeckService
from app.core.database import get_db

router = APIRouter()

@router.post("/shuffle", response_model=ReadingResponse)
async def shuffle_deck(
    request: ReadingCreate,
    db: AsyncSession = Depends(get_db)
):
    service = DeckService(db)
    return await service.create_session(user_id=request.user_id)

@router.post("/draw", response_model=DrawResponse)
async def draw_cards(
    request: DrawRequest,
    db: AsyncSession = Depends(get_db)
):
    service = DeckService(db)
    try:
        cards = await service.draw_cards(request.session_id, request.spread_type)
        return DrawResponse(
            session_id=request.session_id,
            spread_type=request.spread_type,
            cards=cards
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error during card draw")
