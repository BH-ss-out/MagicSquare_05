# Magic Square (4x4) — Test Case Specification

> 본 문서는 **테스트 케이스 카탈로그의 단일 진실 출처**다. PRD의 *FR/AC/BR/Test ID*와 1:1 추적 가능한 형태로, 각 테스트를 **테스트 환경 / 전제 조건 / 성공·실패 기준 / 특별하게 필요한 절차** 4-섹션 양식으로 박제한다.
>
> 본 문서는 **변경 통제: 자유**다. 다만 *Test ID와 PRD §12 매트릭스의 정합성*은 깨지면 안 된다(NFR-08). 신규 RED 작성 시 본 문서의 해당 행을 함께 갱신한다.

---

## 0. 문서 메타데이터

| 항목 | 내용 |
|---|---|
| 문서 ID | `TC-SPEC-MagicSquare-4x4` |
| 산출 단계 | Test Case Specification (PRD §9 보강) |
| 정본 출처 | `docs/PRD.md` §0 입출력 계약, §0.3 실패 코드, §5 FR, §6 BR, §7 NFR, §8 Dual-Track, §9 Test Plan, §12 Traceability Matrix |
| 작업 보드 | `docs/TODO.md` (TASK-XXX 매핑) |
| 산출 형식 | Markdown (4-섹션 양식 + 카탈로그 표) |
| 변경 통제 | 자유. 단 PRD §0/§6/§12 Frozen 영역과 *충돌하는 변경*은 거부됨. |
| 매핑 약어 | `T-U-*` Track A(Boundary) · `T-D-*` Track B(Domain) · `TC-N/F/P-*` 통합 시나리오 · `T-INV-*` 불변 회귀 · `P-*` Property |

---

## 1. 본 문서의 위치 (Document Map과의 관계)

| 층위 | 위치 | 본 문서와의 관계 |
|---|---|---|
| 명세 (정본) | `docs/PRD.md` (756줄) | 본 문서의 **계약·우선순위·메시지의 출처**. 충돌 시 PRD가 우선. |
| 작업 보드 (라이브) | `docs/TODO.md` (404줄) | 본 문서의 각 TC는 *어느 TASK-XXX-N의 RED인지* 명시한다. |
| **테스트 케이스 (본 문서)** | `docs/MagicSquare_TestCaseSpecification.md` | RED 작성 직전 *4-섹션 양식*으로 환원된 테스트 의도. |
| 자동 강제 | `pyproject.toml` · `.pre-commit-config.yaml` · `.github/workflows/ci.yml` | OG-1\~14 게이트가 본 문서의 단정을 *결정적으로* 강제한다. |

> 본 문서를 *복사해 docstring으로 옮기면* OG-12(Traceability 무결성, 미래 활성화) 자동 검사와 정합한다.

---

## 2. 공통 테스트 환경 (모든 TC 공통)

> 이하 개별 TC의 "테스트 환경" 섹션은 *위와 다른 점만* 기재한다 (DRY).

| 항목 | 값 | 출처 |
|---|---|---|
| 언어/런타임 | Python **3.10+** | `pyproject.toml`, `.cursorrules` `project.python_version` |
| 테스트 러너 | `pytest` (AAA 패턴) | `pyproject.toml [tool.pytest.ini_options]`, `.cursorrules` `testing.framework` |
| 커버리지 도구 | `pytest-cov` (Domain ≥95% / Boundary ≥85%) | OG-5 / OG-6 |
| 격리 환경 | `python -m venv .venv` + `pip install -e ".[dev]"` | README §5.1 |
| 정적 게이트 | OG-1 Black · OG-2 Ruff (PLR2004 포함) · OG-3 mypy `--strict` 통과 후 RUN | `.pre-commit-config.yaml`, `ci.yml` Stage 1 |
| 결정성 | OS·Python·타임존 차이 무관, 100회 반복 시 동일 결과 (BR-15 / OG-7) | PRD §6, §13.2 |
| 부작용 금지 | 호출 전·후 입력 행렬 byte-equal (BR-16 / OG-8) | PRD §6 |
| 표준 메시지 | byte-equal 영문 5종 (NFR-07 / OG-10) | PRD §0.3 / §8.1.2 |
| 디렉토리 미러링 | `tests/boundary/` ↔ `src/magicsquare/boundary/` 등 | `.cursorrules` `file_structure` |
| pytest 마커 | `@pytest.mark.boundary` / `domain` / `invariant` / `property` | `pyproject.toml [tool.pytest.ini_options.markers]` |
| 허용 사항 | `pytest.raises(...)` byte-equal 단정 / `unittest.mock.Mock` (Track A의 DT-4) | PRD §8.1.1, §8.3 DT-4 |
| 금지 사항 | Domain 테스트에서 `from magicsquare.boundary ...` import (DT-5 / NFR-09 / BR-17) | PRD §8.3 |

