import asyncio
import json
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, AsyncSessionLocal
from app.models.all_models import TarotCard
from sqlalchemy import select

async def seed_data():
    print("🌱 Starting Database Seeding...")

    # 1. Create Tables (if not exist)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables Created/Verified.")

    # 2. Load JSON Data
    json_path = "data/tarot_cards.json"
    if not os.path.exists(json_path):
        print(f"❌ Error: {json_path} not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        cards_data = json.load(f)
    print(f"📄 Loaded {len(cards_data)} cards from JSON.")

    async with AsyncSessionLocal() as session:
        # Check if data already exists
        result = await session.execute(select(TarotCard))
        existing_cards = result.scalars().all()
        
        if existing_cards:
            print(f"⚠️ Database already contains {len(existing_cards)} cards. Skipping insertion.")
            return

        # Insert Data
        new_cards = []
        for idx, item in enumerate(cards_data):
            card = TarotCard(
                id=item.get("id", idx + 1), # Use index if id is missing
                name_en=item["name_en"],
                name_kr=item["name_kr"],
                image_url=item["image_url"],
                suit=item["suit"],
                number=item["number"],
                element=item.get("element"),
                keywords=item["keywords"],
                description=item["description"]
            )
            new_cards.append(card)
        
        session.add_all(new_cards)
        await session.commit()
        print(f"✅ Successfully inserted {len(new_cards)} cards into database.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_data())
