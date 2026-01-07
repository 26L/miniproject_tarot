# 🔮 PyTarot: AI-Powered Mystical Reading Platform

![Version](https://img.shields.io/badge/version-v0.6-blueviolet) ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white) ![RAG](https://img.shields.io/badge/AI-RAG%20Enhanced-orange)

**PyTarot**은 현대적인 웹 기술과 생성형 AI, 그리고 신비주의적 전통을 결합한 차세대 타로 리딩 플랫폼입니다.
단순한 운세 뽑기를 넘어, **RAG(검색 증강 생성)** 기술을 통해 검증된 타로 지식을 바탕으로 AI가 심도 있는 해석을 제공합니다.

---

## 🔑 Key Features & Core Technology

### 🧠 1. AI & RAG (검색 증강 생성)
*   **Knowledge Base:** 78장 카드의 정방향/역방향 의미, 원소, 수비학적 상징을 포함한 마크다운 지식 베이스를 구축했습니다.
*   **Vector Search:** `ChromaDB`와 `Google Generative AI Embeddings`를 활용한 시멘틱 검색으로 질문에 가장 적합한 해석을 찾아냅니다.
*   **Context-Aware Interpretation:** 사용자 질문과 카드의 의미를 결합하여 LangChain 파이프라인이 문맥에 맞는 해석을 생성합니다.
*   **Real-time Streaming:** SSE(Server-Sent Events)를 통해 AI의 사고 과정을 실시간 타자기 효과로 전달하여 몰입감을 높입니다.

### 🎲 2. True Randomness (진정성 있는 셔플)
*   **CSPRNG:** Python 표준 `random` 대신 암호학적으로 안전한 `secrets` 모듈을 사용하여 예측 불가능한 결과를 보장합니다.
*   **Fisher-Yates Shuffle:** 검증된 알고리즘을 통해 편향 없는 덱 셔플링을 구현했습니다.
*   **Deck Management:** 세션별로 독립적인 덱 상태를 관리하며, 실제 카드 덱처럼 소진 로직(Deck Exhaustion)이 적용됩니다.

### 🏗️ 3. Robust Architecture (아키텍처)
*   **Backend:** FastAPI (Async) 기반의 고성능 API 서버로 구축되었습니다.
*   **Database:** PostgreSQL (Production) 및 SQLite (Dev)를 지원하며 SQLAlchemy ORM (Async)을 사용합니다.
*   **Deployment:** Docker & Docker Compose를 이용한 컨테이너 기반 배포 환경을 완벽하게 지원합니다.
*   **Frontend:** 무거운 프레임워크 없이 Vanilla JS와 CSS3 3D Transforms만으로 가볍고 화려한 UI를 구현했습니다.

---

## 📜 Development History (개발 일지 요약)

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

## 🚀 Quick Start (빠른 시작)

### Option A: Docker (권장)
가장 간편한 실행 방법입니다. Docker가 설치되어 있어야 합니다.

```bash
# 1. 저장소 클론
git clone https://github.com/your-repo/pytarot.git
cd pytarot

# 2. 환경 변수 설정 (.env 파일 생성)
# .env.example을 참고하여 API 키 설정
cp .env.example .env

# 3. 서비스 실행
docker-compose up --build
```
서비스는 `http://localhost:8000` 에서 접속 가능합니다.

### Option B: Local Development
Python 환경에서 직접 실행합니다.

```bash
# 1. 가상환경 생성 및 패키지 설치
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# 2. 데이터베이스 및 지식 베이스 초기화
python scripts/seed_db.py

# 3. 서버 실행
uvicorn app.main:app --reload
```

---

## 📝 License
This project is licensed under the MIT License.