### 2.1 표준 도메인 실패 코드·메시지 (byte-equal — 본 문서 어디서도 변경 금지)

| 코드 | 예외 클래스 (개념) | 표준 메시지 (NFR-07) |
|---|---|---|
| `E_SHAPE` | `BoundaryError` → `ShapeError` | `"Input must be a 4x4 matrix."` |
| `E_VALUE_RANGE` | `BoundaryError` → `ValueRangeError` | `"Each cell must be 0 or an integer in [1, 16]."` |
| `E_BLANK_COUNT` | `BoundaryError` → `BlankCountError` | `"Input must contain exactly 2 blanks (zeros)."` |
| `E_DUPLICATE` | `BoundaryError` → `DuplicateError` | `"Non-zero values must be unique."` |
| `E_UNSOLVABLE` | `DomainError` → `UnsolvableError` | `"No valid magic square completion exists for the given input."` |

### 2.2 표준 테스트 데이터 (PRD §9.3)

#### D-Std — 표준 Dürer 마방진 (모든 합 = 34)

```
[ [16,  3,  2, 13],
  [ 5, 10, 11,  8],
  [ 9,  6,  7, 12],
  [ 4, 15, 14,  1] ]
```

#### D-In-A — 시도 A로 풀리는 입력 (PRD §9.3.2)

```
[ [ 0,  3,  2, 13],
  [ 5, 10, 11,  8],
  [ 9,  6,  7, 12],
  [ 4, 15, 14,  0] ]
```
- BlankPair `((1,1),(4,4))`, MissingPair `(1, 16)` → 결과 `[1,1,1, 4,4,16]`

#### D-In-B / D-Uns — **PRD §11 R-2에 의해 미확정** (TASK-002에서 종결 예정)

본 문서의 모든 D-In-B / D-Uns 의존 TC는 TASK-002 종결 전까지 `@pytest.mark.xfail(reason="R-2 D-In-B/D-Uns unsealed")` 로 마킹.

---

## 3. Test ID 체계 + 첨부 카탈로그 매핑

본 프로젝트의 Test ID 체계(PRD §8.1·§8.2·§9.1)는 *컴포넌트·Track 축*으로 분류된다. 외부 카탈로그(예: 함수 단위 분류표)와의 매핑:

| 외부 분류축 (예: "기능 단위") | 본 프로젝트의 컴포넌트 / Test ID | TODO TASK |
|---|---|---|
| 빈칸 찾기 (`find_blank_coords`) | `BlankFinder` / FR-02 / `T-D-010~014` | TASK-040 |
| 마방진 검증 (`is_magic_square`) | `MagicSquareJudge` / FR-04 / `T-D-001~009` | TASK-030~033 |
| solution() / 빈칸 채우기 / 경계값 | `FillPlanResolver` + `MagicResultAssembler` / FR-05 / `T-D-030~042` / `TC-N-*` | TASK-060~064, 080 |
| 오류 / 예외 | `InputValidator` / FR-01 / `T-U-001~042` + `E_UNSOLVABLE`(`T-D-032`) | TASK-010~016, 070 |

---

## 4. DT-1 한 쌍 — 첫 RED (현재 `red` 브랜치의 직접 작업 대상)

PRD §8.3 DT-1에 의해 **두 RED를 같은 작업 세션 안에**, DT-6에 의해 **각각 별도 커밋으로** 작성한다.

### 4.1 `T-U-001` — Boundary 첫 RED: 3행 입력 → `E_SHAPE`

| 키 | 값 |
|---|---|
| 소속 | Track A (Boundary) — `InputValidator` |
| TODO 매핑 | `TASK-010-1` |
| 요건 추적 | FR-01 ① / BR-01 / AC-01-01 / I1 / NFR-07·BR-20 / PRD §12 행 1 |
| 우선순위 | **P1** (DT-1 짝, 진입 큐 ④) |

#### 테스트 환경
- §2 공통 환경.
- *추가*: Domain Mock 사용 (`unittest.mock.Mock`). DT-4에 의해 *실제 Domain 구현 없이도* Track A는 RED→GREEN 완주 가능해야 함.
- 파일: `tests/boundary/test_input_validator.py` (신설 — 현재 `tests/boundary/__init__.py`만 존재).
- 마커: `@pytest.mark.boundary`.

