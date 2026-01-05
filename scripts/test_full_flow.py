import asyncio
import json
from app.services.deck_service import DeckService
from app.services.interpretation_service import interpretation_service
from app.core.config import settings

async def test_full_flow():
    print("=== PyTarot Full Flow Test (DB & Spread Integrated) ===")
    
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        deck_service = DeckService(db)
        
        # 1. Shuffle (Create Session)
        print("\n[1/3] Shuffling & Creating Session...")
        session_resp = await deck_service.create_session()
        session_id = session_resp.session_id
        print(f"OK: Session Created -> {session_id}")

        # 2. Draw Cards (Three Card Spread)
        print("\n[2/3] Drawing 3 Cards (Three Card Spread)...")
        cards = await deck_service.draw_cards(session_id, "three_card")
        for i, card in enumerate(cards):
            orientation = "역방향" if card.is_reversed else "정방향"
            print(f"Card {i+1} [{card.position_meaning}]: {card.name_kr} ({orientation})")
        
        # 3. AI Interpretation (Streaming)
    print("\n[3/3] Requesting AI Interpretation (Streaming)...")
    question = "올해 연애운이 어떨까요?"
    print(f"Question: {question}")
    print("-" * 30)
    
    full_text = ""
    try:
        async for chunk in interpretation_service.stream_interpretation(
            question=question,
            spread_type="three_card",
            cards=cards
        ):
            print(chunk, end="", flush=True)
            full_text += chunk
    except Exception as e:
        print(f"\nError during AI streaming: {e}")
    
    print("\n" + "-" * 30)
    print("\n=== Test Finished Successfully ===")
    
    return {
        "session_id": str(session_id),
        "cards": [f"{c.name_kr}({'역' if c.is_reversed else '정'})" for c in cards],
        "interpretation_length": len(full_text)
    }

if __name__ == "__main__":
    if not settings.GOOGLE_API_KEY or "AIza" not in settings.GOOGLE_API_KEY:
        print("Error: Google API Key is missing or invalid in .env")
    else:
        results = asyncio.run(test_full_flow())
        # Save results for report
        with open("data/test_result.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
