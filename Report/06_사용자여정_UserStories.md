# 4x4 Magic Square — 사용자 여정 Level 3 (User Stories) 보고서

> ⚠️ 본 문서는 사용자 여정 3계층 중 **Level 3 (User Stories)** 만을 다룹니다.
> Level 1(Epic, `04`)이 *왜*, Level 2(Journey, `05`)가 *누가·어떤 시간 순서로* 를 닫았다면, 본 단계는 *어떤 가치 단위가, 어떤 검증 가능한 기준 아래에서, 어느 ECB 계층에서 충족되는가*를 닫습니다.
> RED 테스트 작성과 production 코드는 본 문서 *이후* 단계의 책무이며, 본 문서는 *그 산출물들이 어떤 Story의 어떤 AC를 만족시켜야 하는지*를 외부화합니다.

---

## 문서 메타데이터

| 항목 | 내용 |
|---|---|
| 문서 ID | `06_사용자여정_UserStories` |
| 단계 | User Journey — Level 3 (User Stories / Value Units) |
| 선행 문서 | `01_문제_정의`, `02_설계`, `03_프로젝트_규약_정의`, `04_사용자여정_Epic`, `05_사용자여정_Journey` |
| 후행 단계 | RED 테스트 작성 → GREEN 구현 → REFACTOR (Implementation Phase) |
| 산출물 형식 | Markdown 보고서 (코드 없음) |
| 학습 초점 | *가치 단위로의 분해* / *AC의 검증 가능성 환원* / *Story ↔ Test ID ↔ Invariant의 3중 추적* |

---

## 0. 본 단계의 위치와 책무 (3계층 재정렬)

### 0.1 3계층의 *재정렬* (Epic 작성 시점 가정 vs 현재)

| Level | `04_Epic` 작성 시점의 가정 | 현재(본 문서 시점)의 정밀화 |
|---|---|---|
| 1 | Epic — *왜* | Epic — *왜* (변경 없음) |
| 2 | User Story — *누가/무엇을/왜* | **User Journey** — *누가, 어떤 시간 순서로, 어떤 인지 부하를 통과하며* |
| 3 | Task — *어떻게* | **User Stories** — *어떤 가치 단위가 어떤 AC로 닫히는가* |

> ※ *Task*는 본 사용자 여정 분해의 *하위 단위*가 아니라, **본 문서 이후 Implementation Phase의 RED/GREEN/REFACTOR 단위**로 자리 이동했다.
> 즉, 본 프로젝트의 사용자 여정은 ***Epic(`04`) → Journey(`05`) → Stories(본 문서)*** 의 3계층으로 닫히며, 그 아래는 *여정의 분해*가 아니라 *구현의 분해*가 된다.

### 0.2 본 단계가 *해야 하는 것*

- 사용자가 제시한 5개 Story를 **표준 As-A / I-Want / So-That + AC** 형식으로 외부화한다.
- 모든 AC를 *D-x 술어* 또는 *byte-equal 진술*로 환원하고, `02_설계`의 기존 Test ID에 1:1 매핑한다.
- Story 간 의존 DAG를 외부화하여, RED 작성 우선순위를 결정적으로 정렬한다.

### 0.3 본 단계가 *하지 않는 것*

- 코드/테스트의 *작성* — 본 문서 이후 Implementation Phase의 책무.
- 새로운 AC의 *발명* — 사용자 제시 AC를 *환원*만 하며, 추가 AC가 필요하면 그 자체를 *역행 사유*로 기록한다 (`05_Journey` 8.2).
- 새로운 Persona의 *추가* — 본 프로젝트는 단일 페르소나(`05_Journey` 1.1)로 고정.

---

## 1. User Story 작성 메타-규약

> 본 단계의 모든 Story는 아래 3종 메타-규약을 *동시에* 만족해야 한다. 한 항목이라도 위반하면 그 Story는 *Story가 아니다*.

### 1.1 INVEST 원칙 적용

