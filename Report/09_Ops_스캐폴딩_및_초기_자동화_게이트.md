# 4x4 Magic Square — Ops 스캐폴딩 및 초기 자동화 게이트 도입 보고서

> 본 문서는 `docs/PRD.md` §13에서 *paper로 정의된* Ops Track을 **작동 가능한 형태로 환원**한 첫 사이클의 결정·산출·검증을 기록한다.
> 산출물 자체는 워크스페이스 루트와 `src/` / `tests/` / `.github/` / `docs/` 트리에 분포한 **13개 파일**이며, 본 보고서는 그 파일 집합에 도달하기까지의 *어떤 게이트를 어떤 도구로 어떤 임계로 강제했는가*를 외부화한다.
> 본 단계는 **TDD 출발점 직전(Pre-RED 상태)을 결정적으로 고정한 단계**다. 프로덕션 코드 0줄, 테스트 0건은 *결함이 아니라 의도다*.

---

## 문서 메타데이터

| 항목 | 내용 |
|---|---|
| 문서 ID | `09_Ops_스캐폴딩_및_초기_자동화_게이트` |
| 단계 | Ops 스캐폴딩 (§13.1 G→GP→GR 사이클의 첫 G) |
| 선행 문서 | `08_PRD_보강_및_Dual_Track_Ops_통합`, `docs/PRD.md`(756줄), `.cursorrules`(265줄) |
| 후행 단계 | 첫 RED 테스트 작성 (DT-1 — `T-U-001` + `T-D-001` 한 쌍) |
| 산출물 | 13개 파일 (§3에 라인 단위 표) |
| 산출물 형식 | TOML / YAML / Python(빈 패키지) / Markdown |
| 학습 초점 | *외부 강제력 도입의 결정적 운영* / *TDD 원칙과 자동화 도구의 충돌 지점 명시 처리* / *"paper-only를 작동으로" 환원의 정직성* |

---

## 0. 본 단계의 위치와 책무

### 0.1 직전 상태

| 항목 | 상태 |
|---|---|
| `docs/PRD.md` §13 (Ops & Automation) | ✅ paper로 정의됨 (OG-1 ~ OG-14, OPS-1 ~ OPS-5, OO-1 ~ OO-5) |
| `.cursorrules` `file_structure.tree` | ✅ 디렉토리 구조 정의됨 |
| 워크스페이스 실제 파일 | ❌ `.cursorrules` + `docs/PRD.md` + 7개 `Report/*.md` *외에는 0개* |
| `pyproject.toml` / `.pre-commit-config.yaml` / `.github/workflows/ci.yml` | ❌ 부재 |
| `src/` / `tests/` 디렉토리 | ❌ 부재 |

→ **§13의 모든 약속이 paper-only 상태**. PR이 발생해도 차단할 수단이 없음.

### 0.2 본 단계의 트리거

`08_PRD_보강` 보고서 §6 *후행 단계 부과 제약*:
> *"`09_Ops_스캐폴딩_및_초기_자동화_게이트`: OG-1 ~ OG-14의 작동 가능한 형태 셋업이 본 단계의 paper-only 상태를 닫는 책임을 갖는다."*

사용자 위임:
> *"더 좋은 쪽으로 잘 판단해서 해줘"* → 3개 옵션(A: Pre-RED Gate 박제 / B: Ops 스캐폴딩 / C: 행렬 확정) 중 **B 채택**. 근거는 `08` 보고서 §1 CYCLE 7.

### 0.3 본 단계가 *해야 하는 것*

- `.cursorrules` `file_structure.tree`를 *물리적으로* 만든다.
- §13.2 OG-1 ~ OG-3 (Stage 1 Static)을 *로컬 + CI 양쪽에서* 자동 실행되게 한다.
- §13.2 OG-4 ~ OG-14는 *슬롯을 명시*하여 후속 PR에서 *별도 PR(OPS-3)*로 단계 도입한다.
- 모든 결정의 *임계값 / 도구 / 보호 대상* 매핑을 외부화한다.
- TDD 원칙(첫 RED → 첫 GREEN)을 *어기지 않는다* — 즉 프로덕션 코드 0줄, 테스트 0건 상태로 끝낸다.

