# 12. 프론트엔드 개발 가이드라인 (Frontend Development Guidelines)

## 1. 개요 (Overview)
본 문서는 `PyTarot` 프로젝트의 프론트엔드 코드 품질과 일관성을 유지하기 위한 개발 표준을 정의합니다. 모든 프론트엔드 작업(HTML, CSS, JS)은 이 가이드라인을 준수해야 합니다.

## 2. 디렉토리 구조 및 파일 명명 (Directory & Naming)
### 2.1 디렉토리 구조
FastAPI의 정적 파일 표준을 따릅니다.
```
static/
├── assets/           # (Optional) 이미지, 폰트 등 정적 리소스
│   └── cards/        # 타로 카드 이미지
├── css/              # 스타일시트 (v0.3 이후 구조화 권장)
├── js/               # 자바스크립트 모듈
├── index.html        # 메인 진입점
├── style.css         # 메인 스타일시트
└── app.js            # 메인 로직
```
*   현재는 `static/` 루트에 주요 파일이 위치하지만, 파일이 늘어날 경우 하위 폴더로 정리합니다.

### 2.2 명명 규칙 (Naming Convention)
*   **파일/폴더:** `kebab-case` (소문자 + 하이픈). 예: `user-profile.js`, `main-style.css`.
*   **이미지:** `snake_case` (Python 프로젝트와의 통일성). 예: `tarot_the_fool.png`.

## 3. HTML 코딩 컨벤션 (HTML Standards)
*   **시맨틱 태그 사용:** `div` 남발을 지양하고 `<header>`, `<main>`, `<section>`, `<footer>`, `<article>` 등을 적절히 사용합니다.
*   **들여쓰기:** **4 Spaces** (Python 코드와의 가독성 통일).
*   **ID vs Class:**
    *   `ID`: 페이지 내에서 유일한 요소, 또는 JS에서 `getElementById`로 접근해야 하는 핵심 컨테이너에만 사용 (예: `#step-intro`, `#deck`).
    *   `Class`: 스타일링 및 반복되는 요소에 사용.
*   **속성 정렬:** 중요도 순 (`id`, `class`, `name`, `data-*`, `src`, `href`...).

## 4. CSS 스타일 가이드 (CSS Guidelines)
*   **방법론:** **BEM (Block Element Modifier)** 패턴을 느슨하게 적용하여 클래스 명의 명확성을 높입니다.
    *   `Block`: `.card`
    *   `Element`: `.card__image`, `.card__title`
    *   `Modifier`: `.card--flipped`, `.card--active`
*   **CSS 변수 (Variables):** 색상, 폰트, 공통 수치 등은 `:root`에 변수로 정의하여 재사용성을 높입니다.
    ```css
    :root {
        --color-bg: #1a0b2e;
        --color-accent: #ffd700;
        --spacing-md: 1rem;
    }
    ```
*   **단위:** 반응형을 위해 `px` 대신 `rem`, `em`, `%`, `vh/vw` 사용을 권장합니다.
*   **Reset:** 브라우저 기본 스타일 초기화를 위해 필요한 부분만 명시적으로 재설정합니다 (`box-sizing: border-box` 등).

## 5. JavaScript 컨벤션 (JavaScript Standards)
*   **버전:** **ES6+ (ECMAScript 2015+)** 문법 사용.
*   **변수 선언:** `var` 사용 금지. 변경 없는 값은 `const`, 변경되는 값은 `let` 사용.
*   **비동기 처리:** Promise 체이닝보다 `async/await` 구문을 선호합니다.
    ```javascript
    // Good
    async function fetchReading() {
        try {
            const res = await fetch('/api/...');
            const data = await res.json();
        } catch (error) {
            console.error(error);
        }
    }
    ```
*   **함수:** 화살표 함수(`=>`)를 적극 활용하되, `this` 바인딩이 필요한 경우 주의합니다.
*   **주석:** 복잡한 로직이나 함수에는 JSDoc 스타일의 주석을 달아 설명합니다.

## 6. 에셋 및 이미지 (Assets)
*   **이미지 경로:** CSS나 HTML에서 절대 경로(`/static/...`)를 사용합니다.
*   **최적화:** 가능한 가벼운 이미지 포맷(WebP, PNG)을 사용하며, 너무 큰 이미지는 리사이징 후 포함시킵니다.
*   **접근성:** `<img>` 태그 사용 시 `alt` 속성을 반드시 작성합니다.

## 7. 브라우저 호환성 및 반응형 (Compatibility & Responsive)
*   **대상 브라우저:** Chrome, Edge, Firefox, Safari 최신 버전 (IE 지원 안 함).
*   **반응형 디자인:** Mobile First 접근을 고려하되, 기본적으로 데스크탑/모바일 양쪽에서 깨지지 않는 UI를 목표로 합니다.
*   **Breakpoints:**
    *   Mobile: < 768px
    *   Tablet: 768px ~ 1024px
    *   Desktop: > 1024px
