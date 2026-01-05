import json
import os

cards_dir = "static/cards/"
output_file = "data/tarot_cards.json"

# List of Major Arcana in order
major_arcana = [
    ("The Fool", "광대", "the_fool"),
    ("The Magician", "마법사", "the_magician"),
    ("The High Priestess", "고위 여사제", "the_high_priestess"),
    ("The Empress", "여황제", "the_empress"),
    ("The Emperor", "황제", "the_emperor"),
    ("The Hierophant", "교황", "the_hierophant"),
    ("The Lovers", "연인", "the_lovers"),
    ("The Chariot", "전차", "the_chariot"),
    ("Strength", "힘", "strength"),
    ("The Hermit", "은둔자", "the_hermit"),
    ("Wheel of Fortune", "운명의 수레바퀴", "wheel_of_fortune"),
    ("Justice", "정의", "justice"),
    ("The Hanged Man", "매달린 남자", "the_hanged_man"),
    ("Death", "죽음", "death"),
    ("Temperance", "절제", "temperance"),
    ("The Devil", "악마", "the_devil"),
    ("The Tower", "탑", "the_tower"),
    ("The Star", "별", "the_star"),
    ("The Moon", "달", "the_moon"),
    ("The Sun", "태양", "the_sun"),
    ("Judgement", "심판", "judgement"),
    ("The World", "세계", "the_world")
]

suits = [("Wands", "완드"), ("Cups", "컵"), ("Swords", "검"), ("Pentacles", "펜타클")]
ranks = [
    ("Ace", "에이스", "ace"), ("Two", "2", "two"), ("Three", "3", "three"),
    ("Four", "4", "four"), ("Five", "5", "five"), ("Six", "6", "six"),
    ("Seven", "7", "seven"), ("Eight", "8", "eight"), ("Nine", "9", "nine"),
    ("Ten", "10", "ten"), ("Page", "페이지", "page"), ("Knight", "기사", "knight"),
    ("Queen", "퀸", "queen"), ("King", "킹", "king")
]

tarot_dataset = []
card_id = 1

# Process Major Arcana
for en, kr, file_part in major_arcana:
    tarot_dataset.append({
        "card_id": card_id,
        "name_en": en,
        "name_kr": kr,
        "image_url": f"/static/cards/tarot_{file_part}.png",
        "suit": "Major",
        "number": card_id - 1,
        "element": "Varies",
        "keywords": {"upright": ["키워드1", "키워드2"], "reversed": ["역방향1", "역방향2"]},
        "description": f"{kr} 카드에 대한 기본 설명입니다."
    })
    card_id += 1

# Process Minor Arcana
for suit_en, suit_kr in suits:
    for rank_en, rank_kr, rank_file in ranks:
        file_name = f"tarot_{rank_file}_of_{suit_en.lower()}.png"
        tarot_dataset.append({
            "card_id": card_id,
            "name_en": f"{rank_en} of {suit_en}",
            "name_kr": f"{suit_kr} {rank_kr}",
            "image_url": f"/static/cards/{file_name}",
            "suit": suit_en,
            "number": (card_id - 23) % 14 + 1,
            "element": suit_en,
            "keywords": {"upright": ["키워드1", "키워드2"], "reversed": ["역방향1", "역방향2"]},
            "description": f"{suit_kr} {rank_kr} 카드에 대한 기본 설명입니다."
        })
        card_id += 1

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(tarot_dataset, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(tarot_dataset)} cards in {output_file}")