### 0.4 본 단계가 *하지 않는 것*

- 프로덕션 코드 작성 — *첫 RED 테스트가 요구하기 전에는* `boundary/` `control/` `entity/` 모두 `__init__.py`만 둔다.
- 테스트 코드 작성 — TDD 원칙. 첫 RED는 *후행 단계에서 작성*.
- 도메인 상수 모듈(`constants.py`) 사전 작성 — 첫 RED가 *명시적으로 import 요구*할 때 추가 (TDD 원칙 + REG-4 단정 약화 금지의 정신).
- OG-9(import-linter) / OG-11(Hypothesis) / OG-12(커스텀 스크립트) / OG-13(혼합 커밋 검사기)의 *실제 활성화* — `pyproject.toml`의 `[opt-strict]` 슬롯과 CI yaml의 *주석 슬롯*만 둔다.

---

## 1. 작업 진행 단계 (Step-by-Step)

### STEP 1 — 현재 상태 검증

| 항목 | 결과 |
|---|---|
| 워크스페이스 루트 스캔 (`Get-ChildItem -Force`) | `.git`, `docs/`, `Prompt/`, `Report/`, `.cursorrules` — *5개 항목만 존재* |
| Glob `**/*.{py,toml,yaml,yml,cfg,ini}` | **0개** — Python 자산 0건 확인 |
| 결정 | *완전한 빈 슬레이트*. PRD §13.2를 그대로 도구로 환원 가능. |

### STEP 2 — 루트 설정 파일 3종 생성

| 파일 | 책임 | 라인 수 |
|---|---|---|
| `.gitignore` | Python/IDE/캐시 표준 + Pytest/Coverage/Mypy/Ruff 캐시 | ~40 |
| `pyproject.toml` | Black/Ruff/mypy/pytest/pytest-cov 단일 진실 출처 (PRD §13.2 OG-1 ~ OG-6 직접 매핑) | ~120 |
| `README.md` | 3-Track 구조 + 빠른 시작 + 게이트 카탈로그 + TDD 출발점 안내 | ~110 |

### STEP 3 — 로컬 게이트 (.pre-commit-config.yaml)

| Gate | Hook | 보호 |
|---|---|---|
| OG-1 | `psf/black` (rev 24.10.0, py3.10) | 코드 포맷 |
| OG-2 | `astral-sh/ruff-pre-commit` (rev v0.7.4, `--fix --exit-non-zero-on-fix`) | NFR-06 매직 넘버 (PLR2004) + PEP 8 + pyflakes + isort + naming + bugbear + simplify |
| OG-2' | `ruff-format --check` | 포맷 일관성 |
| OG-3 | `pre-commit/mirrors-mypy` (v1.13.0, `--config-file=pyproject.toml`, `files: ^src/`) | 타입 안전성 (`.cursorrules` `type_hints.enforcement`) |
| (위생) | `pre-commit/pre-commit-hooks` (v5.0.0): trailing-whitespace, EOF, check-yaml, check-toml, check-added-large-files (500KB), check-merge-conflict | 부수 효과 차단 |

### STEP 4 — CI 워크플로 (.github/workflows/ci.yml)

5-Stage 파이프라인을 *순서대로* 명시.

