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

## 2. API 요청/응답 DTO (Request/Response Schemas)

### 2.1 세션 및 셔플 (Session & Shuffle)

**Request: `POST /api/reading/shuffle`**
```json
{
  "user_id": "UUID-STRING (Optional)" 
}
```

**Response: `200 OK`**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "shuffled",
  "created_at": "2026-01-05T14:30:00Z"
}
```

### 2.2 카드 뽑기 (Draw Cards)

**Request: `POST /api/reading/draw`**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "spread_type": "three_card",
  "question": "이번 프로젝트가 성공할까요?"
}
```

**Response: `200 OK`**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "spread_type": "three_card",
  "cards": [
    {
      "position_index": 0,
      "card_id": 12,
      "is_reversed": false,
      "name_kr": "매달린 남자",
      "image_url": "..."
    },
    {
      "position_index": 1,
      "card_id": 5,
      "is_reversed": true,
      "name_kr": "교황",
      "image_url": "..."
    }
    // ...
  ]
}
```

### 2.3 AI 해석 요청 (Interpretation)

**Request: `POST /api/reading/interpret/stream`**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "이번 프로젝트가 성공할까요?",
  "selected_cards": [ ... ] 
}
```

**Response: `200 OK (Event-Stream)`**
```text
data: {"chunk": "카드들을 살펴보면, "}
data: {"chunk": "현재 상황에서 잠시 멈춤이 필요해 보입니다. "}
data: {"chunk": "매달린 남자는 새로운 관점을..."}
...
data: {"status": "done"}
```

---

## 3. 데이터셋 준비 현황 (Dataset Status)

- [ ] **Tarot Card JSON**: 78장 영문/한글 데이터, 키워드 매핑 필요.
- [ ] **Spread Config JSON**: 기본 3종(원카드, 쓰리카드, 켈틱) 좌표 데이터 필요.
- [ ] **DB Seed Script**: 초기 데이터 적재를 위한 Python 스크립트 필요.
