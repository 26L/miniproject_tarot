# 📝 개발 일지 (Development Log)

## 2026-01-05
### ✅ v0.1 프로토타입 기능 검증 완료
- `scripts/test_full_flow.py`를 통해 셔플, 드로우, AI 해석(스트리밍) 파이프라인 무결성 확인.
- Windows 환경에서의 인코딩 이슈 해결 (시스템 로캘 문제, 데이터는 정상).

### 🚀 v0.2 업데이트 진행
- **데이터 보강:**
  - `config/spreads.json`: 원카드, 쓰리카드, 켈틱 크로스 등 표준 스프레드 정의.
  - `scripts/seed_db.py`: `data/tarot_cards.json` 데이터를 DB로 로드하는 스크립트 작성.
- **시스템 안정화:**
  - `app/core/logging_config.py`: Loguru/Standard Logging 기반의 로깅 시스템 구축 (File Rotation).
  - `app/main.py`: Global Exception Handler 추가로 안정성 확보.
- **문서 업데이트:**
  - `GEMINI.md` 및 `README.md` 버전 v0.2로 상향.
  - `05_TODO_list.md` 최신화.