| 약자 | 원칙 | 본 프로젝트에서의 환원 |
|---|---|---|
| **I**ndependent | 독립성 | 다른 Story의 *내부 동작*을 모르고도 단독 검증 가능. 단, 입출력 *계약*은 공유 가능 (`02_설계` 0절). |
| **N**egotiable | 협상 가능성 | AC는 byte-equal 수준의 *고정* 영역과, 구현 방식의 *자유* 영역을 분리한다. |
| **V**aluable | 가치 | 모든 Story는 `04_Epic` 2절의 P1~P4 중 *최소 하나*에 매핑된다. |
| **E**stimable | 추정 가능성 | 모든 Story는 사이즈(S/M/L) 추정이 가능한 *유한 AC* 수를 갖는다. |
| **S**mall | 소형성 | 한 Story의 AC 개수는 *4개 이하*를 권장. 그 이상이면 분할 후보. |
| **T**estable | 검증 가능성 | 모든 AC는 `02_설계`의 D-x 술어 또는 표준 메시지 byte-equal 진술로 *환원되어야* 한다. |

### 1.2 Story ID 부여 규약

| 형식 | 의미 |
|---|---|
| `US-N` | N번째 User Story (예: `US-1`, `US-2`) |
| `AC-N.M` | `US-N`의 M번째 Acceptance Criterion (예: `AC-1.3`) |
| `DoD-N` | `US-N`의 Definition of Done 항목 집합 |

### 1.3 AC의 *검증 가능성* 환원 규약

| 모호 어휘 (금지) | 검증 가능 환원 (요구) |
|---|---|
| *"예외"* | 정확한 에러 코드 (예: `E_SHAPE`) + `02_설계` 2.4의 표준 메시지 byte-equal |
| *"동일"* | 동일성의 대상 명시 (예: `∀ row r: sum(r) == 34`) |
| *"정확히 N개"* | `count(...) == N` 형태의 카디널리티 술어 |
| *"순서대로"* | 순서 기준 명시 (예: `row-major scan order`, `오름차순`) |
| *"적절히/충분히"* | 즉시 환원 거부 — *정확히 무엇이?* 로 다시 진술 (`05_Journey` Anti-Persona A-4) |

> ※ 본 규약을 만족하지 못하는 AC는 *AC가 아니라 합의의 결함*이다 (`05_Journey` 8.2의 역행 사유).

---

## 2. Story 1 — 입력 검증 (Input Validation)

### 2.1 표준 진술

> **As a** 학습자
> **I want to** 입력이 정확히 4x4인지 검증되길 원한다
> **So that** 잘못된 데이터가 Domain으로 전달되지 않도록 한다

### 2.2 Acceptance Criteria (사용자 원본 ↔ 검증 가능 환원)

| AC ID | 사용자 원본 | 검증 가능 환원 (D-x / byte-equal) | 에러 코드 | 매핑 Test ID |
|---|---|---|---|---|
| `AC-1.1` | 4x4가 아니면 예외 | D1: `rows == 4 ∧ ∀r: cols(r) == 4` 위반 시 차단 + `"Input must be a 4x4 matrix."` byte-equal | `E_SHAPE` | `T-U-001`~`T-U-005`, `T-I-010` |
| `AC-1.2` | 빈칸 2개 아니면 예외 | D4: `count(cell == 0) == 2` 위반 시 차단 + `"Input must contain exactly 2 blanks (zeros)."` byte-equal | `E_BLANK_COUNT` | `T-U-020`~`T-U-023`, `T-I-011` |
| `AC-1.3` | 중복 숫자 예외 | D3: `multiset(cell ≠ 0)` 내 중복 위반 시 차단 + `"Non-zero values must be unique."` byte-equal | `E_DUPLICATE` | `T-U-030`~`T-U-032`, `T-I-013` |
| `AC-1.4` | 범위 위반 예외 | D2: `∀ cell: cell == 0 ∨ 1 ≤ cell ≤ 16` 위반 시 차단 + `"Each cell must be 0 or an integer in [1, 16]."` byte-equal + `locus` 첫 위반 좌표 | `E_VALUE_RANGE` | `T-U-010`~`T-U-013`, `T-I-012` |

### 2.3 매핑