#### 전제 조건
1. `src/magicsquare/boundary/input_validator.py`의 공개 함수 시그니처 합의 — *제안*: `def validate(matrix: list[list[int]]) -> None` (위반 시 raise, 정상 시 None 반환). *대안*: `Result` VO 반환.
2. 표준 예외 클래스 `BoundaryError → ShapeError`가 `entity/exceptions.py`에 *최소 stub*으로 존재 — 그렇지 않으면 `ImportError`로 컬렉션 실패가 발생하며, 이는 `.cursorrules` `tdd_rules.red_phase.must_not` 두 번째 항목에 의해 **의도된 RED로 인정되지 않는다**. → stub은 본 RED와 *같은 커밋*에 포함되거나 *직전 메타 커밋*으로 분리.
3. 입력 데이터: `matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]` (3행 4열, 형태 위반).

#### 성공/실패 기준

| 구분 | 기준 |
|---|---|
| **GREEN(통과) 조건** *(현 단계는 금지 — RED여야 함)* | `validate(matrix)`가 `ShapeError`를 raise하고, `str(exc.value) == "Input must be a 4x4 matrix."` (NFR-07 byte-equal) |
| **RED(의도된 실패) 조건** | (a) raise 자체가 안 일어남, (b) 다른 예외 타입(`ValueError` 등) 발생, (c) 메시지 byte-mismatch — 위 단정문이 `AssertionError`로 실패. **단, `ImportError`로 인한 컬렉션 실패는 RED로 인정되지 않음**. |
| **거부 조건** *(어떤 경우에도 PASS 처리 금지)* | Domain Mock이 *한 번이라도* 호출됨(`mock.assert_not_called()` 위반) — AC-01-11 위반. 다중 코드 동시 raise — BR-19 위반. |

#### 특별하게 필요한 절차
1. **Mock 호출 횟수 단정** *필수*: `domain_mock.assert_not_called()`를 단정에 포함.
2. **byte-equal 단정** *필수*: `assert exc.value.args[0] == "Input must be a 4x4 matrix."` (NFR-07). *금지*: `in` 부분 일치, `.lower()` 변환.
3. **DT-6**: 본 RED는 *단일 커밋*. 같은 커밋에 GREEN 구현·다른 RED·리팩터를 *섞지 않음*. 권장 커밋 메시지: `test(boundary): T-U-001 expects E_SHAPE for 3-row input (RED)`.
4. **DT-1 짝**: 본 커밋과 *같은 작업 세션* 안에 §4.2의 `T-D-001` 커밋도 작성. 순서는 무관.
5. **CI 영향**: 첫 RED 통과 *후* 같은 PR에서 `ci.yml` Stage 2의 `EXIT==5` 우회 코드를 *제거*해야 함 (`Report/09` §6, OPS-4).
6. docstring에 `보호 BR: BR-01 / 보호 AC: AC-01-01 / Track: A(Boundary)` 명시 — OG-12(Traceability 무결성, 미래 활성화) 대비 (NFR-08).

---

### 4.2 `T-D-001` — Domain 첫 RED: 표준 마방진 → `true`

| 키 | 값 |
|---|---|
| 소속 | Track B (Domain) — `MagicSquareJudge` |
| TODO 매핑 | `TASK-030-1` |
| 요건 추적 | FR-04 / AC-04-01 / BR-06 / I4 / PRD §12 행 6 |
| 우선순위 | **P1** (DT-1 짝, 진입 큐 ④) |

#### 테스트 환경
- §2 공통 환경.
- *추가*: Boundary 호출 *0건* (DT-5). 사전조건 충족 입력을 *직접* 전달.
- 파일: `tests/control/test_magic_square_judge.py` (신설 — 현재 `tests/control/__init__.py`만 존재).
- 마커: `@pytest.mark.domain`.

#### 전제 조건
1. `src/magicsquare/control/magic_square_judge.py`의 공개 함수 시그니처 — *제안*: `def is_magic(board: list[list[int]]) -> bool`.
2. 입력 데이터: §2.2 D-Std (빈칸 0개 완전 채움). 사전 검산: 행/열/주대각/부대각 10개 합 모두 = `34`.
3. 도메인 상수 `MAGIC_CONSTANT = 34`가 `entity/constants.py`에 정의(TASK-020 트리거)되어 있거나 본 RED와 *같은 커밋*에 최소 stub만 존재.

#### 성공/실패 기준

