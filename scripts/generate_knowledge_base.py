import json
import os

def generate_knowledge_base():
    input_path = "data/tarot_cards.json"
    output_dir = "data/knowledge"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    for card in cards:
        card_id = str(card.get("card_id", "0")).zfill(2)
        name_en = card.get("name_en", "unknown").lower().replace(" ", "_")
        file_name = f"{card_id}_{name_en}.md"
        file_path = os.path.join(output_dir, file_name)
        
        content = f"""# [타로 지식] {card.get('name_kr')} ({card.get('name_en')})

## 기본 의미
{card.get('description', '설명이 없습니다.')}

## 상징성
- 원소: {card.get('element', 'N/A')}
- 슈트: {card.get('suit', 'N/A')}
- 번호: {card.get('number', 'N/A')}

## 정방향 해석 (Upright Keywords)
{', '.join(card.get('keywords', {}).get('upright', []))}

## 역방향 해석 (Reversed Keywords)
{', '.join(card.get('keywords', {}).get('reversed', []))}

## 리딩 가이드
이 카드는 {card.get('name_kr')}로서 {card.get('description')[:50]}... 의 에너지를 가지고 있습니다.
사용자의 질문에 따라 긍정적으로는 {card.get('keywords', {}).get('upright', ['강점'])[0]}의 면모를 보이기도 하지만, 
부정적으로는 {card.get('keywords', {}).get('reversed', ['주의'])[0]}의 측면을 조심해야 합니다.
"""
        with open(file_path, "w", encoding="utf-8") as f_out:
            f_out.write(content)
            
    print(f"Successfully generated {len(cards)} knowledge files in {output_dir}.")

if __name__ == "__main__":
    generate_knowledge_base()