| Stage | 활성 게이트 | 비활성 사유 / 미래 활성화 조건 |
|---|---|---|
| **1: Static** | OG-1 (`black --check`), OG-2 (`ruff check`, `ruff format --check`), OG-3 (`mypy src`) | (전부 활성) |
| **2: Test** | OG-4 + OG-5 + OG-6 (`pytest`) — *exit code 5 한시 허용* | 테스트 0건 상태 한시 허용. 첫 RED 커밋 PR에서 우회 *제거 의무* (OPS-4 정신). |
| **3: Invariant** | (슬롯) OG-7 / OG-8 / OG-10 / OG-11 | OG-7/8/10은 전용 RED 테스트가 작성된 시점부터 OG-4 안에서 자동 실행됨. OG-11은 Hypothesis 도입 PR(별도) 후 활성화. |
| **4: Architecture** | (슬롯) OG-9 / OG-12 / OG-13 | import-linter 도입 PR + 커스텀 스크립트 작성 PR 후 활성화 (OPS-3 별도 PR). |
| **5: Performance** | (슬롯) OG-14 | pytest-benchmark 도입 + FR-05 첫 GREEN 후 활성화. NFR-05에 따라 차단성은 *참고용*. |

> CI는 Ubuntu 단일 매트릭스 + Python 3.10 핀 (`docs/PRD.md` §11.3 OR-4 대응 — 환경 차이로 인한 비결정 회귀 방지).

### STEP 5 — ECB 패키지 미러링 (`src/magicsquare/`)

| 파일 | 내용 |
|---|---|
| `src/magicsquare/__init__.py` | 패키지 docstring + `__version__ = "0.1.0"` |
| `src/magicsquare/boundary/__init__.py` | Track A 책임 영역 docstring (T-U-* 안내, DIP/A-3 명시) |
| `src/magicsquare/control/__init__.py` | 흐름 제어 docstring (BR-17 / NFR-09 명시) |
| `src/magicsquare/entity/__init__.py` | I1~I5 + 도메인 상수 단일 진실 출처 안내 (T-D-*, T-INV-* 매핑) |

### STEP 6 — 테스트 디렉토리 미러링 (`tests/`)

| 파일 | 내용 |
|---|---|
| `tests/__init__.py` | 명명 규약 + Test ID prefix 안내 (`T-U-*`, `T-D-*`, `T-INV-*`, `TC-*`, `P-*`) |
| `tests/conftest.py` | "공통 fixture 0개 — 첫 RED가 요구할 때 추가" 명시 (`.cursorrules` `testing.fixture_scope` 인용) |
| `tests/boundary/__init__.py` | Track A 핵심 원칙 (DT-4) 안내 |
| `tests/control/__init__.py` | Track B 흐름 제어 단위 안내 |
| `tests/entity/__init__.py` | Track B 컴포넌트 단위 + 불변조건 안내 |

### STEP 7 — 검증

| 검증 항목 | 결과 |
|---|---|
| ReadLints (`pyproject.toml` + `.pre-commit-config.yaml` + `.github/workflows/ci.yml` + `src/` + `tests/` + `README.md`) | **0건** |
| 파일 구조 ↔ `.cursorrules` `file_structure.tree` 일치 | **1:1 일치** (`.gitignore` 1개만 추가 — 트리에 없는 표준 파일) |
| 모든 신규 파일의 인코딩/줄바꿈 | UTF-8 / LF (cross-platform) |

---

## 2. 외부화된 결정 (Decision Log)

> 본 절은 본 단계에서 발생한 *합의된 결정*을 OD-1 ~ OD-9로 외부화한다.

