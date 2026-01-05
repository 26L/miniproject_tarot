import json
import os
from typing import List, Dict, Optional
from pydantic import BaseModel

class PositionInfo(BaseModel):
    index: int
    meaning: str

class SpreadInfo(BaseModel):
    id: str
    name_kr: str
    name_en: str
    card_count: int
    description: str
    positions: List[PositionInfo]

class SpreadService:
    def __init__(self):
        self.spreads: Dict[str, SpreadInfo] = {}
        self._load_config()

    def _load_config(self):
        config_path = "config/spreads.json"
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("spreads", []):
                    self.spreads[item["id"]] = SpreadInfo(**item)
        else:
            # Fallback default
            self.spreads["three_card"] = SpreadInfo(
                id="three_card",
                name_kr="쓰리 카드",
                name_en="Three Card",
                card_count=3,
                description="Default spread",
                positions=[
                    {"index": 0, "meaning": "과거"},
                    {"index": 1, "meaning": "현재"},
                    {"index": 2, "meaning": "미래"}
                ]
            )

    def get_spread(self, spread_id: str) -> Optional[SpreadInfo]:
        return self.spreads.get(spread_id)

    def list_spreads(self) -> List[SpreadInfo]:
        return list(self.spreads.values())

spread_service = SpreadService()
