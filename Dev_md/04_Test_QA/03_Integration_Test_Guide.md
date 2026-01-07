# 21. 통합 테스트 자동화 가이드 및 계획 (Automated Integration Testing Guide)

## 1. 개요 (Overview)
본 문서는 PyTarot v0.4의 백엔드 API와 프론트엔드 로직 간의 통합 동작을 검증하기 위한 **자동화 테스트 전략** 및 **실행 가이드**입니다.
현재 수동 테스트로 검증된 시나리오를 코드로 구현하여, 배포 전 안정성을 확보하는 것을 목표로 합니다.

## 2. 테스트 범위 (Test Scope)
*   **API 통합 테스트:** `/api/v1/readings` (세션 생성, 셔플, 드로우) 및 `/api/v1/interpretations/stream` (해석)의 응답 데이터 무결성 검증.
*   **시나리오 테스트:** [질문 입력 -> 스프레드 선택 -> 카드 결과 수신]의 전체 흐름(End-to-End Flow)이 정상 작동하는지 확인.
*   *제외 범위:* UI 렌더링(CSS, Animation) 등의 시각적 요소는 본 자동화 테스트 범위에서 제외하며, 이는 수동 테스트(Dev_md/16)로 대체합니다.

## 3. 테스트 환경 구성 (Test Environment)
*   **Framework:** `pytest` (테스트 러너), `pytest-asyncio` (비동기 테스트 지원), `httpx` (비동기 HTTP 클라이언트).
*   **Database:** 테스트용 격리된 데이터베이스(SQLite In-memory) 또는 별도의 Test DB 파일 사용.

## 4. 상세 테스트 시나리오 (Test Cases)

### TC-API-01: 타로 리딩 세션 생성 (Happy Path)
*   **입력:** 질문("직업운"), 스프레드("three_card")
*   **검증:**
    1.  HTTP 상태 코드 200 반환.
    2.  `session_id` (UUID) 존재 확인.
    3.  `cards` 배열의 길이가 3인지 확인.
    4.  각 카드의 `position_meaning`이 ["과거", "현재", "미래"]와 일치하는지 확인.

### TC-API-02: 잘못된 입력 처리 (Error Handling)
*   **입력:** 질문 누락(""), 존재하지 않는 스프레드("five_card")
*   **검증:**
    1.  HTTP 상태 코드 400 또는 422 반환.
    2.  에러 메시지에 적절한 사유가 포함되어 있는지 확인.

### TC-API-03: 해석 스트리밍 연결 (Integration)
*   **전제:** TC-API-01에서 생성된 유효한 `session_id` 사용.
*   **입력:** 생성된 세션 ID.
*   **검증:**
    1.  HTTP 상태 코드 200 반환.
    2.  `Content-Type` 헤더가 `text/event-stream`인지 확인.
    3.  응답 본문(Body)에서 데이터를 청크 단위로 수신 가능한지 확인.

### TC-API-04: AI 모델 응답 검증 (AI Response Verification)
*   **목표:** 실제 LLM(LangChain)이 프롬프트를 받아 정상적으로 텍스트를 생성하는지 검증.
*   **주의:** API 호출 비용 발생 가능성 있음 (Mocking 권장되나, 통합 테스트에서는 실제 호출 1회 수행).
*   **검증:**
    1.  생성된 해석 텍스트가 비어있지 않은지 확인.
    2.  응답 내용에 "긍정적 측면" 또는 "부정적 측면"과 같은 구조적 키워드가 포함되어 있는지 확인 (프롬프트 지침 준수 여부).

## 5. 테스트 실행 가이드 (Execution Guide)

### 5.1 사전 준비
```bash
# 가상환경 활성화
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 의존성 설치 (이미 설치됨)
# pip install pytest pytest-asyncio httpx
```

### 5.2 테스트 코드 위치
`tests/integration/test_api_flow.py` (신규 생성 예정)

### 5.3 실행 명령어
```bash
# 전체 테스트 실행
pytest

# 상세 로그 출력 포함 실행
pytest -v

# 특정 테스트 파일만 실행
pytest tests/integration/test_api_flow.py
```

## 6. 향후 계획 (Next Steps)
본 통합 테스트 스크립트는 향후 **CI/CD 파이프라인(Github Actions 등)**에 포함되어, 코드 변경 시마다 자동으로 실행되도록 구성할 예정입니다.
