# 06. 서비스 상세 설계 (Service Detailed Design)

## 1. DeckService
타로 카드의 셔플, 세션 관리, 카드 드로우를 담당하는 핵심 서비스입니다.

### 1.1 주요 기능
*   **Session Management:** 사용자별 고유 세션 ID 발급 및 덱 상태 관리 (In-Memory -> DB 이관 예정).
*   **Cryptographic Shuffle:** `secrets` 모듈을 이용한 Fisher-Yates 셔플 알고리즘 적용.
*   **Dynamic Spread Drawing:** `SpreadService`와 연동하여 선택한 스프레드(원카드, 쓰리카드 등)에 맞춰 카드를 뽑고 위치 의미를 부여.

### 1.2 흐름도
1.  사용자가 `POST /shuffle` 요청.
2.  `DeckService`가 DB에서 전체 카드를 로드하고 셔플하여 세션 생성.
3.  사용자가 `POST /draw` 요청 (Spread Type 지정).
4.  `SpreadService`에서 해당 스프레드의 카드 장수 및 위치 의미 조회.
5.  지정된 장수만큼 카드를 뽑고(pop), 정/역방향 결정 후 반환.

---

## 2. SpreadService (New in v0.2)
`config/spreads.json` 설정 파일을 로드하여 다양한 타로 배열법을 관리합니다.

### 2.1 데이터 구조
```json
{
  "id": "three_card",
  "card_count": 3,
  "positions": [
    {"index": 0, "meaning": "과거"},
    {"index": 1, "meaning": "현재"},
    {"index": 2, "meaning": "미래"}
  ]
}
```

### 2.2 역할
*   새로운 스프레드 추가 시 코드 수정 없이 JSON 설정만 변경하면 됩니다.
*   `DeckService`에 카드 장수 정보를, `InterpretationService`에 위치별 해석 가이드를 제공합니다.

---

## 3. InterpretationService
LangChain을 활용하여 뽑힌 카드와 질문을 결합해 AI 해석을 생성합니다.

### 3.1 프로세스
1.  사용자 질문 + 선택된 카드(위치 의미 포함) + 스프레드 정보 수신.
2.  `System Prompt`에 타로 리더 페르소나 주입.
3.  LLM(OpenAI/Gemini)에 프롬프트 전송.
4.  SSE(Server-Sent Events)를 통해 토큰 단위로 실시간 응답 스트리밍.