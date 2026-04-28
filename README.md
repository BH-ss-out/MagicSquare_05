# Magic Square (4x4) — TDD 학습 프로젝트

> 본 저장소는 4x4 마방진 문제를 매개로 **TDD(Red→Green→Refactor) 사고 양식**과
> **Invariant 기반 검증 사고**를 훈련하기 위한 *순수 로직 중심* 학습 시스템이다.
> 모든 요구사항·계약·검증 기준은 [`docs/PRD.md`](docs/PRD.md) (756줄)에 *검증 가능한 술어*로 형식화되어 있고,
> 단계별 결정·합의는 `Report/01`~`Report/09`에 외부화되어 있으며, 실행·게이트는 `pyproject.toml`과 `.cursorrules`가 자동 강제한다.

---

## 0. 문서 관계 (Document Map)

> **한 줄 요약** *(출처: `Report/09` §0 + §1)*: 본 README는 *진입점*이고, [`docs/PRD.md`](docs/PRD.md)는 *단일 진실 출처*이며, `Report/01`~`Report/09`는 *결정의 외부화 박제*이고, `pyproject.toml` + `.cursorrules` + `.pre-commit-config.yaml` + `.github/workflows/ci.yml`은 *자동 강제 메커니즘*이다 — 네 층은 직교한다.

