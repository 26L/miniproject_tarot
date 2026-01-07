# 07. 테스트 전략 및 케이스 (Test Strategy & Cases)

본 문서는 PyTarot 시스템의 안정성을 보장하기 위한 테스트 접근 방식과 주요 시나리오를 정의합니다. `pytest` 프레임워크를 표준으로 사용합니다.

## 1. 테스트 레벨 (Test Levels)

### 1.1 단위 테스트 (Unit Tests)
- **목표:** 개별 함수 및 클래스(특히 Service 계층)의 논리적 정확성 검증.
- **범위:** 셔플 알고리즘, Pydantic 모델 검증, 유틸리티 함수.
- **도구:** `pytest`, `pytest-mock` (외부 의존성 Mocking).

### 1.2 통합 테스트 (Integration Tests)
- **목표:** API 엔드포인트와 DB/Cache 간의 상호작용 검증.
- **범위:** API Router → Service → Repository → DB 흐름.
- **전략:** 테스트용 인메모리 DB(SQLite) 또는 Docker 컨테이너 사용.

---

## 2. 주요 테스트 시나리오 (Key Test Cases)

### 2.1 덱 및 셔플 (Deck & Shuffle)
| ID | 시나리오 | 예상 결과 | 비고 |
|:---:|:---|:---|:---|
| **TC-01** | `create_shuffled_session` 호출 | 0~77 중복 없는 리스트 생성, 세션 ID 반환 | `secrets` 모듈 사용 필수 |
| **TC-02** | `draw_cards` (정상) | 요청 수만큼 카드 반환, 남은 덱 감소 | 중복 뽑기 없어야 함 |
| **TC-03** | `draw_cards` (잔여 부족) | `DeckEmptyError` 또는 400 에러 발생 | 예외 처리 검증 |
| **TC-04** | 셔플 무작위성 검증 | 1000번 수행 시 특정 패턴(순서) 반복 없음 | 통계적 검증(Chi-square 등) |

### 2.2 AI 해석 (Interpretation)
| ID | 시나리오 | 예상 결과 | 비고 |
|:---:|:---|:---|:---|
| **TC-05** | LLM API 호출 Mocking | 정상적인 텍스트 응답 반환 | 실제 과금 방지 |
| **TC-06** | 스트리밍 응답 구조 | SSE 포맷(`data: ...`) 준수 여부 확인 | Async Generator 테스트 |
| **TC-07** | 프롬프트 주입 방지 | 악의적 질문에 대해서도 페르소나 유지 | 보안 테스트 |

---

## 3. 테스트 환경 구성 (Setup)

```python
# conftest.py 예시
import pytest
from app.main import app
from httpx import AsyncClient

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```
