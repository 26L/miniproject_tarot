# 08. 보안 및 환경 설정 (Security & Environment Setup)

## 1. 환경 변수 관리 (.env)
민감한 정보는 반드시 `.env` 파일로 관리하며, 저장소에는 `.env.example`만 커밋합니다.

### 필수 변수
*   `GOOGLE_API_KEY` 또는 `OPENAI_API_KEY`: LLM 사용을 위한 키.
*   `SECRET_KEY`: JWT 토큰 생성 및 세션 암호화 키.
*   `POSTGRES_SERVER`, `POSTGRES_USER`... : DB 연결 정보 (옵션).

## 2. 데이터베이스 설정 (v0.2 Updated)
본 프로젝트는 **Hybrid Database Strategy**를 채택하고 있습니다.

### 2.1 개발 및 로컬 환경 (SQLite)
*   별도의 설치 없이 `aiosqlite`를 통해 `tarot.db` 파일로 즉시 실행 가능합니다.
*   `POSTGRES_SERVER` 설정이 없거나 실패 시 자동으로 SQLite로 전환됩니다.

### 2.2 운영 환경 (PostgreSQL)
*   `.env`에 PostgreSQL 접속 정보를 입력하면 `asyncpg` 드라이버를 통해 고성능 비동기 연결을 맺습니다.

### 2.3 초기화 명령
```bash
# DB 테이블 생성 및 카드 데이터 주입
python scripts/seed_db.py
```

## 3. 보안 가이드라인
*   **API Key:** 클라이언트(브라우저)에 노출되지 않도록 서버 사이드에서만 사용합니다.
*   **Shuffle:** Python의 기본 `random` 모듈 대신 암호학적으로 안전한 `secrets` 모듈을 사용합니다.
*   **Error Handling:** 프로덕션 모드(`DEBUG=False`)에서는 상세 에러 스택 트레이스를 노출하지 않습니다.