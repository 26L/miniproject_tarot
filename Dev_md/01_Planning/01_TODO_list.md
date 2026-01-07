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

## 📌 Phase 2: 코어 보강 (Core Enhancement - v0.2/v0.3)
- **백엔드 고도화**
  - [x] **[Task]** 스프레드 서비스 (`SpreadService`) 구현
  - [x] **[Task]** API 통합 및 최적화 (`POST /readings`로 통합)
  - [x] **[Task]** 선(先)드로우(Pre-draw) 전략 적용

## 📌 Phase 4: 클라이언트 & UI (Frontend - v0.3)
- **설계 및 가이드**
  - [x] **[Task]** 프론트엔드 UX/UI 상세 설계서 (`Dev_md/10_Frontend_Design_and_UX.md`)
  - [x] **[Task]** 프론트엔드 구현 상세 계획서 (`Dev_md/11_Frontend_Implementation_Plan.md`)
  - [x] **[Task]** 프론트엔드 개발 가이드라인 (`Dev_md/12_Frontend_Development_Guidelines.md`)
  - [x] **[Task]** API 연동 및 컴포넌트 명세서 (`Dev_md/14_Frontend_Detailed_Specs.md`)
  - [x] **[Task]** UI 시각적 제약 및 이미지 핸들링 가이드 (`Dev_md/17_UI_Visual_Constraints_and_Image_Handling.md`)

- **UI 구현**
  - [x] **[Task]** `static/index.html`: SPA 방식의 단계별(Step-by-Step) 구조 재설계
  - [ ] **[Task]** `static/style.css`: Mystical Dark 테마 및 3D 카드 애니메이션 구현
  - [ ] **[Task]** `static/style.css`: 반응형 레이아웃 (모바일/데스크탑) 최적화

- **로직 및 인터랙션**
  - [ ] **[Task]** `static/app.js`: 신규 API(`POST /readings`) 연동 및 상태 관리 구현
  - [ ] **[Task]** `static/app.js`: 카드 셔플, 드로우(이동), 뒤집기 시각적 연출 로직
  - [ ] **[Task]** `static/app.js`: AI 해석 스트리밍 수신 및 타자기 효과 구현

- **검증**
  - [ ] **[Task]** 프론트엔드-백엔드 전체 흐름 통합 테스트

## 📌 Phase 4.5: UX 고도화 (UX Enhancement - v0.4)
- **인터랙션 업그레이드**
  - [x] **[Task]** 부채꼴(Fan-out) 카드 선택 인터페이스 구현 (JS 동적 각도 계산)
  - [x] **[Task]** 모바일 환경 대응 카드 슬라이더/스크롤 UI

## 📌 Phase 4.6: 검증 및 테스트 자동화 (Verification & Automation)
- **테스트 구축**
  - [x] **[Task]** 통합 테스트 자동화 가이드 작성 (`Dev_md/21_Integration_Testing_Guide.md`)
  - [x] **[Task]** API 통합 테스트 코드 구현 (`tests/integration/test_api_flow.py`)
  - [x] **[Task]** 전체 테스트 스위트 실행 및 검증 (Result: PASSED)

- **보고서**
  - [x] **[Task]** 개발 평가 및 감리 보고서 작성 (`Dev_md/22_Evaluation_and_Audit_Report_v0.4.md`)
  - [x] **[Task]** 보고서 작성 표준 가이드 작성 (`Dev_md/23_Report_Writing_Guide.md`)

## 📌 Phase 5.5: RAG 시스템 도입 (AI Enhancement - v0.5)
- **기반 구축**
  - [x] **[Task]** RAG 기술 설계 및 구현 명세서 작성 (`Dev_md/02_Design/11_Technical_Design_RAG.md`)
  - [x] **[Task]** 필요 패키지(`chromadb` 등) 설치 및 `requirements.txt` 업데이트
  - [x] **[Task]** `app/core/rag.py`: 벡터 DB 초기화 및 검색 로직 구현
  - [x] **[Task]** `data/knowledge/`: 타로 지식 데이터셋 구축 (78건 완료)
  - [x] **[Task]** `app/services/interpretation_service.py`: RAG 검색 결과 프롬프트 주입 로직 구현

## 📌 Phase 6: 배포 (Deployment - Next Step)
- **Docker**

## 📌 Phase 5: 배포 (Deployment)
- [x] **Docker**
  - [x] **[Task]** `Dockerfile` 작성 (Multi-stage build)
  - [x] **[Task]** `docker-compose.yml` 작성 (App + DB)
