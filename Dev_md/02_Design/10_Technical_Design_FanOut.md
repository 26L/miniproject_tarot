# 18. 부채꼴 카드 선택 인터페이스 기술 설계 (Fan-out Interface Technical Design)

## 1. 개요 (Overview)
본 문서는 v0.4 UX 고도화의 핵심인 **'부채꼴(Fan-out) 카드 선택'** 기능을 구현하기 위한 수학적 알고리즘과 기술적 구현 방식을 정의합니다.

*   **목표:** 78장의 카드를 아치(Arc) 형태로 자연스럽게 펼치고, 사용자가 직관적으로 선택할 수 있는 인터랙션을 제공한다.
*   **제약 사항:** 모바일 환경(좁은 화면)과 데스크탑 환경(넓은 화면) 모두에서 사용 가능해야 한다.

## 2. 부채꼴 배치 알고리즘 (Fan-out Algorithm)
카드를 둥글게 배치하기 위해 CSS `transform` 속성과 삼각함수를 활용합니다.

### 2.1 기본 공식
*   **중심점 (Origin):** 화면 하단 중앙 (`bottom center`).
*   **전체 각도 (Total Angle):** 약 120도 ~ 140도 (부채꼴의 넓이).
*   **반지름 (Radius):** 화면 너비에 비례하되, 최소 600px 이상 (카드가 너무 겹치지 않도록).
*   **각 카드별 각도 (Theta):**
    $$ \theta_i = \text{StartAngle} + (\frac{\text{TotalAngle}}{\text{CardCount} - 1}) \times i $$
*   **CSS 변환:**
    ```css
    transform: rotate(${theta}deg) translateY(-${radius}px);
    transform-origin: bottom center;
    ```
    *   *참고:* `translateY`를 음수로 주어 원점으로부터 바깥쪽으로 밀어내는 방식을 사용하면 계산이 단순해집니다.

### 2.2 구현 상세 (JS Logic)
```javascript
const TOTAL_CARDS = 78; // 혹은 남은 카드 수
const ARC_ANGLE = 90;   // 부채꼴 각도 (deg)
const RADIUS = 800;     // 반지름 (px)

cards.forEach((card, index) => {
    // -45도 ~ +45도 사이로 분포
    const angle = (ARC_ANGLE / (TOTAL_CARDS - 1)) * index - (ARC_ANGLE / 2);
    
    card.style.transformOrigin = `50% ${RADIUS + cardHeight}px`; // 회전축을 멀리 둠
    card.style.transform = `rotate(${angle}deg)`;
});
```

## 3. 인터랙션 설계 (Interaction)

### 3.1 호버 효과 (Hover Effect)
카드가 겹쳐져 있으므로 마우스를 올렸을 때 해당 카드가 잘 보여야 합니다.
*   **Z-Index:** 호버된 카드의 `z-index`를 높여 맨 위로 올립니다.
*   **Scale & Lift:** 크기를 1.2배 확대하고 위로 살짝(`translateY(-20px)`) 띄웁니다.
*   **Sibling Effect:** (선택 사항) 호버된 카드의 양옆 카드들도 살짝 밀어내어 공간을 확보하면 더 자연스럽습니다.

### 3.2 드로우 애니메이션 (Draw Animation)
사용자가 카드를 클릭했을 때의 동작입니다.
1.  **Detach:** 선택된 카드의 `transform` 속성을 초기화하고, 현재 화면 좌표(`getBoundingClientRect`)를 고정(Fixed) 위치로 변경합니다.
2.  **Fly:** 슬롯 위치로 이동하는 애니메이션을 실행합니다 (`static/app.js`의 기존 로직 재사용 가능).
3.  **Re-align:** (옵션) 빠진 카드의 빈자리를 채우기 위해 남은 카드들이 다시 정렬되거나, 빈자리를 그대로 둡니다. (빈자리 유지가 더 현실감 있음).

## 4. 모바일 대응 전략 (Mobile Strategy)
좁은 화면(폭 < 768px)에서는 78장을 부채꼴로 펼치면 카드가 너무 겹쳐서 선택이 불가능합니다.

### 4.1 가로 스크롤 덱 (Horizontal Scroll Deck)
*   모바일에서는 부채꼴 대신 **'가로로 길게 나열된 덱'**을 스크롤하여 탐색하는 UI로 자동 전환합니다.
*   **CSS:**
    ```css
    .mobile-deck-container {
        display: flex;
        overflow-x: auto;
        padding: 20px;
        gap: -30px; /* 카드 겹침 효과 */
    }
    ```

## 5. 백엔드 영향도 분석 (Backend Impact Analysis)
**결론: 백엔드 수정은 불필요합니다.**

*   **이유:**
    *   부채꼴 인터페이스는 순수하게 **클라이언트 사이드(Client-side)의 시각적 표현(View)**에 불과합니다.
    *   백엔드(`POST /readings`)는 이미 "셔플된 78장의 카드 리스트"를 프론트엔드에 제공하고 있습니다.
    *   프론트엔드는 이 리스트를 받아 '쌓아서 보여줄지(Stack)', '펼쳐서 보여줄지(Fan)'만 결정하면 됩니다.
    *   선택된 카드의 정보 처리 로직도 기존과 동일합니다.

## 6. 개발 로드맵
1.  **CSS/HTML:** 부채꼴 배치를 위한 컨테이너(`.fan-container`) 추가.
2.  **JS (Math):** 카드 78개를 아치형으로 배치하는 `renderFanDeck()` 함수 구현.
3.  **JS (Interaction):** 호버 및 클릭 이벤트 핸들링.
4.  **JS (Responsive):** 화면 너비 감지하여 Fan <-> Scroll 모드 전환 로직.