| 구분 | 기준 |
|---|---|
| **GREEN(통과) 조건** *(현 단계는 금지)* | `is_magic(D_STD) is True` |
| **RED(의도된 실패) 조건** | 함수 미구현 시 `assert True is True`로 임의 통과시키는 행위 *금지*. 함수 호출 결과가 `False`거나 raise 발생으로 `assert ... is True`가 `AssertionError`로 실패. |
| **거부 조건** | (a) 입력 행렬 변경 발생 — BR-16 위반(다음 항 `T-D-008`에서 단정하지만 본 TC에서도 *최소한* `id()` 비교 권장). (b) 본 테스트 파일 내 `import boundary.*` 등장 — DT-5/BR-17 위반. |

#### 특별하게 필요한 절차
1. **단정 형태** *필수*: `assert is_magic(D_STD) is True` (정확히 `is True` — `truthy` 대용 금지, `==` 비교는 PEP8 E712 위반).
2. **Boundary 미참조** *필수*: 본 테스트는 `from magicsquare.boundary ...` import를 *절대* 포함하지 않음 (DT-5, NFR-09).
3. **결정성·부작용은 본 TC에서 미검증**: 결정성 = `T-D-009`, 부작용 = `T-D-008`이 별도 보호. 본 RED는 *단일 동작*(D-Std → true)만 담음 (`.cursorrules` `red_phase.rules` 두 번째).
4. **DT-6**: 단일 커밋. 권장 메시지: `test(control): T-D-001 expects true for D-Std (RED)`.
5. **DT-1 짝**: §4.1 `T-U-001`과 같은 작업 세션 안에 *다른 커밋*으로 작성.
6. docstring에 `보호 BR: BR-06 / 보호 AC: AC-04-01 / 보호 Invariant: I4 / Track: B(Domain)` 명시.

---

## 5. 후속 카탈로그 (4-섹션 압축 표)

> 모든 행의 *공통 환경*은 §2가 일괄 적용. *환경 차이* 컬럼에는 §2와 다른 점만 기재. *전제·기준·절차*는 4-섹션 양식의 압축 표현.

### 5.1 `InputValidator` (FR-01, Track A) — `T-U-*` 시리즈

| TC ID | 환경 차이 | 전제 조건 | 성공/실패 기준 | 특별 절차 |
|---|---|---|---|---|
| `T-U-002` | 동일 | `matrix = 5행 4열` | `ShapeError` + `"Input must be a 4x4 matrix."` byte-equal | Mock `.assert_not_called()`. AC-01-01 |
| `T-U-003` | 동일 | `matrix[1] = [1,2,3]` (한 행만 3열) | `ShapeError` + 동일 메시지 | AC-01-02 |
| `T-U-004` | 동일 | `matrix[0] = [1,2,3,4,5]` (한 행만 5열) | `ShapeError` + 동일 메시지 | AC-01-02 |
| `T-U-005` | 동일 | `matrix = []` (빈 배열) | `ShapeError` | 코너 케이스. `len()==0` 보호 |
| `T-U-010` | 동일 | D-Std에서 (1,1)을 `-1`로 변경, 다른 곳에 빈칸 2개 배치 | `ValueRangeError` + `"Each cell must be 0 or an integer in [1, 16]."` byte-equal + `locus == (1,1)` (1-index) | AC-01-03. 메시지에 `-1` 값 *금지* 삽입 (PT-7) |
| `T-U-011` | 동일 | 어떤 셀이 `17` | `ValueRangeError` + 동일 메시지 | AC-01-04 |
| `T-U-012` | 동일 | 어떤 셀이 `100` | 동일 | 큰 값 보호 |
| `T-U-013` | 동일 | 두 군데 `-1` 동시 | `locus == (첫 row-major 위반 좌표)` | row-major 결정성 |
| `T-U-020` | 동일 | D-Std 그대로 (빈칸 0개) | `BlankCountError` + `"Input must contain exactly 2 blanks (zeros)."` byte-equal | AC-01-05 |
| `T-U-021` | 동일 | 빈칸 1개 | 동일 | |
| `T-U-022` | 동일 | 빈칸 3개 | 동일 | |
| `T-U-023` | 동일 | 빈칸 4개 | 동일 | |
| `T-U-030` | 동일 | 0이 아닌 값 중 `7`이 두 번 + 빈칸 2개 | `DuplicateError` + `"Non-zero values must be unique."` byte-equal | AC-01-06 |
| `T-U-031` | 동일 | `7`이 세 번 등장 | 동일 | 카운트 ≥2 모두 거부 |
| `T-U-032` | 동일 | `7`이 두 번 등장하되 *빈칸은 정확히 2개*, 형태/범위 모두 OK | 동일. **0 두 개**는 *허용*(중복 아님) | I3 정의 보호 |
| `T-U-040` | 동일 | 3행 4열 + 어떤 셀 `-1` | **`ShapeError`** (E_SHAPE 우선) | AC-01-07, BR-19, R-7 |
| `T-U-041` | 동일 | 어떤 셀 `-1` + 빈칸 5개 | **`ValueRangeError`** | AC-01-08 |
| `T-U-042` | 동일 | 빈칸 5개 + `7` 중복 2회 | **`BlankCountError`** | AC-01-09 |
| `T-U-050` | Domain Mock 의무 | D-In-A — 모든 검증 통과 | Mock이 **정확히 1회** 호출됨(`mock.call_count == 1`), 결과는 변형 없이 그대로 반환 | AC-01-10. DT-4 |
| `T-U-051` | 동일 | 형태 위반 | Mock **0회** 호출 | AC-01-11 |
| `T-U-052` | 동일 | D-In-A → Mock이 `[1,1,1,4,4,16]` 반환 | 반환값이 `[1,1,1,4,4,16]`과 byte-equal — 변형 *없음* | 패스스루 무결성 |
| `T-U-060` | 동일 | Mock이 `UnsolvableError("...")` raise | Boundary가 *가공·교체 없이* 동일 예외 그대로 propagate | BR-14, AC-05-04 |
| `T-U-061` | 동일 | 동일 | 메시지 byte-equal: `"No valid magic square completion exists for the given input."` | NFR-07 |
| `T-U-070` | 동일 | Mock이 `[r1,c1,n1,r2,c2,n2]` 반환 | `len(result) == 6` | BR-09, AC-05-05 |
| `T-U-071` | 동일 | 동일 | 좌표 모두 `1..4` (1-index, 0 누설 금지) | BR-08, AC-05-05, PT-1 |
| `T-U-072` | 동일 | 동일 | row-major 순서: `(r1,c1) < (r2,c2)` | AC-05-07 |
| `T-U-073` | 동일 | 동일 | `n1 != n2` | BR-18, AC-05-06 |
| `T-U-074` | 동일 | 동일 | `{n1, n2} ⊆ {1..16}` | BR-18, AC-05-06 |

