import asyncio
from app.services.deck_service import deck_service
from app.services.interpretation_service import interpretation_service

async def capture():
    session_resp = deck_service.create_session()
    cards = deck_service.draw_cards(session_resp.session_id, 3)
    question = "올해 전반적인 운세와 주의할 점이 궁금해요."
    
    full_text = ""
    async for chunk in interpretation_service.stream_interpretation(
        question=question,
        spread_type="three_card",
        cards=cards
    ):
        full_text += chunk
    
    with open("data/sample_interpretation.txt", "w", encoding="utf-8") as f:
        f.write(f"질문: {question}\n")
        f.write("-" * 30 + "\n")
        for i, card in enumerate(cards):
            orientation = "역방향" if card.is_reversed else "정방향"
            f.write(f"카드 {i+1}: {card.name_kr} ({orientation})\n")
        f.write("-" * 30 + "\n\n")
        f.write(full_text)

if __name__ == "__main__":
    asyncio.run(capture())