| ID | 결정 | 근거 | 후행 단계 영향 |
|---|---|---|---|
| **OD-1** | 프로덕션 코드 0줄, 테스트 0건 상태로 본 단계를 *닫는다*. | TDD 원칙 — 첫 RED가 *명시적으로 요구*하기 전에는 어떤 모듈도 사전 생성하지 않는다. `08` 보고서 §6의 후행 단계 부과 제약. | 다음 커밋은 *반드시* 첫 RED 테스트가 된다 (DT-1). |
| **OD-2** | `--cov-fail-under=0` (초기) — Domain 95%/Boundary 85% 임계는 *상향* 시점에 PR로 도입한다. | 테스트 0건 상태에서 95/85 임계는 *기능 차단*이 됨. *0은 약화가 아닌 미설정 상태*임을 README + pyproject.toml 주석에 명시. | 첫 RED→GREEN 직후 PR로 95/85 *상향*. OPS-2의 "강화는 자유". |
| **OD-3** | CI에서 pytest exit code 5(테스트 0건)를 *한시적*으로 허용. | 첫 RED 커밋 직전 *전이 상태*만 허용. CI 출력에 `::warning::` 표시 + README + ci.yml 주석에 *우회 제거 의무* 명시. | 첫 RED 커밋 PR에서 ci.yml의 우회 블록 *제거*. OPS-4 정신 보존. |
| **OD-4** | OG-9(import-linter) / OG-11(Hypothesis) / OG-12(Traceability 스크립트) / OG-13(혼합 커밋 검사기)는 *슬롯만 비워둔다*. | 본 단계에서 도입하면 (a) 학습 의도 흐림, (b) 본 단계 PR이 비대해짐, (c) OPS-3(별도 PR) 정신 위배. `pyproject.toml`의 `[opt-strict]` 슬롯과 ci.yml의 주석 슬롯만 정의. | 후속 PR(들)에서 *각각 별도 PR*로 도입. 도입 시 본 보고서 §1 STEP 4 표를 *업데이트*하지 않고, 새 보고서(`10_*` 등)로 외부화. |
| **OD-5** | pre-commit은 Stage 1만, CI는 Stage 1~5(슬롯 포함). | OPS-1의 *실용적 해석* — 로컬은 빠른 피드백, CI는 종합. 두 환경이 *동일 도구를 호출*하므로 결과 분기는 발생하지 않음. README에 명시. | 향후 pre-push 훅으로 Stage 2 일부 추가 검토 가능 (별도 PR). |
| **OD-6** | `tests/**/*.py`에서만 PLR2004 완화 (`per-file-ignores`). | 테스트의 AAA 입력값(예: `4`, `34`)은 매직 넘버 허용. 단 도메인 코드는 엄격 차단. | 도메인 코드에서 매직 넘버는 *반드시* `entity/` 상수 모듈로 추출. NFR-06 자동 강제. |
| **OD-7** | mypy `--strict` 동치 설정 (12개 옵션 활성화). | `.cursorrules` `type_hints.enforcement: mypy --strict 통과를 권장`. *권장*을 *강제*로 격상. 외부 라이브러리(hypothesis, pytest_cov)는 stubs 누락 무시. | 모든 함수/메서드에 타입 힌트 *필수*. `Any` 사용은 정당한 사유 주석 동반 시에만 허용 (`.cursorrules`). |
| **OD-8** | CI 매트릭스를 *Ubuntu + Python 3.10 단일 핀*으로 최소화. | PRD §11.3 OR-4 (CI 환경 차이로 OG-7/OG-14 흔들릴 가능성) 대응. 결정성 우선. | 매트릭스 확장(예: Windows / Mac / Python 3.11/3.12)은 *별도 PR*에서 OPS-5(게이트 결정성) 통과 검증 후 도입. |
| **OD-9** | `.gitignore`는 표준 + 도구 캐시 + 가상환경. `.cursorrules` `file_structure.tree`에 없는 *유일한* 추가 파일. | Python 표준 위생. 트리에 명시되지 않았지만 *부재 시 부수 효과*가 발생. | 본 단계 종료 후 첫 commit 직전 *명시적 합의* 필요 시 본 보고서 §3에 박제됨. |

---

## 3. 산출물 (13개 파일 — 라인 단위)

### 3.1 신설 파일 트리

