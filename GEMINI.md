# 📂 현재 프로젝트 상태 (Current Status)
- **버전:** v0.2.1
- **날짜:** 2026년 1월 5일
- **진행 상황:** 
    - `v0.2.1` 백엔드 핵심 보강 완료 (DB 리포지토리, 스프레드 서비스).
    - `Dev_md/10_Frontend_Design_and_UX.md` 작성으로 프론트엔드 고도화(Phase 4) 준비 완료.
    - **버전 관리 규칙:** 버전 업데이트는 사용자의 명시적 요청 시 진행함.

### 생성된 폴더 구조
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