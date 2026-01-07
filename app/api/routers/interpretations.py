from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.interpretation_service import interpretation_service
from app.schemas.interpretation_schemas import InterpretationRequest
import json
import asyncio

router = APIRouter()

@router.post("/stream")
async def stream_interpretation(request: InterpretationRequest):
    """
    Streams the AI interpretation for the given reading session.
    """
    async def event_generator():
        try:
            async for chunk in interpretation_service.stream_interpretation(
                question=request.question,
                spread_type=request.spread_type,
                cards=request.selected_cards
            ):
                # SSE format: data: <content>\n\n
                # Directly send text chunk for frontend compatibility
                yield f"data: {chunk}\n\n"
            
            # End signal (Optional, or just close stream)
            yield "data: [DONE]\n\n"
        except Exception as e:
            err_msg = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {err_msg}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
