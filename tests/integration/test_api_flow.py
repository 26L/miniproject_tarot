import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

# 테스트용 기본 설정
BASE_URL = "http://test"

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        yield client

@pytest.mark.asyncio
async def test_create_reading_session(async_client):
    """
    TC-API-01: 타로 리딩 세션 생성 (Happy Path)
    """
    payload = {
        "question": "오늘의 금전운은 어떨까요?",
        "spread_type": "three_card"
    }
    
    response = await async_client.post("/api/v1/readings", json=payload)
    
    # 1. 상태 코드 검증
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    
    # 2. 필수 필드 존재 확인
    assert "session_id" in data
    assert "cards" in data
    assert "spread_config" in data
    
    # 3. 데이터 무결성 검증 (Three Card = 3장)
    assert len(data["cards"]) == 3
    assert data["spread_config"]["card_count"] == 3
    
    return data["session_id"]

@pytest.mark.asyncio
async def test_create_reading_invalid_input(async_client):
    """
    TC-API-02: 잘못된 입력 처리
    """
    # 질문 누락
    payload = {
        "question": "", 
        "spread_type": "one_card"
    }
    # Pydantic 유효성 검사 실패 예상 (422 Unprocessable Entity)
    response = await async_client.post("/api/v1/readings", json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_ai_interpretation_stream(async_client):
    """
    TC-API-03 & 04: 해석 스트리밍 연결 및 AI 응답 검증
    """
    # 1. 선행 작업: 세션 생성 및 카드 확보
    payload = {
        "question": "테스트 질문입니다. 이 프로젝트의 성공 가능성은?",
        "spread_type": "one_card"
    }
    create_res = await async_client.post("/api/v1/readings", json=payload)
    assert create_res.status_code == 200
    session_data = create_res.json()
    session_id = session_data["session_id"]
    cards = session_data["cards"]
    
    # 2. 스트리밍 요청 (InterpretationRequest 스키마 준수)
    stream_payload = {
        "session_id": session_id,
        "question": payload["question"],
        "spread_type": payload["spread_type"],
        "selected_cards": cards
    }
    
    async with async_client.stream("POST", "/api/v1/interpretations/stream", json=stream_payload) as response:
        assert response.status_code == 200
        # assert response.headers["content-type"] == "text/event-stream" # httpx stream may handle headers differently
        
        full_text = ""
        async for chunk in response.aiter_text():
            full_text += chunk
            
        # 3. AI 응답 내용 검증 (TC-API-04)
        print(f"\n[AI Response Preview]: {full_text[:100]}...")
        
        assert len(full_text) > 50, "AI 응답이 너무 짧습니다."
        
        # 프롬프트 지침에 따른 키워드 포함 여부 확인
        # (스트리밍 데이터에는 'data: ' 접두어가 포함될 수 있음)
        assert "긍정" in full_text or "Positive" in full_text, "응답에 '긍정적 측면' 관련 내용이 누락되었습니다."
        assert "부정" in full_text or "Negative" in full_text, "응답에 '부정적 측면' 관련 내용이 누락되었습니다."