### 5.2 `BlankFinder` (FR-02, Track B) — `T-D-010~014`

| TC ID | 환경 차이 | 전제 조건 | 성공/실패 기준 | 특별 절차 |
|---|---|---|---|---|
| `T-D-010` | DT-5 (Boundary 미호출) | 같은 행 두 빈칸: D-Std에서 (2,1)·(2,4)를 0으로 | `find_blanks(board) == BlankPair(first=(2,1), second=(2,4))` (1-index, `c1<c2`) | AC-02-01. 0-index 누설 *금지* (PT-1) |
| `T-D-011` | 동일 | 다른 행: (1,1)·(4,4) 0 | `BlankPair((1,1),(4,4))` | AC-02-02 |
| `T-D-012` | 동일 | 인접: (2,3)·(2,4) 0 | `BlankPair((2,3),(2,4))` | 인접 보호 |
| `T-D-013` | 동일 | (3,1)·(1,4) 0 | `first=(1,4), second=(3,1)` (row-major *첫* 0이 (1,4)) | AC-02-04, R-6 (PT-2 column-major 회피) |
| `T-D-014` | 동일 | 좌상단 (1,1) 빈칸 | 좌표가 `(1,1)`로 반환 (절대 `(0,0)` 아님) | AC-02-03, PT-1 |

### 5.3 `MissingNumberFinder` (FR-03, Track B) — `T-D-020~023`

| TC ID | 환경 차이 | 전제 조건 | 성공/실패 기준 | 특별 절차 |
|---|---|---|---|---|
| `T-D-020` | DT-5 | 1과 16이 누락된 격자 | `MissingPair(small=1, large=16)` | AC-03-01, 경계값 |
| `T-D-021` | 동일 | 7과 8 누락 | `MissingPair(7, 8)` | AC-03-02, 인접 |
| `T-D-022` | 동일 | 발견 순서가 (12, 3)이라도 | `MissingPair(small=3, large=12)` (오름차순) | AC-03-03, BR-18 |
| `T-D-023` | 동일 | 동일 입력 | 100회 호출 모두 동일 결과 | AC-03-05, BR-15 (`for _ in range(100): assert ...`) |

### 5.4 `MagicSquareJudge` (FR-04, Track B) — `T-D-002~009`

