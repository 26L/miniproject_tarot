# 01. 개발 표준 및 아키텍처 가이드 (Development Standards & Architecture)

## 1. 코딩 컨벤션 (Coding Conventions)

본 프로젝트는 **PEP 8** 표준을 엄격히 준수하며, 가독성과 유지보수성을 위해 다음 규칙을 따릅니다.

### 1.1 스타일 가이드
- **Formatter:** `Black` (Line Length: 88자)
- **Linter:** `Ruff` 또는 `Pylint`
- **Import 정렬:** `isort` 표준 사용 (Standard -> Third-party -> Local)

### 1.2 타입 힌팅 (Type Hinting)
- Python 3.11+ 문법을 사용합니다.
- **모든 함수와 메서드**에 파라미터 및 반환 타입 힌트를 명시해야 합니다.
- Pydantic V2를 활용하여 데이터 구조를 정의합니다.

```python
# Bad
def get_user(id):
    return db.query(User).get(id)

# Good
from uuid import UUID
from app.models.user import User

async def get_user(user_id: UUID) -> User | None:
    """사용자 ID로 사용자 정보를 조회합니다."""
    return await db.query(User).filter(User.id == user_id).first()
```

### 1.3 주석 및 Docstring
- **Google Style Docstring**을 사용합니다.
- 복잡한 로직에는 'Why(왜)'에 대한 주석을 작성합니다.

### 1.4 문서화 규칙 (Documentation Rules)
- **파일 네이밍:** `Dev_md` 폴더 내의 모든 문서는 정렬과 순서 파악을 위해 **반드시 두 자리 숫자와 언더스코어(예: `01_`, `02_`)**로 시작해야 합니다.
- **예시:** `05_TODO_list.md`, `06_Meeting_Notes.md`

---

## 2. 아키텍처 구조 (Architecture Structure)

본 프로젝트는 **Layered Architecture**를 채택하여 관심사를 분리합니다.

### 2.1 계층별 역할
1.  **Presentation Layer (`app/api`)**:
    - 요청/응답 처리, 데이터 검증(Pydantic), 상태 코드 관리.
    - 비즈니스 로직을 직접 포함하지 않음.
2.  **Service Layer (`app/services`)**:
    - 핵심 비즈니스 로직 구현 (예: 타로 카드 셔플, AI 해석 요청).
    - 트랜잭션 관리.
3.  **Data Access Layer (`app/repositories`)**:
    - DB와의 직접적인 상호작용 (CRUD).
    - SQLAlchemy 모델 사용.
4.  **Model Layer (`app/models`, `app/schemas`)**:
    - `models`: DB 테이블 매핑 (ORM).
    - `schemas`: API 입출력 객체 (DTO).

---

## 3. 핵심 개발 원칙 (Core Principles)

### 3.1 비동기 처리 (Async/Await)
- I/O 바운드 작업(DB 조회, 외부 API 호출)은 반드시 `async/await`를 사용합니다.
- 동기 함수(Sync)가 비동기 로프를 차단하지 않도록 주의합니다.

### 3.2 보안 및 난수 (Security & Randomness)
- 타로 셔플링에는 절대 `random` 모듈을 사용하지 않습니다.
- 반드시 암호학적으로 안전한 `secrets` 모듈을 사용합니다.

```python
import secrets

# Safe
random_index = secrets.randbelow(len(deck))
```

### 3.3 예외 처리 (Error Handling)
- `try-except` 블록을 남용하지 않으며, 구체적인 예외를 잡습니다.
- API 에러는 `HTTPException`을 통해 명확한 메시지와 함께 반환합니다.
