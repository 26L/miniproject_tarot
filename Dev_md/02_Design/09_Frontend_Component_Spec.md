# 14. 프론트엔드 API 연동 및 에러 핸들링 가이드 (Frontend API Integration Guide)

## 1. 개요 (Overview)
본 문서는 프론트엔드(`app.js`)에서 백엔드 API를 호출할 때 준수해야 할 요청/응답 처리 패턴과 예외 상황(Error Handling)에 대한 대응 지침을 정의합니다.

## 2. API 요청 표준 패턴 (Request Pattern)
모든 API 호출은 `async/await`와 `try-catch` 블록을 사용하며, 사용자 경험을 저해하지 않도록 **로딩 상태(Loading State)**를 관리해야 합니다.

### 2.1 기본 템플릿
```javascript
async function callApi() {
    // 1. Loading UI On
    showLoading(true); 
    
    try {
        const response = await fetch('/api/v1/...', { ... });
        
        // 2. HTTP Error Handling
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'API Request Failed');
        }
        
        // 3. Success Handling
        const data = await response.json();
        return data;
        
    } catch (error) {
        // 4. Error UI Handling
        handleApiError(error);
    } finally {
        // 5. Loading UI Off
        showLoading(false);
    }
}
```

## 3. 에러 상황별 대응 가이드 (Error Handling)

### 3.1 HTTP 상태 코드별 대응
| Status Code | 의미 | 대응 시나리오 | 사용자 메시지 예시 |
| :--- | :--- | :--- | :--- |
| **400** | Bad Request | 입력값 검증 실패 (빈 질문 등) | "질문 내용을 확인해주세요." |
| **404** | Not Found | 세션 만료, 잘못된 ID | "세션이 만료되었습니다. 처음으로 돌아갑니다." (Intro 이동) |
| **429** | Too Many Requests | 과도한 요청 (Rate Limit) | "잠시 후 다시 시도해주세요." |
| **500** | Server Error | 서버 내부 오류, LLM 연동 실패 | "서버에 문제가 발생했습니다. 잠시 후 다시 시도해주세요." |
| **Network** | Connection Fail | 인터넷 연결 끊김 | "네트워크 연결을 확인해주세요." |

### 3.2 사용자 알림 (Notification)
*   **Toast Message:** 일시적인 오류(400, 429)는 화면 상단/하단에 토스트 메시지로 알림.
*   **Modal Alert:** 치명적인 오류(404, 500)나 흐름을 중단해야 하는 경우 모달 창 사용.

## 4. 스트리밍 데이터 처리 (SSE Handling)
해석 데이터(`POST /interpretations/stream`)는 일반 JSON이 아닌 스트림으로 오므로 별도의 처리가 필요합니다.

```javascript
async function readStream(response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        // "event: message\ndata: ...\n\n" 파싱 로직 필요
        // 청크 단위로 UI 업데이트 (Typewriter 효과 연동)
    }
}
```

---

# 15. UI 컴포넌트 명세서 (UI Component Specification)

## 1. 버튼 (Buttons)
*   `.primary-btn`: 주요 액션 (시작하기, 결과 보기). 배경색 `--gold`, 텍스트 검정.
*   `.secondary-btn`: 보조 액션 (다시 하기). 배경 투명, 테두리 `--gold`, 텍스트 `--gold`.
*   **State:**
    *   `:hover`: 밝기 증가 (brightness 110%) 또는 크기 확대 (scale 1.05).
    *   `:disabled`: 투명도 50%, 커서 `not-allowed`.

## 2. 입력 필드 (Inputs)
*   `textarea`, `input[type="text"]`
*   **Style:** 배경 반투명(`rgba(255,255,255,0.1)`), 테두리 없음(Focus 시 `--gold` 테두리).
*   **Validation:** 에러 발생 시 테두리 색상 `red`로 변경 및 흔들림 애니메이션(`shake`).

## 3. 카드 (Tarot Cards)
*   **Container:** `.card-slot` (카드가 놓일 위치).
*   **Inner:** `.tarot-card` (실제 카드 객체).
*   **State Class:**
    *   `.flipped`: 앞면이 보이도록 회전된 상태.
    *   `.reversed`: 카드가 역방향(거꾸로)인 상태 (`transform: rotate(180deg)`).
    *   `.selected`: 결과 화면에서 사용자가 클릭하여 강조된 상태.

## 4. 로딩 인디케이터 (Loading Indicator)
*   **Overlay:** 전체 화면을 덮는 반투명 검정 배경.
*   **Spinner:** 중앙에서 회전하는 수정구슬 또는 타로 덱 애니메이션.

```