| TC ID | 환경 차이 | 전제 조건 | 성공/실패 기준 | 특별 절차 |
|---|---|---|---|---|
| `T-D-002` | DT-5 | D-Std를 90° 회전한 격자 (모든 합 여전히 34) | `is_magic == True` | AC-04-01 (회전 변형) |
| `T-D-003` | 동일 | 1행 합이 33이 되도록 임의 두 셀 swap | `False` | AC-04-02 |
| `T-D-004` | 동일 | 2열 합이 35가 되도록 변형 | `False` | AC-04-03 |
| `T-D-005` | 동일 | 주대각만 합 ≠ 34 (행/열/부대각 모두 34) | `False` | AC-04-04 |
| `T-D-006` | 동일 | 부대각만 합 ≠ 34 | `False` | AC-04-05 |
| `T-D-007` | 동일 | 모든 합이 34 *이지만* 한 값(예: `1`)이 4회 반복 | `False` | AC-04-06, I3, PT-6 (multiset 단정) |
| `T-D-008` | 동일 | D-Std (호출 전 `board_before = copy.deepcopy(board)`) | 호출 후 `board == board_before` (byte-equal) | AC-04-08, BR-16, NFR-04 |
| `T-D-009` | 동일 | D-Std | 100회 호출 모두 `True` 동일 | AC-04-07, BR-15, NFR-03 |

### 5.5 `FillPlanResolver` + `MagicResultAssembler` (FR-05, Track B) — `T-D-030~042`, `T-D-050~052`

| TC ID | 환경 차이 | 전제 조건 | 성공/실패 기준 | 특별 절차 |
|---|---|---|---|---|
| `T-D-030` | DT-5, FR-04는 *실제 함수* 사용 가능 | D-In-A — (1,1)·(4,4) 0, missing=(1,16), 시도 A 마방진 ✓ | 결과의 `(n1,n2) == (1, 16)` (small→첫, large→둘) | AC-05-01, BR-10·12 |
| `T-D-031` | 동일 | **D-In-B** (PRD §11 R-2 미확정) | 결과 `(n1,n2) == (large, small)` | AC-05-02, BR-11·13. **`@pytest.mark.xfail(reason="R-2 D-In-B unsealed")`** (TASK-002 종결 시 해제) |
| `T-D-032` | 동일 | **D-Uns** (R-2 미확정) | `pytest.raises(UnsolvableError)` + `"No valid magic square completion exists for the given input."` byte-equal | AC-05-04, BR-14, R-1. xfail 동일 |
| `T-D-040` | 동일 | BlankPair=((1,1),(4,4)), nums=(1,16) | Assembler 출력 `[1,1,1,4,4,16]` (정확히 6개) | AC-05-05, BR-09 |
| `T-D-041` | 동일 | BlankPair=((2,3),(3,1)) | row-major 순서 보존: `(2,3)` 먼저 | AC-05-07, BR-07 |
| `T-D-042` | 동일 | 임의 정답 입력 | 좌표 모두 `1..4` | AC-05-05, BR-08 |
| `T-D-050` | DT-5, 오케스트레이션 End-to-End | D-In-A | `solve(board) == [1,1,1,4,4,16]` | AC-05 전체 |
| `T-D-051` | 동일 | D-In-A | 100회 호출 모두 동일 결과 (또는 D-Uns의 경우 동일 예외) | AC-05-09, BR-15 |
| `T-D-052` | 동일 | D-Uns | `UnsolvableError`만 raise (다른 코드 *금지*) | AC-05-04 |

### 5.6 통합 시나리오 (PRD §9.1) — `TC-N-* / TC-F-* / TC-P-*`

| TC ID | 환경 차이 | 전제 조건 | 성공/실패 기준 | 특별 절차 |
|---|---|---|---|---|
| `TC-N-01` | Boundary→Domain End-to-End (Mock 없음) | D-In-A | `[1,1,1, 4,4,16]` byte-equal | PRD §9.1.1 |
| `TC-N-02` | 동일 | D-Std에서 (2,1)·(2,4) 0 | `[2,1,5, 2,4,8]` | 같은 행 |
| `TC-N-03` | 동일 | D-In-B | (n1,n2)=(large,small) 순서 | xfail (R-2 대기) |
| `TC-N-04` | 동일 | D-Std에서 (1,1)과 (2,3) 0 | 정상 `int[6]` (구체값은 입력으로 결정) | 주대각 위 빈칸 |
| `TC-N-05` | 동일 | D-Std에서 (4,1)과 (3,3) 0 | 정상 `int[6]` | 부대각 위 빈칸 |
| `TC-F-01` | 동일 | 3행 4열 | `E_SHAPE` + 표준 메시지 | PRD §9.1.2 |
| `TC-F-02` | 동일 | 한 행만 5열 | `E_SHAPE` | |
| `TC-F-03` | 동일 | 어떤 셀이 `-1` | `E_VALUE_RANGE` + `locus` (1-index) | |
| `TC-F-04` | 동일 | 어떤 셀이 `17` | `E_VALUE_RANGE` | |
| `TC-F-05` | 동일 | 모든 셀 채워짐(빈칸 0) | `E_BLANK_COUNT` | |
| `TC-F-06` | 동일 | 정확히 한 개의 0 | `E_BLANK_COUNT` | |
| `TC-F-07` | 동일 | 정확히 세 개의 0 | `E_BLANK_COUNT` | |
| `TC-F-08` | 동일 | `7`이 두 번 등장 + 빈칸 2개 | `E_DUPLICATE` | |
| `TC-F-09` | 동일 | D-Uns | `E_UNSOLVABLE` + 표준 메시지 | xfail (R-2 대기) |
| `TC-P-01` | 동일 | 형태 + 값 범위 동시 위반 | **`E_SHAPE`** | BR-19, AC-01-07 |
| `TC-P-02` | 동일 | 값 + 빈칸 동시 위반 | **`E_VALUE_RANGE`** | AC-01-08 |
| `TC-P-03` | 동일 | 빈칸 + 중복 동시 위반 | **`E_BLANK_COUNT`** | AC-01-09 |