| 항목 | 값 |
|---|---|
| Persona Journey Step | **Step 2** (계약 정의) — 부분적으로 Step 4의 UI Track RED |
| Epic 목적 | **P3** (입력/출력 계약 명확화) — 부수적으로 P1, P2 |
| 보호 Invariant | **I1, I2, I3** (+ 빈칸 카디널리티) |
| 보호 술어 (D-x) | **D1, D2, D3, D4** |
| ECB 계층 귀속 | **Boundary** (`src/magicsquare/boundary/`) |
| 검증 순서 보호 | `02_설계` 2.2.4의 검증 순서 (1→2→3→4→5) → `T-U-040`~`T-U-042` |

### 2.4 Definition of Done (DoD-1)

- [ ] AC-1.1~1.4 모두 RED → GREEN 통과.
- [ ] 검증 순서(`T-U-040`~`T-U-042`) PASS.
- [ ] 표준 메시지 4종이 *byte-equal*로 단일 진실 출처(예: `entity/messages.py` 또는 동급 상수 모듈)에서 import.
- [ ] Domain Mock으로 *위임 직전 검증*만 수행한 테스트(`T-U-050`~`T-U-052`) PASS.

### 2.5 사이즈 / 위반 신호

| 항목 | 내용 |
|---|---|
| 사이즈 추정 | **M** (AC 4개, 검증 순서 보호 포함) |
| Story 위반 신호 | (a) 4개 AC 중 일부만 PASS인데 *Story 닫힘*으로 보고. (b) 에러 메시지가 입력 데이터(셀 값 등)를 포함 (`02_설계` M-2 위반). (c) Domain 호출이 검증 *이전*에 발생. |

---

## 3. Story 2 — 빈칸 탐색 (Blank Discovery)

### 3.1 표준 진술

> **As a** 학습자
> **I want to** `0`의 좌표를 정확히 찾고 싶다
> **So that** 조합 시도가 가능하다

### 3.2 Acceptance Criteria

| AC ID | 사용자 원본 | 검증 가능 환원 | 매핑 Test ID |
|---|---|---|---|
| `AC-2.1` | row-major 순서 유지 | D8: 행-우선 스캔 순서로 정렬된 `BlankPair{first, second}` 반환. `(first.row*4 + first.col) < (second.row*4 + second.col)`. | `T-D-013`, `T-D-014` |
| `AC-2.2` | 정확히 2개 반환 | D4: `len(BlankPair) == 2`. 입력은 D4를 만족한다고 *전제*되며 (Boundary가 사전 차단), 그렇지 않으면 사전조건 위반. | `T-D-010`~`T-D-014` |

### 3.3 매핑

| 항목 | 값 |
|---|---|
| Persona Journey Step | **Step 3** (Domain 분리) → **Step 4** (Logic Track RED) |
| Epic 목적 | **P2** (Dual-Track TDD: Logic) |
| 보호 Invariant | I1·I3·I5 (간접) |
| 보호 술어 (D-x) | **D4, D8** |
| ECB 계층 귀속 | **Entity** (`src/magicsquare/entity/`) — `BlankFinder` |
| 인지 단위 ↔ 구현 단위 | 1:1 (`05_Journey` 5.2의 `BlankFinder` 행) |

### 3.4 Definition of Done (DoD-2)

- [ ] AC-2.1, AC-2.2 모두 RED → GREEN 통과.
- [ ] 1-index 좌표 보장 (`T-D-014`).
- [ ] 좌표 자체는 `Coordinate` VO로 표현 (`02_설계` 1.1.2). 원시 튜플 직접 노출 금지.
- [ ] `BlankFinder`는 다른 Domain Service를 *호출하지 않는다* (낮은 결합도, `02_설계` 1.1.3 주석).

### 3.5 사이즈 / 위반 신호

| 항목 | 내용 |
|---|---|
| 사이즈 추정 | **S** (AC 2개, 단일 책임) |
| Story 위반 신호 | (a) 빈칸이 1개 또는 3개인 입력에서도 *조용히 결과 반환* (사전조건 위반을 검출 못 함). (b) 0-index 좌표가 외부에 노출됨. (c) `BlankFinder`가 `MissingNumberFinder`를 호출하는 등 책임 침범. |

