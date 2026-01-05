# 06. 서비스별 세부 개발 설계서 (Service Detailed Design)

본 문서는 `app/services` 계층에 위치할 핵심 비즈니스 로직의 상세 설계를 정의합니다. 각 서비스는 **단일 책임 원칙(SRP)**을 준수하며, Repository 계층과 상호작용합니다.

---

## 1. 덱 서비스 (Deck Service)
**책임:** 타로 덱의 초기화, 셔플링, 카드 뽑기 상태 관리.

### 1.1 핵심 클래스 및 메서드
```python
class DeckService:
    def __init__(self, session_repo: ReadingSessionRepository, card_repo: TarotCardRepository):
        self.session_repo = session_repo
        self.card_repo = card_repo

    async def create_shuffled_session(self, user_id: Optional[UUID]) -> UUID:
        """
        1. 0~77까지의 정수 리스트 생성
        2. secrets 모듈을 사용한 Fisher-Yates 셔플 수행
        3. 셔플된 덱 상태를 Redis 또는 DB Session 테이블에 저장
        4. 세션 ID 반환
        """
        pass

    async def draw_cards(self, session_id: UUID, spread_type: str) -> List[CardSelectionDTO]:
        """
        1. session_id로 셔플된 덱 상태(남은 카드 리스트) 조회
        2. Spread 설정에서 필요한 카드 수(count) 확인
        3. 덱에서 count만큼 pop() (덱 상태 업데이트)
        4. 각 카드의 정/역방향(Reversed) 여부를 secrets.choice([True, False])로 결정
        5. 선택된 카드 정보를 DB(ReadingDetails)에 저장
        6. 카드 메타데이터(이미지, 이름 등)와 함께 반환
        """
        pass
```

### 1.2 주요 로직 상세
- **Shuffle Engine:** `app.core.shuffler.CryptographicShuffler`를 주입받아 사용.
- **State Management:** 세션별로 '남은 카드'와 '뽑힌 카드'의 순서를 정확히 추적해야 함 (중복 뽑기 방지).

---

## 2. 해석 서비스 (Interpretation Service)
**책임:** LLM(OpenAI/Gemini)과의 통신, 프롬프트 구성, 스트리밍 응답 처리.

### 2.1 핵심 클래스 및 메서드
```python
class InterpretationService:
    def __init__(self, llm_client: LangChainChatModel):
        self.llm = llm_client

    async def generate_interpretation_stream(
        self, 
        question: str, 
        cards: List[CardSelectionDTO], 
        spread_type: str
    ) -> AsyncGenerator[str, None]:
        """
        1. 카드 정보(이름, 위치, 정/역방향, 키워드)를 텍스트로 직렬화
        2. System Prompt에 '타로 리더 페르소나' 주입
        3. User Prompt에 질문 + 카드정보 + 스프레드 설명 결합
        4. LLM에 스트리밍 요청 전송
        5. 청크(Chunk) 단위로 yield 하여 SSE 포맷 지원
        """
        pass
```

### 2.2 프롬프트 전략
- **System Prompt:** "당신은 직관적이고 공감 능력이 뛰어난 타로 마스터입니다..."
- **Input Formatting:**
    - 카드: `[1] 과거: 바보(The Fool) - 정방향 (키워드: 시작, 모험)`
    - 질문: `이직을 해도 될까요?`
- **Output Constraints:** 마크다운 형식 사용 지양 (특수문자 최소화), 구어체 사용.

---

## 3. 사용자 서비스 (User Service)
**책임:** 회원 정보 관리 및 리딩 기록 조회.

### 3.1 핵심 클래스 및 메서드
```python
class UserService:
    async def get_reading_history(self, user_id: UUID, page: int, size: int) -> List[ReadingSummaryDTO]:
        """
        1. User ID로 Readings 테이블 조회 (Pagination)
        2. 각 Reading에 속한 첫 번째 카드 이미지(대표 이미지) 매핑
        3. 요약된 결과 반환
        """
        pass
```

---

## 4. 공통 모듈 (Core / Shared)
### 4.1 에러 핸들링
- `DeckEmptyError`: 덱에 남은 카드가 부족할 때 발생.
- `LLMConnectionError`: AI 서비스 연동 실패 시 발생 (재시도 로직 필요).

### 4.2 설정 (Configuration)
- `config/spreads.json`: 스프레드별 좌표 및 의미 정의 파일을 로드하여 `DeckService` 및 프론트엔드에 제공.