```
MagicSquare_05/
├── .gitignore                        ← OD-9
├── .pre-commit-config.yaml           ← OG-1, OG-2, OG-3 (Stage 1)
├── pyproject.toml                    ← OG-1~6 단일 진실 출처
├── README.md                         ← 3-Track + 빠른 시작 + 게이트 카탈로그
├── .github/
│   └── workflows/
│       └── ci.yml                    ← Stage 1~5 5단계 명시
├── src/
│   └── magicsquare/
│       ├── __init__.py               ← 패키지 루트 + __version__
│       ├── boundary/
│       │   └── __init__.py           ← Track A 안내
│       ├── control/
│       │   └── __init__.py           ← 흐름 제어 안내
│       └── entity/
│           └── __init__.py           ← I1~I5 + 상수 출처 안내
└── tests/
    ├── __init__.py                   ← 명명 규약 + Test ID prefix
    ├── conftest.py                   ← "공통 fixture 0개" 명시
    ├── boundary/
    │   └── __init__.py               ← T-U-* 안내
    ├── control/
    │   └── __init__.py               ← T-D-050~052 안내
    └── entity/
        └── __init__.py               ← T-D-001~042 + T-INV-* 매핑
```

### 3.2 파일별 PRD 매핑

| 파일 | 보호 PRD 영역 | 책임 |
|---|---|---|
| `pyproject.toml` | §7 NFR-01/02/03/04/06 + §13.2 OG-1/2/3/4/5/6 | 도구 설정의 단일 진실 출처. 임계값 변경 시 *유일한* 영향 지점. |
| `.pre-commit-config.yaml` | §13.2 OG-1/2/3 + §13.3 Stage 1 + OPS-1/4 | 로컬 commit 단위 자동 강제. |
| `.github/workflows/ci.yml` | §13.2 OG-1~14 (활성 + 슬롯) + §13.3 5-Stage + OPS-1/2/4/5 | PR/Push 단위 자동 강제. *결정적* 환경 핀(OD-8). |
| `README.md` | §1 Executive Summary 운영 측 환원 | 신규 합류자/리뷰어 30초 진입. |
| `.gitignore` | (위생) | OS/IDE/도구 캐시 차단. |
| `src/magicsquare/__init__.py` | §10.1 Architecture + 패키지 메타 | `__version__` 노출. |
| `src/magicsquare/boundary/__init__.py` | §8.1 Track A + §10.1 Boundary Layer + DIP A-3 | T-U-* 안내. |
| `src/magicsquare/control/__init__.py` | §10.1 Domain Layer (control 하위) + BR-17 + NFR-09 | 흐름 제어 안내. |
| `src/magicsquare/entity/__init__.py` | §10.1 Domain Layer (entity 하위) + I1~I5 + NFR-06 | 도메인 상수 출처 예약. |
| `tests/__init__.py` | §8 Test ID prefix + 부록 B (테스트는 BR/AC 명시) | 명명 규약. |
| `tests/conftest.py` | `.cursorrules` `testing.fixture_scope` | "0개 fixture" 명시 — TDD 원칙 보존. |
| `tests/boundary/__init__.py` | §8.1 Track A + DT-4 | T-U-* 위치. |
| `tests/control/__init__.py` | §8.2 Track B + DT-5 + T-D-050~052 | 흐름 제어 단위 위치. |
| `tests/entity/__init__.py` | §8.2 Track B + §8.2.1 + §8.2.2 | 컴포넌트 + 불변조건 위치. |

---

## 4. OPS 규칙과의 정합성 (자기 검증)

> 본 절은 본 단계의 산출이 PRD §13.3의 OPS-1 ~ OPS-5를 *모두 만족하는가*를 자기 외부화 검증한다.

