# 10. 프론트엔드 설계 및 UX 가이드 (Frontend Design & UX)

## 1. 디자인 컨셉 (Design Concept)
*   **Theme:** `Mystical Dark` (Deep Purple #1a0b2e, Gold #ffd700 accents).
*   **Atmosphere:** 신비롭고 차분한 분위기, 사용자가 점술가와 대화하는 듯한 몰입감 제공.
*   **Typography:** 가독성 높은 산세리프(본문) + 장식적인 세리프(제목/카드명).

## 2. 페이지 구조 (Page Structure)
SPA(Single Page Application) 형태로, 단계별로 화면이 전환되는 **Step-by-Step** 방식을 채택합니다.

### 2.1 메인 스테이지 (Main Stage)
화면 중앙에 콘텐츠가 위치하며, 진행 단계에 따라 섹션이 교체됩니다.

| 단계 | 섹션 ID | 주요 구성 요소 | 사용자 행동 |
| :--- | :--- | :--- | :--- |
| **1. 시작** | `step-intro` | 타이틀, 질문 입력창, **스프레드 선택 드롭다운** | 질문 입력 및 배열법 선택 후 '타로 보기' 클릭 |
| **2. 셔플** | `step-shuffle` | 카드 덱 애니메이션, 진행률 표시 | (자동 진행) 또는 덱 클릭하여 섞기 |
| **3. 드로우** | `step-draw` | 덱(Deck), **빈 슬롯(Spread Slots)** | 덱을 클릭하여 빈 슬롯 채우기 (장수만큼 반복) |
| **4. 결과** | `step-result` | 선택된 카드 리스트(뒤집힘), **AI 해석 텍스트 영역** | 카드 확인 및 실시간 해석 읽기 |

## 3. 주요 기능 및 상태 관리 (Features & State)

### 3.1 스프레드 선택 (Spread Selector)
*   **Data Source:** 백엔드 `config/spreads.json`과 동기화된 하드코딩 데이터 또는 API 호출.
*   **Logic:** 사용자가 선택한 스프레드(`spread_type`)에 따라 **드로우 단계의 빈 슬롯 개수**가 달라져야 합니다.
    *   원카드: 1 slot
    *   쓰리카드: 3 slots

### 3.2 카드 드로우 인터랙션
*   **Deck:** 화면 하단 또는 중앙에 카드 뒷면 뭉치 배치.
*   **Action:** 덱 클릭 시 카드가 날아가서 해당 슬롯에 안착하는 애니메이션 구현.
*   **Constraint:** 정해진 장수(`count`)를 모두 뽑을 때까지 다음 단계로 넘어가지 않음.

### 3.3 결과 및 스트리밍 (Result & Streaming)
*   **Card Reveal:** 결과 화면 진입 시 순차적으로 카드가 뒤집히며(`flip`) 그림이 나타남.
*   **Interpretation:** `fetch` API와 `TextDecoder`를 사용하여 SSE 스트림을 수신, 타자 치듯 텍스트 출력.
*   **Auto-scroll:** 텍스트가 길어질 경우 자동으로 스크롤 하단 이동.

## 4. API 연동 규격 (Frontend <-> Backend)

### 4.1 셔플 요청
*   `POST /api/reading/shuffle`
*   **Req:** `{ "question": "...", "spread_type": "three_card" }` (spread_type 추가 필요)
*   **Res:** `{ "session_id": "uuid..." }`

### 4.2 드로우 요청 (수정 필요)
*   현재 백엔드는 한 번에 `draw_cards`로 모든 카드를 받지만, 프론트엔드 UX상 **'클릭할 때마다 한 장씩'** 보여주는 연출이 필요할 수 있습니다.
*   **옵션 A (Simple):** 백엔드에서 한 번에 3장을 다 받고, 프론트엔드에서 하나씩 애니메이션으로 보여줌. (v0.3 채택)
*   **옵션 B (Complex):** 백엔드에 `draw_one` API 추가.

### 4.3 해석 요청
*   `POST /api/reading/interpret/stream`
*   **Req:** `{ "session_id": "...", "cards": [...] }`

## 5. CSS 애니메이션 전략
*   `@keyframes shuffle`: 카드가 섞이는 움직임.
*   `@keyframes deal`: 덱에서 슬롯으로 이동.
*   `@keyframes flip`: 3D 회전으로 앞면/뒷면 전환.
