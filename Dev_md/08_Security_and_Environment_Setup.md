# 08. 보안 및 환경 설정 가이드 (Security & Environment Setup)

본 문서는 개발 및 배포 환경의 보안성을 확보하고, 일관된 설정을 유지하기 위한 가이드입니다.

## 1. 환경 변수 관리 (.env)

민감한 정보는 절대 코드에 하드코딩하지 않으며, `.env` 파일을 통해 관리합니다. `pydantic-settings`를 통해 타입을 검증하며 로드합니다.

### 1.1 `.env.example` 구조
```ini
# --- General ---
PROJECT_NAME="PyTarot"
DEBUG=True
API_V1_STR="/api/v1"

# --- Security ---
SECRET_KEY="changethis_to_a_secure_random_string"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# --- Database ---
# Local Docker or Cloud DB
POSTGRES_SERVER="localhost"
POSTGRES_USER="pytarot"
POSTGRES_PASSWORD="password"
POSTGRES_DB="pytarot_db"

# --- AI Service ---
OPENAI_API_KEY="sk-..."
# or
GOOGLE_API_KEY="AIza..."
```

## 2. 보안 가이드라인 (Security Guidelines)

### 2.1 API Key 관리
- `.env` 파일은 `.gitignore`에 반드시 포함되어야 합니다.
- CI/CD 파이프라인에서는 GitHub Actions Secrets 등을 통해 주입합니다.

### 2.2 의존성 관리
- `poetry.lock` 또는 `requirements.txt`에 해시값을 포함하여 공급망 공격을 방지합니다.
- 주기적으로 `pip-audit` 등을 통해 취약점 점검을 수행합니다.

### 2.3 CORS (Cross-Origin Resource Sharing)
- 개발 환경: `allow_origins=["*"]` (주의)
- 운영 환경: 구체적인 프론트엔드 도메인만 허용 (예: `https://pytarot.com`)

## 3. 개발 환경 셋업 (Dev Setup)

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 활성화 (Windows)
.\venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경변수 설정
copy .env.example .env
# .env 내용 수정
```