### 5.7 불변 / Property 회귀 — `T-INV-*`, `P-01~08`

| TC ID | 환경 차이 | 전제 조건 | 성공/실패 기준 | 특별 절차 |
|---|---|---|---|---|
| `T-INV-I1` | 마커 `@pytest.mark.invariant` | Domain 진입 시점 격자 | 4x4 사전조건 가드 단정 (debug-mode `assert` 가능) | PRD §8.2.2 |
| `T-INV-I2` | 동일 | 채움 시뮬레이션 후 격자 | 모든 셀 ∈ `{1..16}` | |
| `T-INV-I3` | 동일 | 채움 후 격자 | 16개 셀이 `{1..16}` 다중집합과 정확히 일치 | |
| `T-INV-I4` | 동일 | FR-04가 `true` 반환한 격자 | 행/열/대각 10개 합 모두 `34` | |
| `T-INV-I5` | 동일 | 임의 정상 입력 1건 | `solve()` 100회 동일 결과 | OG-7 |
| `T-INV-BR16` | 동일 | 임의 정상 입력 (호출 전 `deepcopy`) | 호출 후 입력 byte-equal | OG-8 |
| `P-01~08` | `hypothesis` (opt-strict, 별도 PR) | Hypothesis strategy로 합법 4x4 격자 생성 | PRD §9.4 P-01~08 모두 통과 | OG-11, OPS-3 (TASK-091) |

---

## 6. 진행 권고 (Workflow)

### 6.1 현 단계 (`red` 브랜치) 직접 작업 순서

| 순서 | 행동 | 권장 커밋 메시지 |
|---|---|---|
| ① | `entity/exceptions.py`에 5종 예외 클래스의 *최소 stub*만 추가 (단지 `class XxxError(Exception): pass` 수준) — `T-U-001` 컬렉션 실패 회피용 | `chore(entity): add minimal exception stubs to enable RED collection` |
| ② | `tests/control/test_magic_square_judge.py` + §4.2 `T-D-001` 작성 → `pytest -m domain` 실행해 *RED 확인* | `test(control): T-D-001 expects true for D-Std (RED)` |
| ③ | `tests/boundary/test_input_validator.py` + §4.1 `T-U-001` 작성 → `pytest -m boundary` 실행해 *RED 확인* | `test(boundary): T-U-001 expects E_SHAPE for 3-row input (RED)` |
| ④ | DT-1 짝 닫힘 → 다음 사이클은 GREEN (DT-2). 본 카탈로그의 `T-U-002~`, `T-D-002~`는 *후속 RED*들이며, 추가할 때마다 본 문서를 *함께 갱신* (NFR-08) | (추가 RED마다 별도 커밋) |

> ① 단계는 *코드*이지만 *RED를 가능케 하는 골격*에 불과하며 어떤 비즈니스 로직도 포함하지 않는다. `.cursorrules` `red_phase.must_not` 두 번째(컴파일 에러를 RED로 간주 금지)를 *회피하기 위한 메타 작업*으로 정당화된다.

### 6.2 본 문서의 갱신 정책