| OPS 규칙 | 본 단계의 만족 증거 | 위치 |
|---|---|---|
| **OPS-1** 로컬·CI 동일 게이트 집합 | `pyproject.toml`이 단일 진실 출처. pre-commit과 CI 모두 같은 도구(black/ruff/mypy/pytest)를 호출. | `pyproject.toml` 전체 + `.pre-commit-config.yaml` Stage 1 + `ci.yml` Stage 1 |
| **OPS-2** NFR 약화 임계 변경 금지 | `--cov-fail-under=0`은 *초기 미설정 상태*이며 *약화가 아님*을 README + `pyproject.toml` 주석에 명시. 첫 GREEN 직후 95/85 *상향* PR 의무. | `pyproject.toml` `[tool.pytest.ini_options]` 주석 + `README.md` §4 |
| **OPS-3** Ops 변경은 별도 PR | OG-9/11/12/13의 *단계적 도입*이 모두 별도 PR 슬롯으로 비워둠. `pyproject.toml`에 `[opt-strict]` 그룹 분리. | `pyproject.toml` `[project.optional-dependencies]` `opt-strict` + `ci.yml` Stage 3/4/5 주석 슬롯 |
| **OPS-4** 게이트 일시 비활성화 금지 | CI의 exit code 5 우회는 *한시적*이며 첫 RED 커밋 PR에서 *제거 의무*가 README + ci.yml 주석에 명시. | `README.md` §4 + `.github/workflows/ci.yml` Stage 2 주석 |
| **OPS-5** 게이트 자체도 결정적 | CI 단일 매트릭스(Linux/Python 3.10 핀) — OD-8 + PRD §11.3 OR-4 대응. | `.github/workflows/ci.yml` `runs-on` + `python-version` |

---

## 5. 본 단계의 *정직한* 미충족 보고

> `.cursorrules` `ai_behavior.honesty` 직접 운영. 본 단계가 *완전히 닫지 않은* 부분을 회피 없이 보고한다.

| 미충족 항목 | 사유 | 처리 |
|---|---|---|
| OG-9 (import-linter) 실제 활성화 | OD-4 (별도 PR로 분리) | 첫 RED→GREEN 사이클 *후* 별도 PR. 그때까지 BR-17/NFR-09는 *수기 코드 리뷰*가 유일한 방어. |
| OG-11 (Hypothesis Property) 실제 활성화 | OD-4 | 동일. 그때까지 P-01 ~ P-08은 *수기 parametrize 단정*으로 보호. |
| OG-12 (Traceability 무결성 스크립트) | OD-4 | 동일. 그때까지 §12 dangling reference 같은 결함은 *외부 분석*이 유일한 방어. |
| OG-13 (혼합 커밋 검사기) | OD-4 | 동일. 그때까지 DT-6은 *PR 리뷰 단계*에서 수기 차단(부록 B). |
| OG-14 (성능 상한) 실제 활성화 | pytest-benchmark 도입 + FR-05 첫 GREEN 후 | 동일. 그때까지 NFR-05는 *수기 측정*. |
| `.pre-commit-config.yaml`의 `mirrors-mypy` 호환성 | 일부 환경에서 mirrors-mypy가 dependency 해결에 실패 보고된 사례 존재 | 첫 `pre-commit run --all-files` 시 환경 검증 후, 필요 시 *local hook*(시스템 mypy 호출)로 교체. 본 보고서 §6에 *예상 위험*으로 기록. |
| pytest exit code 5 우회의 *자동 제거* | 본 단계의 ci.yml은 우회를 *주석*으로만 유도 | 첫 RED 커밋 PR에서 사람이 직접 제거. 향후 OG-13 스크립트 활성화 시 *우회 코드의 영구 잔존*을 자동 차단할 수 있음. |
| 부록 A Pre-RED Gate 10개 항목의 ✅ 박제 | 본 단계의 책임 영역 밖 | 후속 단계에서 사용자가 자가 점검하거나, *별도 closure log 보고서*로 박제. |

---

## 6. 본 단계가 후행 단계에 부과하는 제약

