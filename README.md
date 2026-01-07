# 🔮 PyTarot: AI-Powered Mystical Reading Platform

![Version](https://img.shields.io/badge/version-v0.6-blueviolet) ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white) ![RAG](https://img.shields.io/badge/AI-RAG%20Enhanced-orange) 

**PyTarot**은 현대적인 웹 기술과 생성형 AI, 그리고 신비주의적 전통을 결합한 차세대 타로 리딩 플랫폼입니다.
단순한 운세 뽑기를 넘어, **RAG(검색 증강 생성)** 기술을 통해 검증된 타로 지식을 바탕으로 AI가 심도 있는 해석을 제공합니다.

---

## ✨ Key Features (주요 기능)

### 🧠 1. RAG 기반 AI 해석 (Knowledge-Enhanced AI)
*   **Vector Database:** ChromaDB와 Google Embeddings를 활용하여 78장 카드의 상징, 원소, 수비학적 의미를 벡터화하여 저장했습니다.
*   **Context-Aware:** 사용자의 질문과 뽑은 카드의 맥락에 맞는 정확한 타로 지식을 실시간으로 검색하여 LLM에 주입합니다.
*   **Storytelling:** LangChain을 통해 단순 키워드 나열이 아닌, 내담자와 대화하듯 흐르는 스토리텔링 해석을 제공합니다.

### 🛡️ 2. 안전하고 공정한 셔플 (True Randomness)
*   Python의 `secrets` 모듈(CSPRNG)을 사용하여 예측 불가능한 카드 섞기를 구현했습니다. 이는 디지털 타로의 진정성을 보장하는 핵심 기술입니다.

### 🐳 3. 컨테이너화된 배포 (Docker Ready)
*   **Easy Setup:** `docker-compose` 명령어 하나로 백엔드(FastAPI)와 데이터베이스(PostgreSQL)를 즉시 실행할 수 있습니다.
*   **Microservices Ready:** 확장 가능한 아키텍처로 설계되었습니다.

### 🎨 4. 몰입형 UI/UX
*   **Mystical Atmosphere:** 반응형 다크 테마와 3D 카드 애니메이션(CSS3 Transforms)으로 신비로운 분위기를 연출합니다.
*   **Real-time Streaming:** AI의 해석이 생성되는 과정을 SSE(Server-Sent Events)를 통해 실시간 타자기 효과로 보여줍니다.

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

## 🏗️ System Architecture

### Project Structure
```
C:\tarot/
├── 🐳 docker-compose.yml     # 컨테이너 오케스트레이션
├── 🐳 Dockerfile             # 백엔드 이미지 빌드 설정
├── 📂 app/
│   ├── 📂 core/              # 핵심 모듈 (Config, DB, RAG, Shuffler)
│   ├── 📂 services/          # 비즈니스 로직 (Deck, Interpretation)
│   ├── 📂 api/               # FastAPI 라우터
│   └── 📂 models/            # SQLAlchemy 데이터 모델
├── 📂 data/
│   ├── 📂 knowledge/         # RAG용 타로 지식 베이스 (.md)
│   └── tarot_cards.json      # 원본 데이터
├── 📂 static/                # 프론트엔드 리소스 (HTML/CSS/JS)
└── 📂 Dev_md/                # 프로젝트 개발 문서 (Planning, Design, Reports)
```

## 📅 Status (개발 현황)

| Phase | Description | Status |
| :--- | :--- | :---: |
| **Phase 1** | 기초 프레임워크 및 데이터베이스 구축 | ✅ |
| **Phase 2** | 핵심 로직(셔플, 스프레드) 및 API 구현 | ✅ |
| **Phase 3** | LangChain 연동 및 AI 해석 엔진 구현 | ✅ |
| **Phase 4** | 프론트엔드 UI/UX 및 통합 테스트 | ✅ |
| **Phase 5** | **RAG 시스템 구축 (Knowledge Base)** | ✅ |
| **Phase 6** | **Docker 컨테이너화 및 배포 준비** | ✅ |

---

## 📝 License
This project is licensed under the MIT License.