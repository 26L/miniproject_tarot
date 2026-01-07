# 04. API 데이터 구조 및 데이터셋 명세 (API Data Structures & Datasets)

본 문서는 프론트엔드와 백엔드 간의 데이터 교환을 위한 **JSON 스키마(DTO)** 및 **초기 데이터셋** 구조를 정의합니다. 모든 스키마는 **Pydantic V2**를 기준으로 작성됩니다.

---

## 1. 핵심 데이터 모델 (Core Data Models)

### 1.1 타로 카드 (Tarot Card)
`78장`의 타로 카드 메타데이터 구조입니다. DB 저장 및 프론트엔드 카드 렌더링에 사용됩니다.

```json
{
  "card_id": 1,
  "name_en": "The Magician",
  "name_kr": "마법사",
  "image_url": "/static/cards/major_01_magician.webp",
  "suit": "Major",
  "number": 1,
  "element": "Air",
  "keywords": {
    "upright": ["창조력", "자신감", "재능", "실행"],
    "reversed": ["혼란", "속임수", "무능력", "지연"]
  },
  "description": "무한한 잠재력과 창조적인 힘을 상징하는 카드..."
}
```

### 1.2 스프레드 정보 (Spread Config)
카드 배열법에 대한 좌표 및 메타데이터입니다.

```json
{
  "spread_id": "three_card",
  "name": "Three Card Spread",
  "card_count": 3,
  "positions": [
    {
      "index": 0,
      "meaning": "과거",
      "x_coord": 100,
      "y_coord": 200,
      "description": "과거의 원인"
    },
    {
      "index": 1,
      "meaning": "현재",
      "x_coord": 300,
      "y_coord": 200,
      "description": "현재의 상황"
    },
    {
      "index": 2,
      "meaning": "미래",
      "x_coord": 500,
      "y_coord": 200,
      "description": "예상되는 결과"
    }
  ]
}
```

---

## 2. API 요청/응답 DTO (Request/Response Schemas) - v0.4

### 2.1 타로 리딩 생성 및 드로우 통합 (Reading & Draw)

**Request: `POST /api/v1/readings`**
```json
{
  "question": "이번 프로젝트가 성공할까요?",
  "spread_type": "three_card",
  "user_id": "UUID-STRING (Optional)"
}
```

**Response: `200 OK`**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "spread_config": {
    "id": "three_card",
    "card_count": 3,
    "positions": [{"index": 0, "meaning": "과거"}, ...]
  },
  "cards": [
    {
      "card_id": 1,
      "name_kr": "광대",
      "is_reversed": false,
      "position_meaning": "과거",
      "image_url": "/static/cards/tarot_the_fool.png",
      ...
    }
  ],
  "created_at": "2026-01-06T..."
}
```

### 2.2 AI 해석 스트리밍 (Interpretation Stream)

**Request: `POST /api/v1/interpretations/stream`**
```json
{
  "session_id": "UUID",
  "question": "질문 내용",
  "spread_type": "three_card",
  "selected_cards": [ ... ] 
}
```

**Response: `200 OK (Event-Stream)`**
```text
data: 오늘 당신의 운세는...
data: 과거 위치의 카드는...
data: [DONE]
```

---

## 3. RAG 지식 데이터셋 명세 (Knowledge Dataset for RAG)

RAG 엔진이 검색할 수 있도록 타로 카드별 상세 지식을 텍스트 파일로 구조화합니다.

### 3.1 파일 구조 (`data/knowledge/`)
카드 한 장당 하나의 Markdown(`.md`) 파일로 구성하여 관리 효율성과 검색 정확도를 높입니다.
- 경로: `data/knowledge/{card_id}_{name_en}.md`
- 예: `data/knowledge/01_the_fool.md`

### 3.2 문서 템플릿
```markdown
# [타로 지식] {name_kr} ({name_en})

## 기본 의미
{description}

## 상징성
{element}, {suit}, {number}

## 정방향 해석 (Upright Keywords)
- {keywords.upright}

## 역방향 해석 (Reversed Keywords)
- {keywords.reversed}

## 상세 해석 가이드
- 금전운: ...
- 연애운: ...
```

---

### 4. 스프레드 데이터 구조 (`config/spreads.json`)
```json
{
  "spreads": [
    {
      "id": "one_card",
      "name_kr": "원 카드",
      ...
    },
    {
      "id": "three_card",
      "name_kr": "쓰리 카드",
      ...
    }
  ]
}
```
