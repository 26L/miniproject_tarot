import json
import os
from typing import List
from app.schemas.schemas import TarotCardDetail

class CardRepository:
    def __init__(self):
        # Temporary: Load from JSON for v0.1 without DB dependency
        self._cards: List[TarotCardDetail] = []
        self._load_from_json()

    def _load_from_json(self):
        file_path = "data/tarot_cards.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._cards = [TarotCardDetail(**item) for item in data]
        else:
            print(f"Warning: {file_path} not found.")

    def get_all_cards(self) -> List[TarotCardDetail]:
        return self._cards

    def get_card_by_id(self, card_id: int) -> TarotCardDetail | None:
        for card in self._cards:
            if card.card_id == card_id:
                return card
        return None