---

## 4. Story 3 — 누락 숫자 탐색 (Missing Number Discovery)

> ※ 사용자 본문에서 As-A / I-Want / So-That 진술이 생략됨 → 일관성을 위해 *추론 진술*로 채움 (이 사실은 본 절 끝의 *추론 표시* 박스로 명시).

### 4.1 표준 진술 (추론 진술)

> **As a** 학습자
> **I want to** 격자에 들어 있지 않은 두 숫자를 정확히 찾고 싶다
> **So that** 어떤 숫자를 빈칸에 채울 후보로 삼을지 결정할 수 있다

### 4.2 Acceptance Criteria

| AC ID | 사용자 원본 | 검증 가능 환원 | 매핑 Test ID |
|---|---|---|---|
| `AC-3.1` | 1~16 중 누락 2개 | D5: `\|{1..16} \ filledValues\| == 2`, 즉 격자에 등장하지 않은 숫자가 정확히 2개. | `T-D-020`, `T-D-021` |
| `AC-3.2` | 오름차순 반환 | `MissingPair{small, large}` 형태로, `small < large` 보장. | `T-D-022` |

### 4.3 매핑

| 항목 | 값 |
|---|---|
| Persona Journey Step | **Step 3** → **Step 4** (Logic Track RED) |
| Epic 목적 | **P2**, 부수적으로 P1 (I3의 누락 측 술어화) |
| 보호 Invariant | I3 (유일성, *누락 측면*), I5 (결정성) |
| 보호 술어 (D-x) | **D5** (+ D7 결정성 보강) |
| ECB 계층 귀속 | **Entity** — `MissingNumberFinder` |
| 결정성 보호 | `T-D-023` (동일 입력 100회 반복) |

### 4.4 Definition of Done (DoD-3)

- [ ] AC-3.1, AC-3.2 모두 RED → GREEN 통과.
- [ ] 결정성 테스트 `T-D-023` PASS.
- [ ] 반환된 `MissingPair`의 `small`, `large` 명명이 `02_설계` 1.1.2의 VO 정의와 일치.
- [ ] `1`, `16`, `15`(상한 직전)와 같은 경계값 누락 케이스가 RED에 포함.

### 4.5 사이즈 / 위반 신호 / 추론 표시

| 항목 | 내용 |
|---|---|
| 사이즈 추정 | **S** (AC 2개, 단일 책임) |
| Story 위반 신호 | (a) 오름차순 보장이 *우연*인 경우 (입력 순서에 따라 깨질 수 있음). (b) 누락이 2개가 아닌 입력(빈칸 ≠ 2)에서 *조용히 잘못된 결과* 반환. |
| 추론 표시 | 본 Story의 As-A/I-Want/So-That는 사용자 본문에서 생략되었으며, `02_설계` 1.1.3 `MissingNumberFinder` 책임으로부터 *최소 추론*된 진술. 다른 합의가 있다면 본 진술은 즉시 폐기/교체 대상. |

---

## 5. Story 4 — 마방진 판정 (Magic Square Validation)

> ※ As-A / I-Want / So-That는 추론 진술 (Story 3과 동일 사유).

### 5.1 표준 진술 (추론 진술)

> **As a** 학습자
> **I want to** 채워진 격자가 마방진인지 결정적으로 판정하고 싶다
> **So that** 두 조합 중 어느 쪽이 정답인지 식별할 수 있다

### 5.2 Acceptance Criteria

| AC ID | 사용자 원본 | 검증 가능 환원 | 매핑 Test ID |
|---|---|---|---|
| `AC-4.1` | 모든 행 합 동일 | D6 부분: `∀ row r ∈ {1..4}: sum(r) == 34` (Magic Constant `M=34`, `02_설계` 0.3) | `T-D-001`, `T-D-003` |
| `AC-4.2` | 모든 열 합 동일 | D6 부분: `∀ col c ∈ {1..4}: sum(c) == 34` | `T-D-001`, `T-D-004` |
| `AC-4.3` | 대각선 동일 | D6 부분: `sum(diag↘) == 34 ∧ sum(diag↙) == 34` (주대각·부대각 모두) | `T-D-005`, `T-D-006` |

