# 📂 현재 프로젝트 상태 (Current Status)
- **버전:** v0.5 (AI Intelligence)
- **날짜:** 2026년 1월 6일
- **진행 상황:** 
    - `v0.5` RAG(검색 증강 생성) 시스템 구축 완료.
    - **Knowledge Base:** 타로 카드 78장에 대한 상세 지식 데이터셋 구축 (`data/knowledge/`).
    - **Vector Search:** ChromaDB + Google Embeddings 기반의 유사도 검색 엔진 탑재.
    - **Context-Aware:** AI가 전문 지식을 참조하여 해석하도록 프롬프트 파이프라인 고도화.
    - **문서화:** `Dev_md/` 폴더 구조화 및 RAG 구현 보고서 작성 완료.

### 생성된 폴더 구조
```
C:\tarot/
├── app/
│   ├── core/
│   │   ├── rag.py        # RAG 엔진
│   │   └── vector_store/ # 벡터 DB 저장소
│   └── services/         # InterpretationService (RAG 통합)
├── data/
│   └── knowledge/        # Markdown 지식 데이터 (78건)
├── Dev_md/               # 개발 문서 (5개 카테고리로 분류됨)
│   ├── 01_Planning/
│   ├── 02_Design/
│   ├── 03_Standards/
│   ├── 04_Test_QA/
│   └── 05_Reports/
└── ...
```