| 층위 | 위치 | 역할 | 변경 통제 |
|---|---|---|---|
| **진입점** | `README.md` (본 문서) | 30초 오리엔테이션 + 작업 큐 진입 | 자유 |
| **명세 (정본)** | [`docs/PRD.md`](docs/PRD.md) | 모든 FR/BR/NFR/AC/Test ID/매트릭스의 단일 진실 출처 | §0/§6/§12 **Frozen**, §13 유연 |
| **작업 보드 (라이브)** | [`docs/TODO.md`](docs/TODO.md) | Epic-001 / US-000~010 / TASK-XXX-1·2·3 / 추적 매트릭스 | 자유 (수시 갱신) |
| **결정 박제** | `Report/01` ~ `Report/09` | 단계별 합의·결함·정정의 turn-by-turn 외부화 | 보고서별 닫힘 |
| **자동 강제** | `pyproject.toml`, `.cursorrules`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml` | OG-1~14 게이트, ECB·TDD·forbidden 패턴 강제 | OPS-2 (NFR 약화 거부) |

**Report 인덱스**

| Report | 단계 | 핵심 산출 |
|---|---|---|
| `Report/01_문제_정의` | 표면 문제 → 정확한 문제 정의 | 5개 핵심 역량 C-1~C-5 |
| `Report/02_설계` | 입출력 계약 + 검증 우선순위 + 5종 실패 코드 | byte-equal 메시지 5종 |
| `Report/03_프로젝트_규약_정의` | TDD/ECB/네이밍/금지 패턴 | `.cursorrules`로 환원됨 |
| `Report/04_사용자여정_Epic` | Epic + 성공 기준 SC-1~SC-5 | 골격 |
| `Report/05_사용자여정_Journey` | 페르소나별 여정 | U-1~U-3 (이후 U-4 추가) |
| `Report/06_사용자여정_UserStories` | User Story 카탈로그 | US-001~US-004 (PRD §3 페르소나 매핑) |
| `Report/07_시나리오검증및정리` | TC-N-* / TC-F-* / TC-P-* 시나리오 정리 | PRD §9.1로 환원됨 |
| `Report/08_PRD_보강_및_Dual_Track_Ops_통합` | Dual-Track + Ops 프레임 정직 수용 | §13 Ops Track 신설 |
| `Report/09_Ops_스캐폴딩_및_초기_자동화_게이트` | 13개 파일 스캐폴딩 (현 상태) | OG-1~3 활성, OG-4~14 슬롯 |
| `Report/10_To-Do_보드_정립_및_README_통합` | 작업 큐 정립 (본 사이클) | `docs/TODO.md` 신설 + 본 README 통합 |

---

## 1. 시스템 정의 (Story)

> *출처*: `Report/04_사용자여정_Epic` + `Report/06_사용자여정_UserStories` + PRD §3.

**Epic-001 — 4x4 Magic Square 완성 시스템**
임의로 주어진 4x4 정수 격자(빈칸 정확히 2칸)에 대해 누락된 두 숫자를 두 빈칸에 배치한 결과가 *마방진의 불변 조건을 충족하는지* 결정하고, 충족 시 그 배치 순서를 *byte-equal* 한 `int[6]`으로 반환한다.

**핵심 User Story 4건**

| US ID | 페르소나 (PRD §3) | 요지 |
|---|---|---|
| **US-001** | U-1 TDD 학습자 | Track A·B의 첫 RED를 *같은 작업 세션 안에* 동시 작성 (DT-1) |
| **US-002** | U-3 호출자 | `int[][]` 한 개에 대해 *항상* `int[6]` 또는 5종 중 *정확히 하나*의 도메인 예외 (BR-15·19) |
| **US-003** | U-2 코드 리뷰어 | 임의 테스트 ID → §12 매트릭스로 30초 내 역추적 (NFR-08) |
| **US-004** | U-4 Ops 운영자 | OG-1~14 결정적 통과 + *임계값 약화 PR 0건* (OPS-2·5) |

> 본 PRD에서 **"UI"는 화면이 아니라 *외부 호출자와 도메인 사이의 입출력 경계***다 (`Report/02` §2). GUI/Web/CLI 디자인은 PRD §4.2 O-1로 명시 배제.

---

## 2. 핵심 계약 요약 (Contract at a Glance)

> *출처*: PRD §0 (입출력 계약 — Frozen) + §0.3 (5종 도메인 실패 코드).

### 2.1 입력 (PRD §0.1)

| 항목 | 규칙 |
|---|---|
| 타입 | `int[][]` (정수 2차원 배열) |
| 형태 | 4행 4열 |
| 값 범위 | `0` 또는 `1..16` |
| 빈칸 표지 | `0` |
| 빈칸 개수 | **정확히 2개** |
| 중복 | 0을 제외한 값에 중복 금지 |

### 2.2 출력 (PRD §0.2)

| 항목 | 규칙 |
|---|---|
| 타입 | `int[6] = [r1, c1, n1, r2, c2, n2]` |
| 좌표 | **1-index** (`1 ≤ r,c ≤ 4`), row-major 순서 `(r1,c1) < (r2,c2)` |
| 시도 1 | `(작은수 → 첫 빈칸, 큰수 → 둘째 빈칸)` 채움 후 마방진이면 그 순서로 반환 |
| 시도 2 | 시도 1 실패 시 `(큰수 → 첫 빈칸, 작은수 → 둘째 빈칸)` 채움 후 역순 반환 |
| 두 시도 모두 실패 | **`E_UNSOLVABLE` 예외** (PRD §11 R-1) |
| Magic Constant | `M = 34` |

### 2.3 5종 도메인 실패 코드 (PRD §0.3 + §8.1.2)

| 코드 | 의미 | 책임 레이어 | 표준 메시지 (byte-equal — NFR-07) |
|---|---|---|---|
| `E_SHAPE` | 4x4 형태가 아님 | Boundary | `"Input must be a 4x4 matrix."` |
| `E_VALUE_RANGE` | 셀 값이 `{0} ∪ {1..16}` 밖 | Boundary | `"Each cell must be 0 or an integer in [1, 16]."` |
| `E_BLANK_COUNT` | 빈칸이 정확히 2개가 아님 | Boundary | `"Input must contain exactly 2 blanks (zeros)."` |
| `E_DUPLICATE` | 0을 제외한 중복 존재 | Boundary | `"Non-zero values must be unique."` |
| `E_UNSOLVABLE` | 두 조합 모두 마방진 미성립 | Domain | `"No valid magic square completion exists for the given input."` |

> 한 입력에 다중 위반이 있어도 **단 하나의 코드만 반환** (BR-19, R-7). 코드 결정은 *형태 → 값 범위 → 빈칸 개수 → 중복* 순서.

---

## 3. 3-Track 구조 + ECB 매핑

> *출처*: PRD §8 (Dual-Track) + §13 (Ops Track) + `.cursorrules` `architecture`.

### 3.1 3-Track (Dual-Track + Ops 직교)

| Track | 책임 | RED 출처 | 사이클 | PRD 위치 |
|---|---|---|---|---|
| **A — Boundary (UI) TDD** | 입력 계약 검증, 표준 에러 메시지 byte-equal | 입력 계약 + 우선순위 | RED→GREEN→REFACTOR | §8.1 |
| **B — Domain (Logic) TDD** | I1~I5 보호, 마방진 판정·해 찾기 | 수학적 술어 D6 | RED→GREEN→REFACTOR | §8.2 |
| **C — Ops (Quality Gates)** | A/B 두 트랙을 자동 강제하는 *메타 트랙* | (사이클 다름) | G(Gate) → GP(Pass) → GR(Refine) | §13 |

> ⚠️ **MLOps가 아니다**. 본 프로젝트는 *결정론적* 마방진이며 ML 모델 학습/배포는 PRD §13.5 OO-1로 명시 배제.

### 3.2 ECB 책임 분리 (`.cursorrules` `architecture.layers`)

| 레이어 | 폴더 | 책임 | 의존 가능 | 금지 |
|---|---|---|---|---|
| **Boundary** | `src/magicsquare/boundary/` | 외부 입출력 (FR-01 입력 검증, 표준 에러) | `control`, `entity` | 비즈니스 규칙 직접 수행 / 도메인 상태 직접 변경 |
| **Control** | `src/magicsquare/control/` | 비즈니스 로직 / 유스케이스 (FR-02~05) | `entity` | `boundary` 의존 / 직접 I/O |
| **Entity** | `src/magicsquare/entity/` | 도메인 모델 + I1~I5 + 도메인 상수 | (없음) | 외부 계층 의존 / I/O / 부수 효과 |

**의존성 방향**: `boundary → control → entity` *단방향* (BR-17 / NFR-09 / `.cursorrules` `dependency_direction`). Domain → Boundary import는 OG-9(`import-linter`)로 자동 차단 예정.

### 3.3 5개 도메인 불변 조건 (Invariants)

| ID | 불변 조건 | 보호 BR (PRD §6) |
|---|---|---|
| **I1** | 형태 — 입력은 항상 4행 4열 | BR-01, BR-03 |
| **I2** | 정의역 — 모든 셀 ∈ `{0,1,...,16}` | BR-02 |
| **I3** | 유일성 — 0 제외 값 중복 없음 + 누락 숫자 정확히 2 | BR-04, BR-18 |
| **I4** | 합 균질 — 모든 행/열/두 대각의 합 = 34 | BR-05, BR-06 |
| **I5** | 결정성 + 부작용 금지 — 동일 입력 → 동일 결과, 입력 행렬 byte-equal 보존 | BR-15, BR-16 |

---

## 4. TDD 사이클 + 병렬 진행 규칙

> *출처*: `.cursorrules` `tdd_rules` + PRD §8.3 (DT-1 ~ DT-6).

### 4.1 RED → GREEN → REFACTOR (`.cursorrules` `tdd_rules`)

| Phase | 핵심 규칙 | 금지 |
|---|---|---|
| **RED** | 프로덕션 코드보다 테스트를 *반드시 먼저*. 한 테스트는 *단일 동작/단일 불변*만 검증 | 컴파일 에러를 RED로 간주 / 다중 동작 검증 |
| **GREEN** | *현재 실패 테스트만* 통과시키는 최소 코드. 임시 구현(하드코딩) 허용 | 동시 리팩터링 / 무관한 새 기능 / 추가 테스트 동시 작성 |
| **REFACTOR** | 외부 동작 보존 + 중복 제거 + 명명 개선 + ECB 경계 정리 | 새 기능 / 새 테스트 / 외부 동작 변경 / 중간 RED 상태 커밋 |

### 4.2 Dual-Track 병렬 진행 (PRD §8.3)

| 규칙 | 요지 |
|---|---|
| **DT-1** | Track A·B의 *첫 RED*는 같은 작업 세션 안에 동시 작성 |
| **DT-2** | `[A.RED]&[B.RED] → [A.GREEN]&[B.GREEN] → [A.REFACTOR]&[B.REFACTOR]` — 양 Track 모두 완료 후 다음 phase |
| **DT-3** | *"도메인을 다 끝낸 후 경계 추가"* 진행 **금지** |
| **DT-4** | Track A의 RED는 Domain Mock 사용. 실제 Domain 없어도 RED→GREEN 완주 |
| **DT-5** | Track B의 RED는 Boundary 호출 0건. 사전조건 충족 입력을 직접 전달 |
| **DT-6** | 한 커밋은 *하나 Track의 하나 phase*만 (혼합 커밋 금지). OG-13으로 자동 차단 예정 |

---

## 5. 빠른 시작 (Setup)

> *출처*: `pyproject.toml` `[project.optional-dependencies] dev` + `Report/09` §7 첫 RED 진입 체크리스트.

### 5.1 가상환경 + 개발 의존성 설치

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

`dev` 그룹은 OG-1~6에 직접 매핑된 6종(`black` / `ruff` / `mypy` / `pytest` / `pytest-cov` / `pre-commit`). OG-9·11(`import-linter` / `hypothesis`)은 *별도 PR*에서 도입할 `opt-strict` 그룹에 분리되어 있다 (OPS-3).

### 5.2 Pre-commit 훅 등록 (Stage 1 게이트 자동 실행)

```bash
pre-commit install
pre-commit run --all-files   # 최초 1회 전체 검증 (Report/09 §7)
```

이 시점부터 모든 `git commit`은 OG-1(Black) → OG-2(Ruff) → OG-3(mypy)을 자동 통과해야 한다 (OPS-1: 로컬·CI 동일 게이트).

---

## 6. 자동화 게이트 카탈로그 (PRD §13.2 — OG-1 ~ OG-14)

> *출처*: PRD §13.2 + `pyproject.toml` + `.pre-commit-config.yaml` + `.github/workflows/ci.yml`.

| Gate | 도구 | 보호 NFR/BR | Stage | 상태 |
|---|---|---|---|---|
| **OG-1** | Black | (코드 스타일) | 1 Static | ✅ 활성 |
| **OG-2** | Ruff (PLR2004 포함) | NFR-06 매직 넘버 금지 | 1 Static | ✅ 활성 |
| **OG-3** | `mypy --strict` | 타입 안전성 | 1 Static | ✅ 활성 |
| **OG-4** | pytest | NFR-02 / BR-19 / BR-20 | 2 Test | ✅ 활성 (exit-code 5 한시 허용) |
| **OG-5** | pytest-cov (Domain ≥ 95%) | NFR-01 | 2 Test | 🟦 임계 0 → 첫 GREEN 후 95 상향 |
| **OG-6** | pytest-cov (Boundary ≥ 85%) | NFR-02 | 2 Test | 🟦 임계 0 → 첫 GREEN 후 85 상향 |
| **OG-7** | pytest 100회 반복 단정 | NFR-03 / BR-15 결정성 | 3 Invariant | 🟦 첫 RED 시 활성 |
| **OG-8** | pytest deep-copy 단정 | NFR-04 / BR-16 부작용 | 3 Invariant | 🟦 첫 RED 시 활성 |
| **OG-9** | `import-linter` | NFR-09 / BR-17 의존성 방향 | 4 Architecture | ⏸ 슬롯 (TASK-101) |
| **OG-10** | 문자열 동등성 단정 | NFR-07 메시지 byte-equal | 3 Invariant | 🟦 첫 RED 시 활성 |
| **OG-11** | Hypothesis | PRD §9.4 P-01~P-08 | 3 Invariant | ⏸ 슬롯 (TASK-091) |
| **OG-12** | 커스텀 docstring 파서 | NFR-08 Traceability | 4 Architecture | ⏸ 슬롯 (TASK-102) |
| **OG-13** | 커밋+파일 분석기 | DT-6 혼합 커밋 금지 | 4 Architecture | ⏸ 슬롯 (TASK-103) |
| **OG-14** | pytest-benchmark | NFR-05 성능 ≤ 50ms | 5 Performance | ⏸ 슬롯 (TASK-104, 참고용) |

OPS 운영 규칙 5종은 PRD §13.3 (OPS-1 동일 게이트 / OPS-2 약화 거부 / OPS-3 별도 PR / OPS-4 일시 비활성화 금지 / OPS-5 결정성).

---

## 7. 작업 보드 (To-Do 요약)

> **정본은 [`docs/TODO.md`](docs/TODO.md)** (라이브 보드, 수시 갱신).
> 본 절은 *진입 큐와 상위 골격*만 박제한다. *RED/GREEN/REFACTOR sub-task와 추적 매트릭스 39행*은 정본 참조.

### 7.1 진입 큐 (다음 5개 커밋)

| 순서 | TASK | Phase | 비고 |
|---|---|---|---|
| ① | **TASK-001** | (Pre-RED) | PRD 부록 A 10개 항목 ✅ 박제 — 본 단계가 닫혀야 PRD가 *닫힘* |
| ② | **TASK-002** | (Pre-RED) | R-2 종결 (D-In-B / D-Uns 4x4 행렬 확정) — TASK-061·070 BLOCKED 해제 |
| ③ | **TASK-003** | (Pre-RED) | `pre-commit run --all-files` 1회 박제 |
| ④ | **TASK-010-1 + TASK-030-1** | RED *(DT-1 한 쌍)* | `T-U-001` (3행 → `E_SHAPE`) + `T-D-001` (D-Std → `true`) — *같은 세션, 다른 커밋* |
| ⑤ | **`ci.yml` Stage 2 우회 제거** | GREEN 직후 | 첫 GREEN 진입과 동시에 exit-code 5 우회 제거 (`Report/09` §6 의무) |

### 7.2 User Story 골격 (US-000 ~ US-010)

| US | 제목 | 핵심 TASK | ECB |
|---|---|---|---|
| **US-000** | Pre-RED 진입 게이트 박제 (PRD 부록 A) | TASK-001·002·003 | (메타) |
| **US-001** | Boundary 입력 검증 (FR-01) | TASK-010·011·012·013·014·015·016 | Boundary |
| **US-002** | Domain Entity 골격 (상태 표현) | TASK-020·021·022·023 | Entity |
| **US-003** | 마방진 판정 (FR-04 — Logic 첫 RED) | TASK-030·031·032·033 | Control |
| **US-004** | 빈칸 탐지 (FR-02) | TASK-040 | Control + Entity |
| **US-005** | 후보값 필터링 (FR-03) | TASK-050·051 | Control + Entity |
| **US-006** | 완성 로직 (FR-05) | TASK-060·061·062·063·064 | Control |
| **US-007** | 잘못된 입력 처리 (실패 시나리오) | TASK-070·071·072·073 | 통합 |
| **US-008** | 정상 시나리오 통합 (TC-N-*) | TASK-080·081 | 통합 |
| **US-009** | 불변조건 + Property 회귀 | TASK-090·091 | Entity / 통합 |
| **US-010** | 테스트 커버리지 체크포인트 (Ops G→GP→GR) | TASK-100·101·102·103·104 | (메타·Ops) |

### 7.3 Definition of Done (Epic-001)

- [ ] PRD §12 Traceability Matrix 14행이 *모두* 최소 1개 GREEN 테스트로 보호 (NFR-08)
- [ ] OG-1 ~ OG-8, OG-10 모두 CI 결정적 통과 (PRD §13.3 Stage 1·2·3)
- [ ] OG-5 (Domain 95% 라인 / 90% 분기), OG-6 (Boundary 85% 라인) 통과
- [ ] PRD §11.3 R-2가 닫히고 D-In-B / D-Uns 구체 행렬이 PRD §9.3에 박제
- [ ] OG-9 / OG-11 / OG-12 / OG-13가 별도 PR로 도입 (OPS-3)

---

## 8. 초기 상태 + 다음 행동 (TDD 출발점)

> *출처*: `Report/09` §0.1 (직전 상태) + §6 (후행 단계 부과 제약) + PRD §8.3 (DT-1).

본 저장소는 *현재 테스트 0건, 프로덕션 코드 0건* 상태에서 시작한다. **이는 의도다** (`Report/09` §0.4: "프로덕션 코드 0줄, 테스트 0건은 결함이 아니라 의도다").

- **다음 커밋**은 [`docs/TODO.md`](docs/TODO.md) §진입 큐의 *TASK-001*이거나, Pre-RED 게이트가 이미 닫혔다면 *TASK-010-1 + TASK-030-1* (DT-1 한 쌍)이 되어야 한다.
- pytest는 초기에 exit code 5(테스트 0건)를 반환할 수 있다. CI는 이를 *한시적으로* 허용하며, 첫 RED 커밋 PR에서 우회를 *제거*한다 (OPS-4: 일시 비활성화 금지).
- 첫 RED→GREEN 전이 직후 PR로 `pyproject.toml`의 `--cov-fail-under` 임계를 *95(Domain) / 85(Boundary)* 로 *상향*한다 (OPS-2: 강화는 자유).

---

## 9. 디렉토리 구조

> *출처*: `.cursorrules` `file_structure.tree` (1:1 일치 — `Report/09` §1 STEP 7 검증 완료).

```
MagicSquare_05/
├── .cursorrules                  # 프로젝트 규약 (ECB / TDD / forbidden / file_structure)
├── .gitignore
├── .pre-commit-config.yaml       # OG-1 ~ OG-3 로컬 강제
├── .github/workflows/ci.yml      # OG-1 ~ OG-14 (5-Stage)
├── pyproject.toml                # 도구 설정 단일 진실 출처 (OG-1 ~ OG-6 직접 매핑)
├── README.md                     # 본 문서
├── docs/
│   ├── PRD.md                    # 명세 정본 (756줄, §0/§6/§12 Frozen)
│   └── TODO.md                   # 작업 보드 라이브 정본
├── src/
│   └── magicsquare/
│       ├── __init__.py
│       ├── boundary/             # FR-01 입력 검증, 표준 에러
│       ├── control/              # FR-02 ~ FR-05 유스케이스 / 검증 흐름 조율
│       └── entity/               # 도메인 모델 + I1~I5 + 상수
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── boundary/                 # T-U-* 시리즈 (Track A)
│   ├── control/                  # T-D-050~052 (오케스트레이션)
│   └── entity/                   # T-D-001~042, T-INV-* (Track B)
├── Prompt/                       # 단계별 프롬프트 자료
└── Report/                       # 단계별 산출 보고서 (01 ~ 09)
```

---

## 10. 자주 쓰는 명령

> *출처*: `pyproject.toml` `[tool.*]` 설정 + `.pre-commit-config.yaml`.

| 목적 | 명령 |
|---|---|
| 로컬 게이트 전체 실행 (pre-commit) | `pre-commit run --all-files` |
| 단위 테스트 실행 (커버리지 포함) | `pytest` |
| 커버리지 HTML 리포트 | `pytest --cov-report=html` → `htmlcov/index.html` |
| 타입 검사 (단독) | `mypy src` |
| Lint (단독, 자동 수정) | `ruff check src tests --fix` |
| 포맷 (단독) | `black src tests` |
| Track A 테스트만 실행 | `pytest -m boundary` |
| Track B 테스트만 실행 | `pytest -m domain` |
| Invariant 테스트만 실행 | `pytest -m invariant` |
| Property 테스트만 실행 (도입 후) | `pytest -m property` |

---

## 11. 더 깊이 파고들기

| 주제 | 위치 |
|---|---|
| 입출력 계약 (Frozen) | [`docs/PRD.md`](docs/PRD.md) §0 |
| 5개 도메인 실패 코드 + 표준 메시지 | [`docs/PRD.md`](docs/PRD.md) §0.3 + §8.1.2 |
| FR-01 ~ FR-05 + AC | [`docs/PRD.md`](docs/PRD.md) §5 |
| BR-01 ~ BR-20 (Frozen) | [`docs/PRD.md`](docs/PRD.md) §6 |
| NFR-01 ~ NFR-09 | [`docs/PRD.md`](docs/PRD.md) §7 |
| Track A/B 필수 RED 테스트 ID 카탈로그 | [`docs/PRD.md`](docs/PRD.md) §8.1.1, §8.2.1 |
| Test Plan + 시나리오 (TC-N-* / TC-F-* / TC-P-*) | [`docs/PRD.md`](docs/PRD.md) §9 |
| Traceability Matrix (Frozen) | [`docs/PRD.md`](docs/PRD.md) §12 |
| Ops 게이트 + 5-Stage CI + OPS-1~5 | [`docs/PRD.md`](docs/PRD.md) §13 |
| Pre-RED 합의 게이트 10개 | [`docs/PRD.md`](docs/PRD.md) 부록 A |
| Dual-Track + Ops 통합 결정 과정 | `Report/08_PRD_보강_및_Dual_Track_Ops_통합.md` |
| Ops 스캐폴딩 13개 파일 외부화 | `Report/09_Ops_스캐폴딩_및_초기_자동화_게이트.md` |
| 작업 큐 정립 + README 통합 결정 박제 | `Report/10_To-Do_보드_정립_및_README_통합.md` |
| ECB·TDD·forbidden 패턴 강제 | `.cursorrules` |
| 작업 보드 (라이브 정본) | [`docs/TODO.md`](docs/TODO.md) |

---

> **마무리 진술** *(출처: PRD §마무리 진술)*
> *"본 PRD는 마방진을 풀기 위한 명세가 아니다. 본 PRD는 불변 조건(I1~I5)을 먼저 진술하고, 검증을 먼저 설계하며, 입출력 계약을 byte-equal 수준으로 고정한 채, Boundary와 Domain을 각자 독립된 RED→GREEN→REFACTOR 사이클로 운영하는 학습 시스템의 — 외부에서 검증 가능한 — 명세다."*