### 5.3 매핑

| 항목 | 값 |
|---|---|
| Persona Journey Step | **Step 3** → **Step 4** (Logic Track RED) |
| Epic 목적 | **P1** (Invariant 중심), **P2** (Logic Track) |
| 보호 Invariant | **I4** (합 균질 불변성) — *마방진의 본질* |
| 보호 술어 (D-x) | **D6** (전체) |
| ECB 계층 귀속 | **Entity** — `MagicSquareValidator` (인지 단위) ≡ `MagicSquareJudge` (구현 단위) |
| 부수 보호 | I3 (`T-D-007`: 합은 34지만 중복 → `false`), I5 (`T-D-009`: 결정성 100회) |

### 5.4 Definition of Done (DoD-4)

- [ ] AC-4.1~4.3 모두 RED → GREEN 통과.
- [ ] 빈칸이 있는 입력에 대한 호출은 *사전조건 위반*으로 즉시 차단(`02_설계` 1.4 주석). 디버그 모드 `assert` 허용.
- [ ] 회전 변형(`T-D-002`)·결정성(`T-D-009`)·경계 셀(`T-D-008`) 케이스가 RED에 포함.
- [ ] `M=34` 상수가 `entity/`의 `Final` 상수(예: `MAGIC_CONSTANT`)에서 import (SC-4 보호).

### 5.5 사이즈 / 위반 신호

| 항목 | 내용 |
|---|---|
| 사이즈 추정 | **M** (AC 3개, 회귀 보호 케이스 포함 시 RED 9건 이상) |
| Story 위반 신호 | (a) `34`가 코드에 직접 박힘(SC-4 위반). (b) 행만 검증하고 열·대각이 누락된 채 GREEN 보고. (c) `T-D-007`(합은 34지만 중복) 케이스가 RED에 누락 — *합 충족 ≠ 마방진* 명제의 외부화 실패. |

---

## 6. Story 5 — 두 조합 시도 (Two-Combination Solver)

> ※ As-A / I-Want / So-That는 추론 진술. 또한 `Solver`는 `05_Journey` 5.2의 매핑에 따라 *인지 단위 1개 ↔ 구현 단위 2개*(`FillPlanResolver` + `MagicResultAssembler`)임을 본 Story가 명시 처리한다.

### 6.1 표준 진술 (추론 진술)

> **As a** 학습자
> **I want to** 두 누락 숫자를 두 빈칸에 두 가지 순서로 시도하고 싶다
> **So that** 항상 마방진을 만드는 결정적 채움 계획을 산출하고, 그 결과를 `int[6]`으로 반환할 수 있다

### 6.2 Acceptance Criteria

| AC ID | 사용자 원본 | 검증 가능 환원 | 매핑 Test ID |
|---|---|---|---|
| `AC-5.1` | small → first blank 시도 | D9 + F-1~F-4: `FillPlan_A = (first→missing.small, second→missing.large)` 채움 → `MagicSquareValidator.isMagic == true`이면 채택. | `T-D-030` |
| `AC-5.2` | 실패 시 reverse | D9 + F-5~F-8: A 실패 시 `FillPlan_B = (first→large, second→small)` 시도. B도 실패 시 D10에 의해 `E_UNSOLVABLE`. | `T-D-031`, `T-D-032`, `T-I-014` |
| `AC-5.3` | 정답 배열 길이 6 | D8: 출력은 `[r1, c1, n1, r2, c2, n2]` 형태의 `int[6]`. 좌표 1-index, `r1, c1, r2, c2 ∈ {1..4}`, `n1, n2 ∈ {1..16}`, `n1 ≠ n2`. | `T-D-040`~`T-D-042`, `T-U-070`~`T-U-074` |

### 6.3 매핑

