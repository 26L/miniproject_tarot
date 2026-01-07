# 13. 서비스 상세 사양서 v0.3 (Service Detailed Specification)

## 1. 개요 (Overview)
본 문서는 PyTarot v0.3 버전의 **프론트엔드-백엔드 통합 동작 사양**을 정의합니다. 사용자의 타로 리딩 경험 흐름(User Flow)을 기준으로 시스템의 동작과 데이터 교환 방식을 상세히 기술합니다.

## 2. 사용자 시나리오 및 시스템 동작 (User Scenario & System Behavior)

### 단계 1: 인트로 및 설정 (Intro & Setup)
*   **사용자 행동:** 질문을 입력하고, 타로 배열법(Spread)을 선택한 후 '운세 보기' 버튼 클릭.
*   **프론트엔드 동작:**
    *   입력값 검증 (질문 길이 등).
    *   `POST /api/v1/readings` 호출하여 세션 생성 요청.
*   **백엔드 동작:**
    *   세션 ID 생성 및 DB 저장.
    *   선택된 Spread 정보 검증.
    *   전체 카드 덱 초기화 (아직 셔플 전 상태).
*   **데이터 교환:**
    *   **Req:** `{ "question": "...", "spread_id": "three_card" }`
    *   **Res:** `{ "session_id": "uuid-...", "total_cards": 78, "draw_count": 3 }`

### 단계 2: 셔플 및 드로우 (Shuffle & Draw - Integrated)
*   **사용자 행동:** 화면상의 카드 덱이 섞이는 애니메이션을 감상한 후, 덱을 클릭하여 카드를 하나씩 확인(오픈).
*   **프론트엔드 동작:**
    *   단계 1에서 받은 `cards` 데이터를 기반으로, 사용자가 클릭할 때마다 순차적으로 카드 이미지를 공개.
    *   모든 카드가 공개되면 자동으로 결과 단계로 전환 준비.
*   **백엔드 동작:**
    *   이미 단계 1(`POST /readings`)에서 모든 처리가 완료되었으므로, 이 단계에서는 서버와 통신하지 않음 (Client-side interaction).

### 단계 3: 결과 및 해석 (Result & Interpretation)
*   **사용자 행동:** 뒤집힌 카드의 이미지를 확인하고, 실시간으로 생성되는 AI 해석을 읽음.
*   **프론트엔드 동작:**
    *   `POST /api/v1/interpretations/stream` 호출하여 SSE 연결.
    *   수신되는 텍스트 청크(Chunk)를 타자 치듯 화면에 출력.

## 3. API 인터페이스 명세 (API Specifications)

### 3.1 세션 생성 및 결과 수신 (Create Reading & Draw)
*   **URL:** `POST /api/v1/readings`
*   **Request Body:**
    ```json
    {
      "question": "연애운이 궁금해요",
      "spread_type": "three_card" // "one_card" | "three_card"
    }
    ```
*   **Response:**
    ```json
    {
      "session_id": "550e8400-e29b-...",
      "spread_config": {
          "id": "three_card",
          "card_count": 3,
          "positions": [
              {"index": 0, "meaning": "과거"},
              ...
          ]
      },
      "cards": [ 
          {"card_id": 12, "name_en": "The Fool", "position_index": 0, ...},
          ...
      ],
      "created_at": "2026-01-06T..."
    }
    ```

### 3.2 해석 스트리밍 (Stream Interpretation)
*   **URL:** `POST /api/v1/interpretations/stream`
*   **Request Body:**
    ```json
    {
      "session_id": "550e8400-e29b-..."
    }
    ```
    *   *변경점:* 이미 서버 세션에 뽑힌 카드 정보가 저장되어 있으므로, 클라이언트가 카드 정보를 다시 보낼 필요가 없습니다. `session_id`만 보내면 됩니다.
*   **Response:** `text/event-stream`

## 4. 예외 처리 (Error Handling)
*   **400 Bad Request:** 질문이 비어있거나 지원하지 않는 스프레드 타입. -> "올바른 질문을 입력해주세요." 알림.
*   **404 Not Found:** 유효하지 않은 세션 ID. -> "세션이 만료되었습니다. 처음부터 다시 시작해주세요." (Intro로 리다이렉트).
*   **500 Internal Server Error:** LLM 연동 실패 등. -> "운명의 목소리를 듣는데 잠시 문제가 생겼습니다. 잠시 후 다시 시도해주세요."

## 5. 데이터베이스 스키마 요구사항 (DB Requirements)
*   `readings` 테이블에 `spread_type`, `drawn_cards` (JSON) 컬럼이 필요하거나 적절히 매핑되어야 함.
*   v0.3에서는 일단 In-Memory 또는 파일 시스템 로그로 대체 가능하나, 추후 DB 연동 시 이 구조를 따름.
