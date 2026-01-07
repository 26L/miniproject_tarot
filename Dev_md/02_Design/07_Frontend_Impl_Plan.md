# 🏗️ v0.3 프론트엔드 구현 계획 (Frontend Implementation Plan)

본 문서는 `Dev_md/10_Frontend_Design_and_UX.md`에 정의된 설계를 바탕으로, 실제 구현을 위한 상세 작업 단계를 정의합니다.

## 1. 개요
*   **목표:** 단순한 폼 기반 UI를 몰입감 있는 **단계별(Step-by-Step) SPA(Single Page Application)** 형태로 전환.
*   **테마:** Mystical Dark & Gold.

## 2. 상세 작업 순서

### 2.1 HTML 구조 재설계 (`static/index.html`)
*   **레이아웃 변경:** 기존의 단일 폼 형태를 제거하고, `main` 컨테이너 안에 4개의 독립된 섹션(`section`)을 배치.
*   **섹션 정의:**
    *   `#step-intro`: 타이틀, 질문 입력, 스프레드 선택(Select Box).
    *   `#step-shuffle`: 셔플 애니메이션 영역, 안내 문구.
    *   `#step-draw`: 카드 덱(Deck)과 선택된 카드가 놓일 슬롯(Slots) 영역.
    *   `#step-result`: 결과 카드 리스트(앞면), 해석 텍스트 영역(Typewriter effect).
*   **공통 요소:** 헤더(로고), 배경 요소(별/달 장식 등).

### 2.2 스타일링 상세 설계 (`static/style.css`)
*   **Color Palette (Mystical Dark):**
    *   `--bg-deep`: `#0f051d` (심해의 보라색, 전체 배경)
    *   `--bg-panel`: `rgba(30, 15, 60, 0.7)` (반투명 패널)
    *   `--gold`: `#ffd700` (강조색, 텍스트 로고)
    *   `--gold-glow`: `rgba(255, 215, 0, 0.5)` (카드 선택 시 광채)
*   **Layout & Responsive:**
    *   `Main Container`: 최대 너비 1200px, 중앙 정렬.
    *   `Card Slots`: CSS Grid를 사용하여 스프레드 타입에 따라 유연하게 배치.
        *   `one_card`: 1 col
        *   `three_card`: 3 cols (모바일에서는 1 col로 전환)
*   **애니메이션 (Keyframes):**
    *   `@keyframes deck-hover`: 덱 위에 마우스 올릴 때 미세하게 들썩이는 효과.
    *   `@keyframes card-draw`: 덱 위치(`bottom-center`)에서 각 슬롯 위치로 포물선을 그리며 이동.
    *   `@keyframes card-flip`: `perspective`와 `rotateY(180deg)`를 이용한 리얼한 3D 뒤집기.
    *   `@keyframes text-reveal`: 해석 텍스트가 위로 부드럽게 밀려 올라오는 효과.

### 2.3 클라이언트 로직 구현 (`static/app.js`) - 승인된 API 반영
*   **Optimized Flow:**
    1.  `POST /api/v1/readings` 호출 시 질문과 스프레드 타입을 보냄.
    2.  서버로부터 **이미 뽑힌 카드 리스트**를 세션 ID와 함께 즉시 수신.
    3.  프론트엔드 `state`에 카드 정보를 저장하되, 화면에는 뒷면으로 표시.
    4.  사용자가 덱을 클릭할 때마다 저장된 리스트의 순서대로 카드를 슬롯으로 이동(연출).
    5.  모든 카드가 놓이면 자동으로 뒤집기 연출 후 `POST /api/v1/interpretations/stream` 호출.

## 3. 리소스 확인
*   카드 이미지 경로: `static/cards/` (기존 파일 활용).
*   API 엔드포인트 확인:
    *   `POST /api/v1/readings/` (질문/스프레드 생성)
    *   `POST /api/v1/interpretations/stream` (해석 스트림)

## 4. 향후 개선 사항 (Post-v0.3 Enhancements)

### 4.1 부채꼴 카드 선택 인터페이스 (Fan-out Card Selection)
현재의 '쌓여있는 덱(Stack)'을 클릭하는 방식에서, 실제 타로 리딩처럼 **카드를 부채꼴로 넓게 펼쳐놓고 사용자가 직접 원하는 카드를 선택**하는 방식으로 UX를 고도화합니다.

*   **배치 방식:** 화면 하단 또는 상단에 `arc` 형태로 카드 뒷면들을 겹쳐서 배치.
*   **인터랙션:**
    *   **Hover:** 마우스를 올린 카드가 살짝 위로 솟아오름 (`transform: translateY`).
    *   **Click:** 선택된 카드가 슬롯으로 이동하며, 남은 카드들은 자연스럽게 간격이 재조정됨.
*   **기술적 과제:**
    *   CSS `transform-origin`과 `rotate`를 계산하여 동적으로 스타일을 생성해야 함 (JS로 각도 계산).
    *   모바일 화면(좁은 폭)에서의 부채꼴 표현 한계 극복 필요 (스크롤 가능한 가로 슬라이더 형태로 대체 고려).