| 항목 | 값 |
|---|---|
| Persona Journey Step | **Step 3** → **Step 4** (Logic Track RED) → **Step 5** (회귀 보호 D10) |
| Epic 목적 | **P2**, **P3** (출력 포맷 byte-equal) |
| 보호 Invariant | I4(간접), I5(결정성), 그리고 *실패 식별성* |
| 보호 술어 (D-x) | **D9** (순서 규칙), **D10** (풀이 가능성 / `E_UNSOLVABLE`), **D8** (출력 좌표 일관성) |
| ECB 계층 귀속 | **Control** (`src/magicsquare/control/`) — 흐름 조율 책임 (`05_Journey` 5.4) |
| 인지 단위 ↔ 구현 단위 | **1 : 2** — `Solver`(인지) = `FillPlanResolver`(조합 결정) + `MagicResultAssembler`(int[6] 조립) |

### 6.4 Definition of Done (DoD-5)

- [ ] AC-5.1~5.3 모두 RED → GREEN 통과.
- [ ] 두 조합 모두 비-마방진 케이스(`T-D-032`, `T-I-014`)에서 `E_UNSOLVABLE` 발생 + 표준 메시지 `"No valid magic square completion exists for the given input."` byte-equal.
- [ ] 출력 `int[6]`의 길이 불변성 테스트(`T-D-042`) PASS.
- [ ] Boundary가 `E_UNSOLVABLE`을 *다른 코드로 가리지 않음*(`T-U-060`, `T-U-061`) PASS.
- [ ] End-to-end 결정성 테스트(`T-D-051`) PASS.

### 6.5 사이즈 / 위반 신호

| 항목 | 내용 |
|---|---|
| 사이즈 추정 | **L** (AC 3개 + 인지/구현 1:2 + 도메인 실패 처리) |
| Story 위반 신호 | (a) 조합 A가 정답일 때 *우연히* B도 시도 후 비교 — *결정성/순서 규칙(D9) 위반*. (b) `E_UNSOLVABLE`을 `E_DUPLICATE` 등 다른 코드로 가림 (`T-U-061` 위반). (c) `int[6]`이 아닌 길이로 반환 (`T-D-042` 위반). (d) 조립 책임(`MagicResultAssembler`)을 `FillPlanResolver`에 섞어 SRP 위반. |

---

## 7. Story 간 의존 관계 매트릭스 (DAG)

> Story 간 의존은 *런타임 호출 의존*이 아니라 *RED 작성 가능성 의존*이다. 즉, 어떤 Story의 RED를 의미 있게 작성하려면 어떤 Story의 AC가 먼저 외부화되어야 하는가.

```
US-1 (입력 검증, Boundary)
   │  (Boundary가 D1~D4를 사전 차단)
   ▼
US-2 (빈칸 탐색)         US-3 (누락 숫자 탐색)
   │                    │
   └─────────┬──────────┘
             ▼
        US-4 (마방진 판정)
             │
             ▼
        US-5 (두 조합 시도)
        = FillPlanResolver + MagicResultAssembler
```

| 의존 | 형태 | 의미 |
|---|---|---|
| US-1 → US-{2..5} | **약** | Boundary가 D1~D4를 사전 차단하므로, Domain Service는 *D1~D4를 다시 검증하지 않는다* (방어적 검증 중복 금지, `02_설계` 1.4 주석). |
| US-2, US-3 → US-5 | **강** | Solver는 빈칸 좌표 + 누락 숫자 두 입력을 *동시에* 받아 채움 계획을 결정. |
| US-4 → US-5 | **강** | Solver의 *조합 채택 판정*은 `MagicSquareValidator.isMagic` 호출에 의존 (F-3, F-7). |
| US-2, US-3, US-4 ↔ 서로 | **무관** | 세 Story는 서로의 내부를 모르고, 각자 단독으로 RED → GREEN 가능. |

> ※ DAG의 *루트*는 US-1, *리프*는 US-5이다. US-5의 RED는 US-1~US-4의 GREEN을 *전제*하지 않지만, US-5의 *통합 검증*(`T-I-XXX`)은 모두의 GREEN을 전제한다.

---

## 8. 기존 산출물(`02_설계` Test ID)과의 매핑 요약

