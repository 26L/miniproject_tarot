import os
import shutil
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from app.core.config import settings

# 벡터 DB 저장 경로
VECTOR_DB_PATH = "./app/core/vector_store"
KNOWLEDGE_PATH = "./data/knowledge"

class RAGService:
    def __init__(self):
        self._vector_db = None
        self._embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", # Gemini Embedding Model
            google_api_key=settings.GOOGLE_API_KEY
        )

    def get_db(self):
        """
        벡터 DB 인스턴스를 반환합니다. 로드되지 않았다면 로드합니다.
        """
        if self._vector_db is None:
            if os.path.exists(VECTOR_DB_PATH) and os.listdir(VECTOR_DB_PATH):
                self._vector_db = Chroma(
                    persist_directory=VECTOR_DB_PATH,
                    embedding_function=self._embeddings
                )
            else:
                # DB가 없으면 새로 구축
                print("Vector DB not found. Building new one...")
                self.build_vector_db()
        return self._vector_db

    def build_vector_db(self):
        """
        지식 데이터(Markdown)를 로드하여 벡터 DB를 구축(또는 재구축)합니다.
        """
        # 기존 DB 삭제 (Clean Rebuild)
        if os.path.exists(VECTOR_DB_PATH):
            shutil.rmtree(VECTOR_DB_PATH)

        # 1. 문서 로드
        if not os.path.exists(KNOWLEDGE_PATH):
            os.makedirs(KNOWLEDGE_PATH)
            return # 데이터가 없으면 빈 DB 생성 방지

        loader = DirectoryLoader(KNOWLEDGE_PATH, glob="**/*.md")
        docs = loader.load()
        
        if not docs:
            print("No documents found in knowledge path.")
            return

        # 2. 텍스트 분할 (Chunking)
        # 타로 카드 설명은 그리 길지 않으므로 청크 크기를 적절히 조절
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        # 3. 임베딩 및 저장
        self._vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self._embeddings,
            persist_directory=VECTOR_DB_PATH
        )
        print(f"Vector DB built successfully at {VECTOR_DB_PATH} with {len(chunks)} chunks.")

    def search(self, query: str, k: int = 3) -> List[Document]:
        """
        주어진 쿼리와 유사한 문서를 검색합니다.
        """
        db = self.get_db()
        if not db:
            return []
        
        # Similarity Search
        docs = db.similarity_search(query, k=k)
        return docs

rag_service = RAGService()
