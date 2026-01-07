# 24. RAG 기반 타로 해석 시스템 기술 설계 및 구현 명세서

## 1. 개요 (Overview)
본 문서는 단순 LLM 의존도를 낮추고, 타로 해석의 깊이와 정확성을 높이기 위해 **RAG (Retrieval-Augmented Generation, 검색 증강 생성)** 기술을 도입하는 설계서입니다.

### 1.1 목표
*   **전문성 강화:** AI가 일반적인 지식이 아닌, 검증된 타로 서적이나 전문 데이터베이스의 내용을 근거로 해석하게 합니다.
*   **환각(Hallucination) 감소:** 근거 없는 내용을 지어내는 현상을 줄이고, 신뢰할 수 있는 해석을 제공합니다.

## 2. 기술 아키텍처 (Technical Architecture)

### 2.1 구성 요소
1.  **Knowledge Base (지식 저장소):**
    *   타로 카드 78장에 대한 정방향/역방향 상세 의미, 상징, 조합 해석(Combination) 데이터.
    *   형식: 텍스트 파일(.txt, .md) 또는 JSON.
2.  **Embeddings Model:**
    *   텍스트를 벡터(숫자 배열)로 변환하는 모델.
    *   추천: `OpenAI text-embedding-3-small` 또는 `HuggingFace (ko-sbert)` (한국어 특화).
3.  **Vector Database (벡터 DB):**
    *   임베딩된 벡터 데이터를 저장하고 유사도 검색을 수행하는 DB.
    *   선정: **ChromaDB** (로컬 파일 기반, 설정 간편, Python 친화적).
4.  **Retrieval Chain:**
    *   사용자 질문 + 뽑힌 카드 키워드로 DB를 검색(Retrieval)하고, 찾은 관련 지식을 프롬프트에 주입(Augmentation)하여 LLM에 전달(Generation)하는 파이프라인.

### 2.2 데이터 흐름 (Data Flow)
1.  **Ingestion (구축):** 타로 지식 데이터 -> 청킹(Chunking) -> 임베딩 -> ChromaDB 저장.
2.  **Query (조회):**
    *   Input: "연애운인데 바보(The Fool) 카드가 나왔어."
    *   Search: DB에서 'The Fool 연애운', 'The Fool 정방향' 관련 텍스트 검색.
    *   Prompting: 검색된 텍스트를 `Context`로 프롬프트에 삽입.
    *   Answer: LLM이 Context를 바탕으로 답변 생성.

## 3. 구현 명세 (Implementation Specs)

### 3.1 필요 라이브러리
```bash
pip install langchain-chroma chromadb
```

### 3.2 디렉토리 구조
```
app/
├── core/
│   ├── rag.py          # RAG 로직 (DB 로드, 검색기 생성)
│   └── vector_store/   # ChromaDB 데이터 저장 폴더
├── services/
│   └── knowledge_service.py # 지식 데이터 관리
data/
└── knowledge/          # 원본 텍스트 데이터 (예: fool.md, magician.md)
```

### 3.3 핵심 모듈 설계 및 구현 (`app/core/rag.py`)

#### A. RAGService 클래스
*   **역할:** 벡터 DB의 생성, 로드, 검색을 담당하는 싱글톤 서비스.
*   **Embeddings:** `GoogleGenerativeAIEmbeddings` (models/embedding-001) 사용.
*   **Vector Store:** `Chroma` (Persist Directory: `./app/core/vector_store`)

```python
class RAGService:
    def build_vector_db(self):
        # 1. 기존 DB 삭제 (Clean Build)
        # 2. data/knowledge/*.md 로드
        # 3. 텍스트 청킹 (Chunk Size: 1000)
        # 4. 임베딩 및 ChromaDB 저장
    
    def search(self, query: str, k: int = 3):
        # 유사도 검색 수행
```

#### B. 데이터 갱신 절차 (Data Update Workflow)
지식 데이터가 수정되거나 추가되었을 때 시스템에 반영하는 순서입니다.
1.  **데이터 수정:** `data/tarot_cards.json` 수정 후 `scripts/generate_knowledge_base.py` 실행 (또는 `data/knowledge/`의 md 파일 직접 수정).
2.  **DB 재구축:** 앱 재시작 시 자동으로 기존 DB가 없으면 생성되며, 강제 갱신이 필요한 경우 `rag_service.build_vector_db()`를 호출하는 관리자용 API 또는 스크립트 실행이 필요함.

## 4. 데이터셋 구축 계획

## 4. 데이터셋 구축 계획
*   초기에는 `data/tarot_cards.json`에 있는 `description`과 `keywords`를 텍스트 문서로 변환하여 기본 지식으로 활용합니다.
*   추후 상세한 해석 텍스트 파일을 추가하면 별도 코드 수정 없이 지식이 확장됩니다.

## 5. 기대 효과
*   해석의 일관성 유지.
*   단순 키워드 나열을 넘어선 깊이 있는 문맥 제공 가능.
