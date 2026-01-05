# 05. 개발 작업 목록 (TODO List)

## 📌 Phase 1: 기반 구축 (Foundation)
- [x] **환경 설정**
  - [x] 프로젝트 폴더 구조 생성
  - [x] 개발 문서(표준, 평가기준 등) 작성
  - [x] `.env.example` 생성
  - [x] 가상환경(`venv`) 설정 및 `.gitignore` 생성
  - [x] `requirements.txt` 작성

- **데이터셋 구축**
  - [x] **[Task]** 타로 카드 78장 JSON 데이터 생성 (`data/tarot_cards.json`)
  - [x] **[Task]** 스프레드 설정 JSON 데이터 생성 (`config/spreads.json`)
  - [x] **[Task]** DB 시드 스크립트 작성 (`scripts/seed_db.py`)

- **FastAPI 기본 설정**
  - [x] **[Task]** `app/main.py` 작성 (Hello World 엔드포인트)
  - [x] **[Task]** `app/core/config.py` 작성 (환경변수 로드)
  - [x] **[Task]** 로깅 및 에러 핸들링 구성 (`app/core/logging_config.py`)

- **데이터베이스**
  - [x] **[Task]** SQLAlchemy 모델 구현 (`app/models/`)
  - [x] **[Task]** DB 연결 세션 관리 (`app/core/database.py`)
  - [ ] **[Task]** Alembic 마이그레이션 환경 구성

- **셔플 엔진**
  - [x] **[Task]** `app/core/shuffler.py`: `secrets` 기반 셔플 클래스 구현
  - [ ] **[Task]** 셔플 로직 단위 테스트 (`tests/test_shuffler.py`)

- **덱 서비스**
  - [x] **[Task]** `DeckService` 구현: 덱 생성 및 카드 뽑기 로직
  - [x] **[Task]** API 엔드포인트 연결 (`app/api/routers/readings.py`)

## 📌 Phase 3: AI 연동 (AI Integration)
- [x] **LangChain 설정**
  - [x] **[Task]** OpenAI/Gemini API 키 연동
  - [x] **[Task]** 시스템 프롬프트 템플릿 작성 (`app/core/prompts.py`)

- **해석 서비스**
  - [x] **[Task]** `InterpretationService` 구현: LLM 요청 및 응답 처리
  - [x] **[Task]** SSE(Server-Sent Events) 스트리밍 엔드포인트 구현

## 📌 Phase 4: 클라이언트 & UI (Client)
- [x] **설계 및 기획**
  - [x] **[Task]** 프론트엔드 UX/UI 상세 설계서 작성 (`Dev_md/10_Frontend_Design_and_UX.md`)

- **기능 구현 (v0.3)**
  - [ ] **[Task]** `static/app.js`: 상태 관리 리팩토링 (Class 기반 또는 모듈화)
  - [ ] **[Task]** `static/index.html`: 스프레드 선택 UI (<select>) 추가
  - [ ] **[Task]** `static/app.js`: 스프레드별 동적 슬롯 생성 로직 구현
  - [ ] **[Task]** `static/style.css`: 카드 드로우 및 뒤집기 애니메이션 고도화

- **기존 프로토타입 개선**
  - [x] **[Task]** `static/index.html`: 메인 페이지 및 구조
  - [x] **[Task]** `static/style.css`: 보라색 테마 및 카드 애니메이션
  - [x] **[Task]** `static/app.js`: API 연동 및 스트리밍 처리

## 📌 Phase 5: 배포 (Deployment)
- [ ] **Docker**
  - [ ] **[Task]** `Dockerfile` 작성 (Multi-stage build)
  - [ ] **[Task]** `docker-compose.yml` 작성 (App + DB)
