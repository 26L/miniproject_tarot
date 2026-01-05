# 🗺️ Development Roadmap: v0.3 (Next Steps)

## 🎯 목표
v0.2에서 완성된 백엔드 코어(DB, Spread, Logic)를 바탕으로, **사용자 경험(UX)을 개선하고 배포 가능한 형태**로 패키징합니다.

## 📅 주요 과제

### 1. 프론트엔드 고도화 (Frontend Enhancement)
*   **스프레드 선택 UI:** 사용자가 '원카드', '쓰리카드' 등을 선택할 수 있는 드롭다운/버튼 추가.
*   **인터랙션 개선:** 카드 드로우 시 시각적 효과 강화 (뒤집기 애니메이션 등).
*   **반응형 디자인:** 모바일 환경에서의 가독성 최적화.

### 2. Docker 컨테이너화 (Containerization)
*   **Dockerfile:** Python 3.11-slim 기반의 최적화된 이미지 빌드 스크립트 작성.
*   **docker-compose:** App + (Optional) PostgreSQL 구성을 한 번에 실행할 수 있는 설정 파일 작성.

### 3. 세션 영구 저장 (Session Persistence)
*   현재 메모리에 저장되는 세션 정보를 DB `readings` 테이블에 저장하도록 `DeckService` 로직 완전 이관.
*   `GET /api/history/{user_id}` 엔드포인트 구현.

## 🏁 마일스톤
*   **v0.3-alpha:** Docker 빌드 성공 및 로컬 실행 확인.
*   **v0.3-beta:** 프론트엔드 스프레드 선택 기능 연동 완료.
*   **v0.3-release:** 최종 통합 테스트 및 배포 가이드 작성.
