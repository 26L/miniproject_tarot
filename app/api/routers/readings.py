from fastapi import APIRouter, HTTPException, Depends
from app.services.deck_service import deck_service
from app.schemas.schemas import ReadingCreate, ReadingResponse, DrawRequest, DrawResponse

router = APIRouter()

@router.post("/shuffle", response_model=ReadingResponse)
async def shuffle_deck(reading_in: ReadingCreate):
    """
    Starts a new reading session and shuffles the deck securely.
    """
    return deck_service.create_session(user_id=reading_in.user_id)

@router.post("/draw", response_model=DrawResponse)
async def draw_cards(draw_in: DrawRequest):
    """
    Draws cards for the specified spread type.
    """
    # Define card counts for spreads
    spread_counts = {
        "one_card": 1,
        "three_card": 3,
        "celtic_cross": 10
    }
    
    count = spread_counts.get(draw_in.spread_type, 3)
    
    cards = deck_service.draw_cards(draw_in.session_id, count)
    
    if not cards:
        raise HTTPException(status_code=400, detail="Session expired or invalid")
        
    return DrawResponse(
        session_id=draw_in.session_id,
        spread_type=draw_in.spread_type,
        cards=cards
    )