| Story | Domain 테스트 (`T-D-XXX`) | UI 테스트 (`T-U-XXX`) | 통합 테스트 (`T-I-XXX`) |
|---|---|---|---|
| US-1 | — | T-U-001~005, 010~013, 020~023, 030~032, 040~042, 050~052 | T-I-010~013 |
| US-2 | T-D-010~014 | — | (간접: T-I-001~003) |
| US-3 | T-D-020~023 | — | (간접: T-I-001~003) |
| US-4 | T-D-001~009 | — | (간접: T-I-001~003) |
| US-5 | T-D-030~034, 040~042, 050~052 | T-U-060, 061, 070~074 | T-I-001~003, 014 |

> ※ 빈 셀(`—`)은 *그 계층의 테스트가 해당 Story에 직접 매핑되지 않음*을 의미한다 (예: US-2는 Boundary 테스트와 직접 매핑 없음 — Boundary는 US-1이 전담).

---

## 9. 선행 문서와의 정합성 매트릭스

| 본 문서 항목 | 선행 문서 위치 | 정합성 |
|---|---|---|
| 0.1 3계층 재정렬 | `04_Epic` 0.1, `05_Journey` 0.1 | ✅ (정밀화 명시) |
| 1.1 INVEST + 1.3 환원 규약 | `03_프로젝트_규약_정의` `forbidden`, `ai_behavior.honesty` | ✅ |
| US-1 (AC + 매핑) | `02_설계` 0.4, 2.2, 2.4 | ✅ |
| US-2 (D4, D8) | `02_설계` 1.4 (`BlankFinder`), 1.5.2 | ✅ |
| US-3 (D5) | `02_설계` 1.4 (`MissingNumberFinder`), 1.5.3 | ✅ |
| US-4 (D6, M=34) | `02_설계` 0.3, 1.4 (`MagicSquareJudge`), 1.5.1 | ✅ |
| US-5 (D9, D10, F-1~F-9) | `02_설계` 1.4 (`FillPlanResolver`+`MagicResultAssembler`), 1.4.1, 1.5.4, 1.5.5 | ✅ |
| 인지 1 ↔ 구현 2 (US-5) | `05_Journey` 5.2의 Solver 행 | ✅ |
| Story 우선순위 (10절) | `02_설계` 1.5.7 진행 순서 | ✅ |

---

## 10. Story 우선순위 (RED 작성 순서)

> 본 우선순위는 `02_설계` 1.5.7의 진행 순서를 *Story 단위로 재서술*한 것이다.

| 순서 | Story | 첫 RED 후보 | 근거 |
|---|---|---|---|
| 1 | **US-4** (마방진 판정) | `T-D-001` | I4의 직접 술어이며, 다른 Story의 *판정 도구*로 사용된다. 가장 단순한 정상 케이스로 골격 형성. |
| 2 | **US-2** (빈칸 탐색) | `T-D-010` | D4·D8 술어가 단순. 단일 책임 Service. |
| 3 | **US-3** (누락 숫자 탐색) | `T-D-020` | D5 술어가 단순. 단일 책임 Service. |
| 4 | **US-5** (두 조합 시도) | `T-D-030` | US-2, US-3, US-4의 GREEN을 *호출하여* 흐름 조율. 내부에 조합 A/B 분기. |
| 5 | **US-1** (입력 검증) | `T-U-001` | UI Track RED. Logic Track과 *병렬* 진행 가능 (`05_Journey` 6절 Dual-Track). |

> ※ Logic Track 우선순위는 1→2→3→4. UI Track(US-1)은 별도 트랙으로 *언제든* 시작 가능.
> 단, US-1의 *통합 검증*(`T-I-XXX`)은 US-5 GREEN 이후에만 의미가 있다.

---

## 마무리 진술

> 본 단계에서 우리가 도달한 결론은 다음과 같다.
>
> **"우리는 학습자의 여정을, 한 줄짜리 가치 진술과 검증 가능한 합격 기준의 묶음으로 다시 분해했다.
> Level 1(Epic)이 *목적의 평면*을, Level 2(Journey)가 *시간의 축*을 닫았다면,
> Level 3(본 단계)은 *그 두 차원을 5개의 가치 단위(Story)로 환원*했다.
> 각 Story는 단독으로 합격/불합격 판정이 가능하며, 어떤 D-x 술어와 어떤 Test ID로 보호되는지가 외부화되어 있다."**