| 사건 | 갱신 대상 | 정합성 |
|---|---|---|
| 새 RED 추가 | §5 해당 그룹의 표에 한 행 추가, docstring과 본 표의 *기준* 컬럼이 byte-equal | NFR-08, OG-12 (미래) |
| PRD §0/§6/§12 변경 | 본 문서의 *모든 영향 행* 동시 갱신 | PRD `Frozen` 영역 — 사실상 발생 금지 |
| TASK-002 종결 (R-2) | §5.5의 `T-D-031`/`T-D-032`, §5.6의 `TC-N-03`/`TC-F-09`의 xfail 마커 *제거* | PRD §11.3 R-2 |
| 메시지 변경 (NFR-07) | §2.1 표 + §5의 모든 byte-equal 단정 행 동시 갱신 | OPS-2 (NFR 약화 금지) |

---

## 7. 추적 매트릭스 (TC ID → PRD §12 행 → 보호 BR)

> 본 표는 PRD §12 매트릭스의 *역방향 인덱스*다. *임의 TC → 보호 BR/AC/Component*를 30초 내 역추적할 수 있어야 한다(NFR-08, US-003).

| TC ID 그룹 | PRD §12 행 | 주된 보호 BR | Component |
|---|---|---|---|
| `T-U-001~005` | 행 1 (I1) | BR-01 | Boundary / `InputValidator` |
| `T-U-010~013` | 행 2 (I2) | BR-02 | Boundary / `InputValidator` |
| `T-U-020~023` | 행 1 (I1 보강) | BR-03 | Boundary / `InputValidator` |
| `T-U-030~032` | 행 3 (I3 입력측) | BR-04 | Boundary / `InputValidator` |
| `T-U-040~042` | 행 13 (I5 우선순위) | BR-19 | Boundary / `InputValidator` |
| `T-U-050~052` | 행 5·12 (DIP·출력) | AC-01-10·11 | Boundary / `InputValidator` |
| `T-U-060~061` | 행 9 (I4 실패 식별성) | BR-14 | Boundary 통과 + Domain |
| `T-U-070~074` | 행 12 (I5 출력 좌표) | BR-08·09·18 | Boundary 출력 보존 |
| `T-D-001~009` | 행 6 (I4 합 균질) | BR-05·06 | Domain / `MagicSquareJudge` |
| `T-D-010~014` | 행 5 (I1 스캔 순서) | BR-07 | Domain / `BlankFinder` |
| `T-D-020~023` | 행 4 (I3 누락측) | BR-18 | Domain / `MissingNumberFinder` |
| `T-D-030~032` | 행 7·8·9 (I4 시도 A/B/실패) | BR-10~14 | Domain / `FillPlanResolver` |
| `T-D-040~042` | 행 12 (I5 출력 좌표) | BR-08·09 | Domain / `MagicResultAssembler` |
| `T-D-050~052` | 행 10 (I5 결정성) | BR-15 | Domain / 오케스트레이션 |
| `TC-N-01~05` | 행 7·8 (시도 A/B) | BR-10~13 | 통합 |
| `TC-F-01~09` | 행 1~3·9 | BR-01~04·14 | 통합 |
| `TC-P-01~03` | 행 13 (I5 우선순위) | BR-19 | Boundary |
| `T-INV-I1~I5` | 행 1·2·3·6·10 | I1~I5 | 전 도메인 |
| `T-INV-BR16` | 행 11 (I5 부작용) | BR-16 | 전 도메인 |
| `P-01~08` | 행 12·11·10·6 | BR-06~09·15·16·18·19 | 통합 (Hypothesis) |

---

## 8. 변경 로그

| 날짜 | 변경 | 근거 |
|---|---|---|
| 2026-04-28 | 초기 카탈로그 신설 — DT-1 한 쌍(§4) 상세 + 후속 카탈로그(§5) + 추적 매트릭스(§7) | `red` 브랜치, 사용자 요청 |

---

## 부록 A. 본 문서가 후속 단계에 부과하는 제약

| 후속 단계 | 본 문서가 부과한 제약 |
|---|---|
| **RED 테스트 작성** | 모든 새 RED는 (a) 본 문서 §5의 해당 그룹에 *한 행 추가* + (b) 테스트 docstring에 `보호 BR / 보호 AC / Track` 명시 + (c) PRD §12 매트릭스와의 정합 확인. |
| **GREEN 구현** | 본 문서의 *기준* 컬럼을 *변경하지 않고* 통과시키는 최소 구현만 작성. byte-equal 메시지·1-index·row-major·결정성·부작용 금지를 모두 보존. |
| **REFACTOR** | 본 문서의 *어떤 행*도 변경하지 않는다. 행 변경이 필요하면 *별도 PR*로 분리. |
| **PR 리뷰** | 본 문서의 갱신과 코드 변경이 *같은 PR* 안에 있어야 함 (NFR-08 traceability). |
| **TASK-002 종결 시** | §2.2·§5.5·§5.6의 xfail 마커를 *동일 PR*에서 일괄 제거. |
