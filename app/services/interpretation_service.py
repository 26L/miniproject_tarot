from typing import List, AsyncGenerator
from app.core.llm import get_llm_model
from app.core.prompts import get_interpretation_prompt
from app.schemas.schemas import CardDrawResult
from app.core.rag import rag_service
from langchain_core.output_parsers import StrOutputParser

class InterpretationService:
    def __init__(self):
        self.llm = get_llm_model()
        self.prompt = get_interpretation_prompt()
        self.parser = StrOutputParser()

    def format_card_data(self, cards: List[CardDrawResult]) -> str:
        """Formats the list of cards into a readable string for the LLM."""
        formatted = []
        for card in cards:
            orientation = "역방향(Reversed)" if card.is_reversed else "정방향(Upright)"
            formatted.append(
                f"- 위치 {card.position_index + 1} ({card.position_meaning}): {card.name_kr} ({card.name_en}) [{orientation}]\n"
                f"  * 키워드: {', '.join(card.keywords['reversed'] if card.is_reversed else card.keywords['upright'])}\n"
                f"  * 설명: {card.description[:50]}..."
            )
        return "\n".join(formatted)

    def _get_rag_context(self, question: str, cards: List[CardDrawResult]) -> str:
        """Retrieves relevant knowledge from RAG service."""
        try:
            # 검색 쿼리 생성: 질문 + 주요 카드 이름
            card_names = " ".join([c.name_kr for c in cards])
            query = f"{question} {card_names}"
            
            docs = rag_service.search(query, k=3)
            if not docs:
                return "관련된 상세 지식 정보를 찾을 수 없습니다."
            
            return "\n\n".join([d.page_content for d in docs])
        except Exception as e:
            print(f"RAG Search Error: {e}")
            return "지식 베이스 검색 중 오류가 발생하여 기본 지식으로 해석합니다."

    async def stream_interpretation(self, question: str, spread_type: str, cards: List[CardDrawResult]) -> AsyncGenerator[str, None]:
        """
        Generates a streaming tarot reading using the LLM with RAG context.
        """
        if not self.llm:
            yield "시스템 오류: AI 모델이 설정되지 않았습니다."
            return

        card_text = self.format_card_data(cards)
        rag_context = self._get_rag_context(question, cards)
        
        chain = self.prompt | self.llm | self.parser
        
        async for chunk in chain.astream({
            "question": question,
            "spread_type": spread_type,
            "card_data": card_text,
            "context": rag_context
        }):
            yield chunk

interpretation_service = InterpretationService()
