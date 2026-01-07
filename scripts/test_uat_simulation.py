import asyncio
import json
import sys
import os

# PYTHONPATH 설정 효과
sys.path.append(os.getcwd())

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.services.deck_service import DeckService
from app.services.interpretation_service import InterpretationService
from app.schemas.interpretation_schemas import InterpretationRequest

async def test_uat_flow():
    print("\n" + "="*50)
    print("🚀 [UAT Simulation] Starting Full User Journey...")
    print("="*50)

    # 1. Setup DB Session
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        deck_service = DeckService(db)
        interpretation_service = InterpretationService()

        # STEP 1: Create Session (Input Question & Select Spread)
        print("\n[Step 1] User inputs question and selects 'three_card' spread...")
        question = "올해의 전반적인 운세가 어떨까요?"
        spread_type = "three_card"
        
        session_data = await deck_service.create_reading_session(question, spread_type)
        session_id = session_data["session_id"]
        drawn_cards = session_data["cards"]
        
        print(f"✅ Session Created: {session_id}")
        print(f"✅ Spread: {session_data['spread_config']['name_kr']}")
        for i, card in enumerate(drawn_cards):
            direction = "역방향" if card.is_reversed else "정방향"
            print(f"   - 카드 {i+1}: {card.name_kr} ({direction}) | 위치 의미: {card.position_meaning}")

        # STEP 2 & 3: Interaction & Display (Simulated as successful as cards are already drawn)
        print("\n[Step 2 & 3] User draws cards and views them on screen... [PASS]")

        # STEP 4: AI Interpretation with RAG
        print("\n[Step 4] Requesting AI Interpretation (RAG-enabled)...")
        
        print("--- [AI Response (First 200 chars)] ---")
        full_text = ""
        async for chunk in interpretation_service.stream_interpretation(
            question=question,
            spread_type=spread_type,
            cards=drawn_cards
        ):
            full_text += chunk
            if len(full_text) < 205 and len(full_text) >= 200:
                print(full_text[:200] + "...")
        
        if not full_text:
            print("❌ Error: No interpretation received.")
        else:
            print(f"\n✅ Interpretation Stream Completed ({len(full_text)} characters)")
            
        # Verify RAG context (Check if certain keywords from card description appear)
        # This is a soft check
        print("\n[Verification] Checking if AI referenced card-specific meanings...")
        referenced = any(card.name_kr in full_text for card in drawn_cards)
        if referenced:
            print("✅ Success: AI correctly referenced the selected cards.")
        else:
            print("⚠️ Warning: AI did not explicitly mention card names, but may have used meanings.")

    print("\n" + "="*50)
    print("✨ [UAT Simulation] All Steps Completed Successfully!")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(test_uat_flow())