| 후행 단계 | 본 단계가 부과한 제약 |
|---|---|
| **첫 RED 테스트 작성** | DT-1을 만족하는 *Track A·B 한 쌍* 동시 작성. `tests/boundary/test_*.py` (T-U-001) + `tests/entity/test_*.py` (T-D-001) 권장. 첫 RED는 *반드시* `pre-commit run --all-files` + CI 통과를 *함께* 보여야 한다. |
| **첫 RED 커밋 PR** | (a) `ci.yml` Stage 2의 exit code 5 우회 *제거*. (b) `pyproject.toml`의 `--cov-fail-under` 임계 *상향*은 첫 GREEN 직후 별도 PR. (c) 한 PR은 한 phase만(DT-6). |
| **OG-9/11/12/13 도입 PR** | 각각 *별도 PR*(OPS-3). 도입 시 본 보고서 §1 STEP 4 표를 *수정하지 않고*, 새 보고서(`10_*` 또는 그 이후)로 외부화. |
| **임계값 변경 PR** | OPS-2 — 약화 거부. 강화는 자유 단 회귀 테스트 함께 동반. |
| **도구 교체 PR** (예: Ruff → 다른 린터) | §13.7 — 자유, 단 OG-12 동등 보호 수준 검증 (OG-12 활성화 전까지는 수기 검증 + PR 리뷰). |
| **회귀** | 본 단계의 13개 파일은 *그 자체로* 회귀 보호 대상. 누군가 `pyproject.toml`의 ruff `select`에서 `PL` 그룹을 제거하면 NFR-06 보호가 *즉시 깨진다*. 이 회귀는 사람이 PR 리뷰에서 차단해야 한다 (OG-12 활성화 전까지). |

---

## 7. 첫 RED 진입을 위한 *체크리스트*

> 본 절은 다음 작업자(또는 동일 학습자가 모자만 바꾼 상태)가 *바로 실행 가능한 명령*을 박제한다.

```powershell
# Windows PowerShell — 본 워크스페이스 루트에서
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files   # 최초 1회 — Stage 1 전체가 통과해야 함
```

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

이 직후, *PRD에 이미 byte-equal로 적힌* 두 RED를 *같은 작업 세션 내*에 작성한다 (DT-1):

| Track | 파일 (제안) | Test ID | 입력 | 기대 |
|---|---|---|---|---|
| A (Boundary) | `tests/boundary/test_input_validator_shape_violations.py` | `T-U-001` | 3행 입력 | `E_SHAPE` + `"Input must be a 4x4 matrix."` |
| B (Domain) | `tests/entity/test_magic_square_judge_standard.py` | `T-D-001` | §9.4 D-Std (Dürer 마방진) | `True` |

두 테스트는 *서로의 구현을 모르고*(DT-4 + DT-5) 동시에 RED여야 한다.

---

## 8. 본 단계의 마무리 진술

> **"본 단계는 PRD §13에서 paper로 정의된 Ops Track을 *작동 가능한 형태*로 환원한 첫 사이클이다.**
> **13개 파일이 산출되었으나 프로덕션 코드는 0줄, 테스트는 0건이다 — 이는 결함이 아니라 TDD 원칙의 정직한 보존이다.**
> **§13.3의 5-Stage 파이프라인 중 Stage 1(Static)은 *완전 활성*, Stage 2(Test)는 *첫 RED 직전 전이 상태로 한시 허용*, Stage 3/4/5는 *별도 PR을 위한 슬롯*으로 비워둠으로써, 본 단계가 한 PR로 비대해지는 위험을 피하면서 §13의 약속을 *기능적으로* 닫았다.**
> **다음 커밋은 *반드시* 첫 RED 테스트(DT-1을 만족하는 한 쌍)가 되며, 그 RED는 본 PRD의 어떤 줄도 새로 만들 필요 없이 §8의 Test ID와 §12 매트릭스가 가리키는 자리로 정확히 진입할 수 있다."**

본 단계가 닫히는 순간, 본 PRD는 *외부에서 검증 가능한 명세*에서 *외부 도구가 자동으로 강제하는 명세*로 전환되었다.