이 환원으로 본 사용자 여정 분해는 닫힌다.
다음 단계는 사용자 여정의 *추가 분해*가 아니라, **각 Story의 RED 테스트를 실제로 작성하고 GREEN으로 통과시키는 Implementation Phase**이다.

---

## 다음 단계 체크리스트 (Pre-Implementation Gate)

다음 단계(RED 테스트 작성 → GREEN 구현)로 진입하기 전, 아래 항목 모두에 ✅가 찍혀야 합니다.
*아래는 본 Story 작성자의 자체 판정 결과이며, 별도 검토자가 의견을 제시하면 해당 시점에 항목별로 재개방됩니다.*

- [x] 5개 Story가 *INVEST 원칙*(1.1)을 모두 만족하는가?
- [x] 모든 AC가 *D-x 술어 또는 byte-equal 진술*로 환원되었는가? (1.3, 2~6장)
- [x] 모든 AC가 `02_설계`의 기존 Test ID(`T-D-XXX`/`T-U-XXX`/`T-I-XXX`)에 *최소 1개* 매핑되었는가? (8절)
- [x] Story 3·4·5의 *추론 진술*임이 명시되었으며, 사용자의 다른 합의가 등장 시 즉시 폐기 가능한 형태인가? (4.5, 5.1, 6.1)
- [x] US-5의 *인지 단위 1 ↔ 구현 단위 2* 매핑이 명시되었는가? (6.3)
- [x] Story 간 의존 DAG(7절)가 *RED 작성 가능성 의존*임이 명시되었는가? (7절 머리말)
- [x] RED 작성 우선순위(10절)가 `02_설계` 1.5.7과 정합인가?
- [x] 본 단계 이후 *Implementation Phase*(RED → GREEN → REFACTOR)로 진입한다는 사실이 명시되었는가? (마무리 진술)

### 자체 판정 근거 (Self-Evaluation Notes)

| # | 항목 | 판정 근거 |
|---|---|---|
| 1 | INVEST | 1.1 표가 6개 원칙을 *본 프로젝트에서의 환원*으로 명시. 모든 Story가 AC ≤ 4개. |
| 2 | AC 환원 | 모든 AC 행에 *검증 가능 환원* 컬럼이 존재하며, D-x 또는 표준 메시지 byte-equal로 환원됨. 모호 어휘(*"적절히"* 등) 0건. |
| 3 | Test ID 매핑 | 8절 매트릭스에서 5개 Story 모두 최소 1개 이상의 Test ID와 매핑. 매핑 0건 Story 없음. |
| 4 | 추론 표시 | 4.5, 5.5(*Story 4는 표면 Validator 명명만 추론*), 6.1에서 추론 사실을 박스/주석으로 명시. 폐기 가능성 명문화. |
| 5 | 1↔2 매핑 | 6.3에서 `Solver = FillPlanResolver + MagicResultAssembler`로 명시. `05_Journey` 5.2와 정합. |
| 6 | DAG 의미 | 7절 머리말에서 *런타임 호출 의존이 아닌 RED 작성 가능성 의존*임을 명시. |
| 7 | 우선순위 정합 | 10절 표가 `02_설계` 1.5.7의 1~7단계를 Story 단위로 재서술. 순서 동일. |
| 8 | Phase 전이 명시 | 마무리 진술에서 *추가 분해가 아니라 Implementation Phase 진입*임을 외부화. |

→ **8/8 ✅ 충족.** 본 User Stories 단계는 자체 판정 기준에 의해 **Pre-Implementation Gate를 통과**한 것으로 마감합니다.

> 위 8개 항목 모두에 ✅가 찍힌 본 시점부터, 다음 단계인 **RED 테스트 작성 → GREEN 최소 구현 → REFACTOR (Implementation Phase)** 로 진입할 수 있습니다.
> 단, RED 작성의 *세부 지침*(테스트 파일 배치, 픽스처 설계, 명명 규약 적용 예)은 별도 안내를 통해 부여받습니다.
