# 🔮 PyTarot: AI 타로 리딩 플랫폼 (v0.2)

## 📖 프로젝트 소개
**PyTarot**은 최신 Python 트렌드를 반영하여 **FastAPI(백엔드)**와 **생성형 AI(LLM)**를 결합한 고도화된 타로 해석 서비스입니다. 
사용자가 질문을 입력하고 카드를 선택하면, `secrets` 모듈을 이용한 암호학적으로 안전한 셔플링을 통해 카드가 선정되며, LangChain 기반의 AI가 문맥을 고려한 깊이 있는 해석을 실시간으로 제공합니다.

## 🚀 주요 기능
*   **고품질 난수 생성:** `secrets` 모듈을 활용하여 예측 불가능하고 진정성 있는 셔플을 보장합니다.
*   **다양한 스프레드:** 원카드, 쓰리카드, 켈틱 크로스 등 다양한 배열법 지원 (v0.2+)
*   **AI 기반 심층 해석:** OpenAI/Gemini API와 LangChain을 연동하여, 단순 키워드 조합이 아닌 스토리텔링 기반의 상담을 제공합니다.
*   **실시간 스트리밍:** AI의 답변을 타자 치듯 실시간(SSE)으로 보여주어 사용자 몰입감을 극대화합니다.
*   **데이터베이스:** PostgreSQL (SQLAlchemy) 기반의 데이터 관리 및 초기화 기능 제공.

## 🛠️ 기술 스택
*   **Backend:** Python 3.11+, FastAPI, Uvicorn
*   **AI & LLM:** LangChain, OpenAI API / Google Gemini API
*   **Database:** PostgreSQL, SQLAlchemy (Async)
*   **Tools:** Docker, Pydantic V2

## 📦 설치 및 실행

1. **환경 설정**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **데이터베이스 초기화 (v0.2)**
   ```bash
   python scripts/seed_db.py
   ```

3. **서버 실행**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📂 폴더 구조
```
C:\tarot\
├── app/
│   ├── api/          # 엔드포인트 라우터
│   ├── core/         # 설정, 보안, 셔플 엔진
│   ├── services/     # 비즈니스 로직
│   ├── repositories/ # DB 접근 계층
│   ├── models/       # SQLAlchemy 모델
│   └── schemas/      # Pydantic 스키마
├── config/           # 스프레드 설정 등
├── Dev_md/           # 개발 문서 및 리포트 저장소
└── tests/            # 테스트 코드
```

## 📝 라이선스
MIT License
