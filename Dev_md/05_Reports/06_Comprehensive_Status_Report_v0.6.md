# 📊 PyTarot Comprehensive Status Report (v0.6)

**Date:** 2026-01-07  
**Version:** v0.6 (Deployment Ready)  
**Status:** Stable / Deployed

---

## 1. 🌟 프로젝트 개요 (Project Overview)
**PyTarot**은 전통적인 타로 리딩 경험을 현대적인 웹 기술과 최첨단 AI 기술로 재해석한 프로젝트입니다.  
사용자에게 단순한 운세 텍스트를 던져주는 것이 아니라, **진정성 있는 셔플 경험**, **전문적인 타로 지식(RAG)**, 그리고 **몰입감 있는 스트리밍 해석**을 제공하는 것을 목표로 합니다.

---

## 2. 🔑 핵심 기능 및 기술 (Key Features & Core Technology)

### 2.1 🧠 AI & RAG (검색 증강 생성)
*   **Knowledge Base:** 78장 카드의 정방향/역방향 의미, 원소, 수비학적 상징을 포함한 마크다운 지식 베이스 구축.
*   **Vector Search:** `ChromaDB`와 `Google Generative AI Embeddings`를 활용한 시멘틱 검색.
*   **Context-Aware Interpretation:** 사용자 질문과 카드의 의미를 결합하여 LangChain 파이프라인이 문맥에 맞는 해석 생성.
*   **Real-time Streaming:** SSE(Server-Sent Events)를 통해 AI의 사고 과정을 실시간 타자기 효과로 전달.

### 2.2 🎲 True Randomness (진정성 있는 셔플)
*   **CSPRNG:** Python 표준 `random` 대신 암호학적으로 안전한 `secrets` 모듈 사용.
*   **Fisher-Yates Shuffle:** 검증된 알고리즘을 통해 편향 없는 덱 셔플링 구현.
*   **Deck Management:** 세션별 독립적인 덱 상태 관리 및 카드 소진 로직(Deck Exhaustion) 구현.

### 2.3 🏗️ Robust Architecture (아키텍처)
*   **Backend:** FastAPI (Async) 기반의 고성능 API 서버.
*   **Database:** PostgreSQL (Production) / SQLite (Dev) + SQLAlchemy ORM (Async).
*   **Deployment:** Docker & Docker Compose를 이용한 컨테이너 기반 배포 환경.
*   **Frontend:** Vanilla JS + CSS3 3D Transforms를 활용한 가볍고 화려한 UI (No heavy frameworks).

---

## 3. 📜 개발 히스토리 요약 (Development Log Summary)

### **Phase 1: Foundation (v0.1)**
*   프로젝트 구조 설계 및 환경 설정 (`venv`, `requirements.txt`).
*   기본 FastAPI 서버 및 SQLAlchemy 모델링 (`User`, `Reading`, `Card`).
*   `secrets` 기반 셔플러 프로토타입 구현.

### **Phase 2: Core Logic (v0.2)**
*   **데이터 구축:** 78장 타로 데이터 JSON화 및 DB 시딩 스크립트 작성.
*   **스프레드 엔진:** 원카드, 쓰리카드, 켈틱 크로스 등 다양한 배열법 설정(`spreads.json`) 및 로직 구현.
*   **안정성:** 로깅 시스템(`Loguru`) 및 전역 예외 처리 핸들러 도입.

### **Phase 3: AI Integration (v0.3 - v0.4)**
*   **LangChain 연동:** Google Gemini / OpenAI API 통합.
*   **프롬프트 엔지니어링:** 페르소나(신비로운 점술가) 설정 및 구조화된 출력 유도.
*   **스트리밍 API:** `text/event-stream` 프로토콜을 이용한 실시간 응답 구현.

### **Phase 4: Knowledge Enhancement (v0.5)**
*   **RAG 시스템 도입:** 타로 전문 지식 데이터셋(`data/knowledge/`) 구축 및 벡터 DB 연동.
*   **정확도 향상:** AI가 할루시네이션(거짓 정보) 없이 정확한 카드 상징을 인용하도록 개선.

### **Phase 5: Deployment (v0.6 - Current)**
*   **Containerization:** `Dockerfile` (Multi-stage build 최적화) 및 `docker-compose` 작성.
*   **Documentation:** 전체 개발 문서(`Dev_md/`) 구조화 및 리포트 정리.

---

## 4. 🚀 향후 계획 (Next Steps)
*   **v0.7 (User Accounts):** JWT 인증 및 사용자 이력 관리 시스템 도입.
*   **v0.8 (Advanced UI):** WebGL/Three.js를 활용한 더욱 화려한 3D 카드 효과.
*   **v1.0 (Official Launch):** CI/CD 파이프라인 구축 및 클라우드 배포.
