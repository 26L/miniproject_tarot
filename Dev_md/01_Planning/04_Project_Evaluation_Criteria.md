# 02. 프로젝트 평가 기준 (Project Evaluation Criteria)

## 1. 완성도 평가 (Completeness Metrics)

프로젝트의 완성도는 다음 항목들을 기준으로 정량적 및 정성적으로 평가합니다.

### 1.1 기능적 완성도 (Functional Completeness)
| 항목 | 가중치 | 평가 기준 (Definition of Done) |
|:---:|:---:|:---|
| **기본 API** | 20% | CRUD 기능 정상 동작, 올바른 상태 코드 반환 |
| **셔플 엔진** | 20% | `secrets` 기반 셔플 검증, 엔트로피(무작위성) 확보 |
| **AI 연동** | 25% | LangChain 파이프라인 동작, 프롬프트 응답 품질, 스트리밍(SSE) 구현 |
| **DB 설계** | 15% | 정규화된 스키마, 관계 설정, 마이그레이션 파일 존재 |
| **예외 처리** | 10% | 예상된 에러(404, 400, 500)에 대한 우아한 처리 |
| **문서화** | 10% | Swagger UI(OAS) 정상 출력, README 최신화 |

### 1.2 코드 품질 (Code Quality)
- **Lint Score:** Pylint/Ruff 기준 9.0/10.0 이상.
- **Type Check:** `mypy` 검사 시 오류 0건.
- **Test Coverage:** 핵심 로직(Service Layer) 단위 테스트 커버리지 80% 이상 권장.

---

## 2. 진척률 산정 방식 (Progress Tracking)

진척률은 개발 로드맵 단계별 가중치를 적용하여 산출합니다.

- **Phase 1 (기반 구축):** 15%
- **Phase 2 (코어 로직 - 셔플/스프레드):** 25%
- **Phase 3 (AI 연동 - LLM/스트리밍):** 30%
- **Phase 4 (클라이언트/UI):** 20%
- **Phase 5 (배포/인프라):** 10%

---

## 3. 자체 검수 체크리스트 (Self-Check List)

- [ ] **Secret Keys:** API Key 등 민감 정보가 코드에 하드코딩되지 않았는가? (`.env` 사용)
- [ ] **Async:** DB 및 외부 API 호출이 비동기(`await`)로 처리되었는가?
- [ ] **Response:** API 응답 포맷이 일관성(JSON)을 유지하는가?
- [ ] **Dependencies:** 불필요한 라이브러리가 포함되지 않았는가?
