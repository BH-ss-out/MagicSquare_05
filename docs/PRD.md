# Magic Square (4x4) — TDD 연습용 PRD

> ⚠️ 본 문서는 **구현 코드를 포함하지 않는다**.
> 모든 요구사항은 *검증 가능한 술어(predicate)* 로 환원되어 있으며, “적절히/충분히” 같은 모호 표현은 사용하지 않는다.
> 본 PRD는 Boundary(경계)와 Domain(도메인)을 **물리적으로 분리하는 Dual-Track 구조**를 전제로 작성되었다.

---

## 문서 메타데이터

| 항목 | 내용 |
|---|---|
| 문서 ID | `PRD-MagicSquare-4x4` |
| 산출 단계 | Product Requirements Document (PRD) |
| 선행 문서 | `Report/01_문제_정의`, `Report/02_설계`, `Report/03_프로젝트_규약_정의`, `Report/04_사용자여정_Epic` |
| 산출 형식 | Markdown |
| 골격 출처 | `Report/04`(Epic / 성공 기준)을 축으로, `Report/01`(문제·동기), `Report/02`(계약·기능·성공 정의), `Report/03` 및 `.cursorrules`(품질·개발 원칙) 결합 |
| 변경 통제 | 0절 입출력 계약, 6절 BR, 12절 Traceability Matrix는 **변경 금지**(회귀 보호 대상). 13절 Ops & Automation은 *유연 변경 허용*(§13.7) — 단 NFR을 약화하는 임계값 변경은 거부된다. |

---

## 0. 입출력 계약 (Frozen Contract)

> 본 절은 PRD 본문 모든 요구사항의 *공통 전제*다. 본 PRD의 어떤 절도 본 계약을 약화·변경할 수 없다.

### 0.1 입력 (Input)

| 항목 | 규칙 | 검증 가능 술어 |
|---|---|---|
| 타입 | `int[][]` (정수 2차원 배열) | 원소 타입이 정수 |
| 형태 | 4행 4열 | `len(matrix) == 4 ∧ ∀r: len(matrix[r]) == 4` |
| 값 범위 | 0 또는 1..16 | `∀(r,c): matrix[r][c] == 0 ∨ 1 ≤ matrix[r][c] ≤ 16` |
| 빈칸 표지 | `0` | — |
| 빈칸 개수 | **정확히 2개** | `count((r,c) where matrix[r][c]==0) == 2` |
| 중복 | 0을 제외한 값 중 중복 금지 | `multiset({matrix[r][c] : matrix[r][c] != 0})` 내 중복 0 |
| 첫 번째 빈칸 정의 | row-major(행 우선) 스캔 시 *처음* 만나는 0 | 스캔 인덱스 `r*4+c` 최소 |

### 0.2 출력 (Output)

| 항목 | 규칙 |
|---|---|
| 타입 | `int[6]` (길이 6 정수 배열) |
| 좌표 인덱싱 | **1-index** (`1 ≤ r,c ≤ 4`) |
| 포맷 | `[r1, c1, n1, r2, c2, n2]` |
| `(r1,c1)` | row-major 첫 번째 빈칸 좌표 |
| `(r2,c2)` | row-major 두 번째 빈칸 좌표 |
| `n1, n2` | 격자에 누락된 두 숫자 |
| 시도 1 | (작은 수 → 첫 빈칸, 큰 수 → 둘째 빈칸) 채움 → 마방진이면 그 순서로 반환 (`n1=작은수, n2=큰수`) |
| 시도 2 | 시도 1 실패 시 (큰 수 → 첫 빈칸, 작은 수 → 둘째 빈칸) 채움 → 마방진이면 역순 반환 (`n1=큰수, n2=작은수`) |
| 두 시도 모두 실패 | **명시적 도메인 예외 `E_UNSOLVABLE` 발생** (11절 결정 항목 참조) |
| Magic Constant | `M = 34` (`n×(n²+1)/2 = 4×17/2`) |

### 0.3 도메인 실패 코드

| 코드 | 의미 | 책임 레이어 |
|---|---|---|
| `E_SHAPE` | 4x4 형태가 아님 | Boundary |
| `E_VALUE_RANGE` | 셀 값이 `{0} ∪ {1..16}` 밖 | Boundary |
| `E_BLANK_COUNT` | 빈칸이 정확히 2개가 아님 | Boundary |
| `E_DUPLICATE` | 0을 제외한 중복 존재 | Boundary |
| `E_UNSOLVABLE` | 두 조합 모두 마방진 미성립 | Domain |

> ※ `E_PERSISTENCE`(저장/로드 실패)는 본 PRD 범위 밖(§4.2)이므로 정의하지 않는다.

---

## 1. Executive Summary

본 프로젝트는 4x4 마방진 문제를 매개로, **알고리즘 난이도가 아니라 TDD(Red→Green→Refactor) 사고 양식**과
**Invariant 기반 검증 사고**를 훈련하기 위한 *순수 로직 중심* 학습 시스템을 산출한다.
산출물은 다음 **네 가지** 핵심 역량을 *외부 도구가 자동 강제할 수 있는 형태로* 형식화한다.
(1) 입력/출력 **계약(Contract)** 을 byte-equal 수준으로 고정하고,
(2) 5개의 도메인 **불변 조건(I1~I5)** 을 검증 가능한 술어로 환원하며,
(3) Boundary Track과 Domain Track의 **Dual-Track TDD** 사이클을 분리·병렬 운영하고,
(4) 위 (1)~(3)을 **Ops Track의 자동화 게이트(§13)** 가 PR/커밋 단위로 *결정적으로* 강제한다.
UI 화면, 데이터베이스, 네트워크 의존성, 그리고 **MLOps 본래 의미의 모든 구성요소(§13.5 OO-1)** 는 **본 PRD 범위에서 의도적으로 배제**한다.

---

## 2. Problem Statement (문제 정의)

### 2.1 표면 문제 (잘못된 정의)

> *"4x4 격자에 1~16을 배치하여 마방진을 만든다."*

이 정의는 **산출물 중심**이며 다음을 누락한다 (`Report/01` 5.1).
- 무엇이 “올바름”인지에 대한 *판정 기준*
- *부분 위반*과 *전체 위반*의 구분
- *결정성*·*반복성*·*자동성* 요구

### 2.2 본 PRD가 채택하는 정확한 문제 정의

> *"임의로 주어진 4x4 숫자 배치(빈칸 2개 포함)에 대해, 누락된 두 숫자를 두 빈칸에 배치한 결과가
> 마방진의 불변 조건을 충족하는지 여부와, 충족 시 그 배치 순서를 검증 가능한 형태로 결정하는 문제."*

### 2.3 입력/출력 계약이 핵심인 이유

| 관점 | 계약이 모호할 때 무너지는 것 |
|---|---|
| **TDD 성립성** | TDD는 *“입력 → 기대 출력” 계약을 먼저 쓰는 행위*다. 계약이 없으면 RED 자체가 불가능하다 (`Report/01` 4.3). |
| **검증 신뢰성** | 입력 형태가 흔들리면 *“무엇을 검증한 것인가”* 자체가 흔들린다. |
| **출력 의사결정성** | 출력의 의미가 흔들리면 *“이 결과로 무엇을 결정할 수 있는가”* 가 사라진다. |
| **회귀 보호** | 표준 에러 코드/순서가 흔들리면 모든 Boundary 테스트가 깨진다. |

### 2.4 본 PRD가 훈련하려는 핵심 역량

| 코드 | 역량 | 출처 |
|---|---|---|
| C-1 | 산출물보다 **불변 조건을 먼저** 언어화 | `Report/01` 5.4-1 |
| C-2 | 구현보다 **검증을 먼저** 설계 | `Report/01` 5.4-2 |
| C-3 | 실패를 **분류·식별** 가능한 단위로 분해 | `Report/01` 5.4-3 |
| C-4 | 암묵지를 **형식지**(테스트/계약)로 환원 | `Report/01` 5.4-4 |
| C-5 | **계약 기반 사고**(Contract-driven thinking) | `Report/01` 5.4-5 |

---

## 3. Target Users

| ID | 페르소나 | 사용 목적 | 사용 환경 | 성공 신호 |
|---|---|---|---|---|
| U-1 | **TDD 학습자** | RED→GREEN→REFACTOR 사이클을 *작은 폐쇄 도메인*에서 반복 훈련 | 로컬 개발 환경 + 터미널의 테스트 러너(`pytest`) | 모든 RED 커밋이 GREEN 커밋보다 *먼저* 등장하며, 새 기능 추가 시에도 기존 테스트가 깨지지 않는다. |
| U-2 | **코드 리뷰어** | 학습자가 작성한 테스트가 *어느 Invariant/계약을 보호*하는지 추적 | 로컬 또는 CI 환경, PR 리뷰 화면 | 12절 Traceability Matrix를 사용해 *임의 테스트 → Invariant* 의 역추적이 30초 내 가능. |
| U-3 | **호출자(테스트 드라이버)** | `int[][]`를 입력해 `int[6]` 또는 도메인 예외를 받는 *순수 함수형 인터페이스* 사용 | 콘솔 실행, 단위 테스트 함수 호출 | 동일 입력에 대해 항상 동일 결과/예외를 받는다(BR-15). |
| U-4 | **Ops 게이트 운영자**(Quality-Gate Maintainer) | §13에서 정의된 자동화 게이트(OG-1 ~ OG-14) 도입·튜닝·회귀 보호 — §7 NFR을 *외부 도구로 결정적 강제* | GitHub Actions 워크플로 / pre-commit 훅 / lint·type·cov·property·traceability 도구 설정 | 모든 PR에서 OG-1 ~ OG-14가 *결정적으로* 통과/실패하며(OPS-5), *임계값 약화 PR은 0건*이다(OPS-2). |

> ※ 본 PRD에서 **"UI"는 화면이 아니라 *외부 호출자와 도메인 사이의 입출력 경계*** 를 뜻한다(`Report/02` 2절).
> ※ 학습 프로젝트 맥락에서는 **U-1과 U-4가 같은 학습자**일 수 있다(역할 분리만 명시). U-4는 *런타임 사용자*가 아니라 *빌드/CI 시점의 운영자*임에 유의한다(§13.1 메타 트랙).

---

## 4. Scope

### 4.1 In-Scope (본 PRD가 책임지는 범위)

| 코드 | 항목 | 대응 FR |
|---|---|---|
| S-1 | **입력 검증**(형태/값 범위/빈칸 개수/중복) — Boundary 레이어 | FR-01 |
| S-2 | **빈칸 좌표 찾기**(row-major 2개) | FR-02 |
| S-3 | **누락 숫자 찾기**(오름차순 2개) | FR-03 |
| S-4 | **마방진 판정**(행/열/두 대각의 합 = 34) | FR-04 |
| S-5 | **해 찾기**(두 조합 시도 후 결과 반환 또는 `E_UNSOLVABLE`) | FR-05 |
| S-6 | **순수 로직** 인터페이스(콘솔/테스트에서 직접 호출) | 전 FR |
| S-7 | **자동화 게이트 운영**(CI/CD, pre-commit, lint/type/cov/property/traceability 검사) — Ops Track | §13 (전 NFR 보호) |

### 4.2 Out-of-Scope (본 PRD가 다루지 않는 범위)

| 코드 | 제외 항목 | 사유 |
|---|---|---|
| O-1 | UI 화면(GUI/Web/CLI 디자인) | 본 PRD는 *입출력 경계 계약*만 다룬다(U-3, `Report/04` NG-4). |
| O-2 | DB 저장/조회, 파일 영속성 | *순수 로직 중심* 학습 목표(`Report/04` NG-5). `E_PERSISTENCE`는 본 PRD에서 정의하지 않는다. |
| O-3 | N×N 일반화(N≠4) | 학습 단위는 4x4로 고정(`Report/04` NG-1). |
| O-4 | 마방진 *생성* 알고리즘 | 본 PRD는 *판정/완성*이지 *생성*이 아님(`Report/04` NG-2). |
| O-5 | 성능 벤치마킹·최적화 | 결정성·검증 가능성이 1순위(`Report/04` NG-3). 단, NFR-04의 상한은 적용. |
| O-6 | 다국어/i18n | 표준 메시지는 영어 byte-equal 고정(`Report/04` NG-6). |
| O-7 | 비-정수 입력(float/문자열) 처리 | 입력 타입은 `int[][]`로 고정. 비-정수는 호출자/타입 시스템이 차단한 것으로 가정 (11절 R-3 참조). |

---

## 5. Functional Requirements (기능 요구사항)

> 모든 FR은 동일한 7-종 키 (Feature ID / 설명 / 입력 / 처리 규칙 / 출력 / 승인 기준 AC / 오류 정책) 로 작성한다.
> 모든 AC는 *테스트 가능한 단정 문장*으로 기술된다.

---

### FR-01 — 입력 검증 (Boundary)

| 항목 | 내용 |
|---|---|
| **Feature ID** | FR-01 |
| **설명** | 외부 호출자가 전달한 `int[][]`이 0절 입력 계약을 모두 충족하는지 *결정적 순서*로 검증하고, 위반 시 단일 도메인 실패 코드를 반환한다. |
| **소속 레이어** | Boundary |
| **입력** | `matrix: int[][]` |
| **처리 규칙** | 다음 5개 규칙을 **이 순서대로**(변경 금지) 평가한다 (`Report/02` 2.2.4). 첫 위반에서 즉시 중단·실패 코드 반환. <br>① 행 개수 == 4 → 위반 시 `E_SHAPE` <br>② 모든 행의 열 개수 == 4 → 위반 시 `E_SHAPE` <br>③ 모든 셀이 `0 ∨ 1..16` → 위반 시 `E_VALUE_RANGE` (첫 위반 좌표를 `locus`에 기록) <br>④ `count(0) == 2` → 위반 시 `E_BLANK_COUNT` <br>⑤ 0을 제외한 값에 중복 없음 → 위반 시 `E_DUPLICATE` (첫 위반 좌표를 `locus`에 기록) <br>모두 통과 시 Domain(FR-05)에 위임. |
| **출력** | (a) 정상: Domain의 `int[6]` 결과를 *변형 없이* 그대로 반환. (b) 위반: 도메인 실패 코드 + 표준 메시지(byte-equal). |
| **승인 기준 (AC)** | **AC-01-01** 입력이 3행이면 `E_SHAPE`를 반환한다. <br>**AC-01-02** 어느 한 행의 열 개수가 4가 아니면 `E_SHAPE`를 반환한다. <br>**AC-01-03** 셀 값이 음수이면 `E_VALUE_RANGE`를 반환하고, `locus`는 row-major 첫 위반 좌표(1-index)와 일치한다. <br>**AC-01-04** 셀 값이 17 이상이면 `E_VALUE_RANGE`를 반환한다. <br>**AC-01-05** `count(0) ∈ {0,1,3,4,...}`이면 `E_BLANK_COUNT`를 반환한다. <br>**AC-01-06** 0이 아닌 값이 두 번 이상 등장하면 `E_DUPLICATE`를 반환한다. <br>**AC-01-07** 형태 위반과 값 범위 위반이 동시에 존재하면 `E_SHAPE`를 반환한다(우선순위). <br>**AC-01-08** 값 범위 위반과 빈칸 개수 위반이 동시에 존재하면 `E_VALUE_RANGE`를 반환한다(우선순위). <br>**AC-01-09** 빈칸 개수 위반과 중복 위반이 동시에 존재하면 `E_BLANK_COUNT`를 반환한다(우선순위). <br>**AC-01-10** 모든 검증 통과 시 Domain은 *정확히 1회* 호출된다. <br>**AC-01-11** 검증 위반 시 Domain은 *0회* 호출된다. <br>**AC-01-12** 표준 에러 메시지는 다음과 byte-equal: `E_SHAPE`→`"Input must be a 4x4 matrix."`, `E_VALUE_RANGE`→`"Each cell must be 0 or an integer in [1, 16]."`, `E_BLANK_COUNT`→`"Input must contain exactly 2 blanks (zeros)."`, `E_DUPLICATE`→`"Non-zero values must be unique."` |
| **오류 정책** | 한 입력에 대해 **단 하나의 실패 코드**만 반환한다(다중 코드 금지). 코드 결정은 위 ①~⑤ 순서를 따른다. 메시지에는 입력 데이터 값을 포함하지 않는다(보안·결정성, `Report/02` 2.4.1 M-2). |

---

### FR-02 — 빈칸 탐색 (Domain)

| 항목 | 내용 |
|---|---|
| **Feature ID** | FR-02 |
| **설명** | 4x4 `Board`에서 row-major 스캔 순서로 정확히 2개의 빈칸 좌표를 1-index로 반환한다. |
| **소속 레이어** | Domain |
| **입력** | 빈칸이 정확히 2개인 4x4 정수 격자 |
| **처리 규칙** | 행 인덱스 `r ∈ {1,2,3,4}` 오름차순, 각 행 내에서 열 인덱스 `c ∈ {1,2,3,4}` 오름차순으로 스캔한다. 발견된 0의 좌표를 발견 순서대로 `(first, second)`로 묶는다. 사전조건(빈칸 == 2개)은 Boundary가 보장하므로 도메인은 방어적 재검증을 *중복 수행하지 않는다*. |
| **출력** | `BlankPair{first=(r1,c1), second=(r2,c2)}`, `1 ≤ r,c ≤ 4` |
| **승인 기준 (AC)** | **AC-02-01** 두 빈칸이 동일 행이면 두 좌표는 행이 같고 `c1 < c2`이다. <br>**AC-02-02** 두 빈칸이 다른 행이면 `r1 < r2`이다. <br>**AC-02-03** 좌상단 0행0열의 빈칸은 `(1,1)`로 반환된다(0-index 누설 금지). <br>**AC-02-04** 빈칸이 `(3,1)`과 `(1,4)`에 있을 때 `first=(1,4), second=(3,1)`이다(row-major 순서). <br>**AC-02-05** 동일 입력에 대해 100회 호출 시 결과가 모두 동일하다(결정성). |
| **오류 정책** | 사전조건(빈칸 개수 == 2) 위반은 *호출자 책임*이며, 위반 시 도메인 가정 위반(Precondition violated). Boundary가 사전 차단하므로 정상 흐름에서는 발생하지 않는다. |

---

### FR-03 — 누락 숫자 탐색 (Domain)

| 항목 | 내용 |
|---|---|
| **Feature ID** | FR-03 |
| **설명** | 4x4 `Board`에서 1..16 중 등장하지 않은 두 숫자를 *오름차순*으로 반환한다. |
| **소속 레이어** | Domain |
| **입력** | 0이 아닌 값이 *서로 다른 14개* 들어있는 4x4 정수 격자 |
| **처리 규칙** | `filled = {matrix[r][c] : matrix[r][c] != 0}`을 구성하고, `missing = {1..16} \ filled`를 계산한다. `missing`의 카디널리티는 항상 2(`|missing| == 2`). 결과는 `(small, large)` 오름차순. |
| **출력** | `MissingPair{small, large}` with `1 ≤ small < large ≤ 16` |
| **승인 기준 (AC)** | **AC-03-01** 1과 16이 누락된 입력에 대해 `(small=1, large=16)`을 반환한다. <br>**AC-03-02** 7과 8이 누락된 입력에 대해 `(small=7, large=8)`을 반환한다. <br>**AC-03-03** 누락 숫자가 (12, 3) 순서로 발견되어도 결과는 `(small=3, large=12)`로 정렬된다. <br>**AC-03-04** `small != large`가 항상 성립한다. <br>**AC-03-05** 동일 입력에 대해 100회 호출 시 결과가 모두 동일하다(결정성). |
| **오류 정책** | 사전조건(`|missing| == 2`) 위반은 호출자 책임. Boundary 통과 시 자동 보장. |

---

### FR-04 — 마방진 판정 (Domain)

| 항목 | 내용 |
|---|---|
| **Feature ID** | FR-04 |
| **설명** | 빈칸 없는 4x4 격자에 대해 모든 행/열/두 대각선의 합이 Magic Constant 34와 같은지 boolean으로 판정한다. |
| **소속 레이어** | Domain |
| **입력** | 빈칸이 0개인 4x4 정수 격자 |
| **처리 규칙** | 술어 `D6 ≡ (∀r: Σc matrix[r][c] == 34) ∧ (∀c: Σr matrix[r][c] == 34) ∧ (Σi matrix[i][i] == 34) ∧ (Σi matrix[i][3-i] == 34)`을 평가한다. 입력은 *읽기 전용*으로 취급하며 변경하지 않는다(BR-16). |
| **출력** | `boolean` |
| **승인 기준 (AC)** | **AC-04-01** 표준 Dürer 마방진(§9.4 D-Std)에 대해 `true`를 반환한다. <br>**AC-04-02** 1행 합이 33인 격자에 대해 `false`를 반환한다. <br>**AC-04-03** 2열 합이 35인 격자에 대해 `false`를 반환한다. <br>**AC-04-04** 주대각 합만 34가 아닌 격자에 대해 `false`를 반환한다. <br>**AC-04-05** 부대각 합만 34가 아닌 격자에 대해 `false`를 반환한다. <br>**AC-04-06** 모든 합이 34라도 셀에 중복 숫자가 있으면(예: 한 값이 4회 반복) `false`를 반환한다(I3 보호). <br>**AC-04-07** 동일 입력에 대해 100회 호출 시 결과가 모두 동일하다(결정성). <br>**AC-04-08** 호출 전·후의 입력 격자는 byte-equal하다(부작용 금지). |
| **오류 정책** | 빈칸이 1개 이상이면 사전조건 위반. Boundary 사전 차단으로 정상 흐름에서는 발생하지 않는다. |

---

### FR-05 — 해 찾기 (solution): 두 조합 시도 및 반환

| 항목 | 내용 |
|---|---|
| **Feature ID** | FR-05 |
| **설명** | 빈칸 2개와 누락 숫자 2개로부터 두 조합(A: 작↔첫, B: 큰↔첫)을 *순서대로* 시도하여 마방진을 만드는 조합의 결과를 `int[6]`으로 반환한다. 둘 다 실패 시 `E_UNSOLVABLE`을 발생시킨다. |
| **소속 레이어** | Domain (FR-02 + FR-03 + FR-04 오케스트레이션) |
| **입력** | 0절 계약을 충족하는 `int[][]` |
| **처리 규칙** | 다음 절차를 **이 순서대로** 수행한다(변경 금지). <br>① `BlankPair = FR-02(matrix)` <br>② `MissingPair = FR-03(matrix)` <br>③ 시도 A: `matrix`의 *복사본*에 `(first ← small, second ← large)`로 채운 후 FR-04 호출. `true`이면 `[r1,c1,small,r2,c2,large]` 반환·종료. <br>④ 시도 B: `matrix`의 *별도 복사본*에 `(first ← large, second ← small)`로 채운 후 FR-04 호출. `true`이면 `[r1,c1,large,r2,c2,small]` 반환·종료. <br>⑤ 둘 다 `false`이면 `E_UNSOLVABLE` 예외 발생. <br>원본 입력 행렬은 어떤 단계에서도 변경되지 않는다(BR-16). |
| **출력** | `int[6] = [r1,c1,n1,r2,c2,n2]` 또는 `E_UNSOLVABLE` |
| **승인 기준 (AC)** | **AC-05-01** 시도 A가 마방진이면 `n1=small, n2=large` 순서로 반환한다. <br>**AC-05-02** 시도 A가 마방진이 아니고 시도 B가 마방진이면 `n1=large, n2=small` 순서로 반환한다. <br>**AC-05-03** 시도 A가 이미 마방진일 때 시도 B는 *호출되지 않는다*(단락 평가, `Report/02` 1.4.1 F-4). <br>**AC-05-04** 두 시도 모두 비-마방진이면 `E_UNSOLVABLE` 예외가 발생하고, 그 외 다른 도메인 코드(`E_*`)는 사용되지 않는다. <br>**AC-05-05** 출력 길이는 항상 6이다. <br>**AC-05-06** `n1 ≠ n2`이며, `{n1, n2} ⊆ {1..16}`이다. <br>**AC-05-07** 출력 좌표 (r1,c1), (r2,c2)는 1-index이고, row-major 순서로 `(r1,c1) < (r2,c2)`이다. <br>**AC-05-08** 호출 전·후의 입력 행렬은 byte-equal하다(부작용 금지, BR-16). <br>**AC-05-09** 동일 입력에 대해 100회 호출 시 동일한 `int[6]` 또는 동일한 `E_UNSOLVABLE`이 반환된다(결정성). |
| **오류 정책** | 두 조합 모두 실패 시 `E_UNSOLVABLE` 발생, 표준 메시지 `"No valid magic square completion exists for the given input."`(`Report/02` 2.4 byte-equal). 다른 코드로 가리지 않는다. |

---

## 6. Business Rules (도메인 규칙)

> 모든 BR은 *“항상 참이어야 하는”* 술어다. 위반은 곧 회귀(regression)다.
> 본 절은 **변경 금지**(Frozen) — 변경 시 12절 Traceability Matrix가 깨진다.

| ID | 규칙 (검증 가능 술어) | 보호 Invariant | 보호 주체 |
|---|---|---|---|
| **BR-01** | 입력은 항상 4행 4열이다. `len(matrix)==4 ∧ ∀r: len(matrix[r])==4` | I1 | Boundary (FR-01) |
| **BR-02** | 모든 셀 값은 0 또는 1..16의 정수다. `∀(r,c): matrix[r][c] ∈ {0,1,...,16}` | I2 | Boundary (FR-01) |
| **BR-03** | 빈칸 개수는 정확히 2다. `count(matrix[r][c]==0) == 2` | I1 보강 | Boundary (FR-01) |
| **BR-04** | 0을 제외한 값에 중복은 없다. `multiset({v ∈ matrix : v!=0})` 내 중복 0 | I3 | Boundary (FR-01) |
| **BR-05** | Magic Constant `M = 34`이다 (`n=4 → 4×17/2`). | I4 | Domain 상수 |
| **BR-06** | 마방진 ⇔ 모든 행/열/두 대각의 합이 34와 같다. | I4 | Domain (FR-04) |
| **BR-07** | 첫 번째 빈칸은 row-major 스캔 시 첫 번째로 발견되는 0의 좌표다. | I1 보강 | Domain (FR-02) |
| **BR-08** | 출력 좌표는 1-index이며 `1 ≤ r,c ≤ 4`이다. | I5 보강 | Domain (FR-05 출력) |
| **BR-09** | 출력 길이는 항상 6이다. `len(result) == 6` | I5 보강 | Domain (FR-05) |
| **BR-10** | 시도 1 채움 규칙: `(first ← small, second ← large)` | I4 보강 | Domain (FR-05) |
| **BR-11** | 시도 2 채움 규칙: `(first ← large, second ← small)` | I4 보강 | Domain (FR-05) |
| **BR-12** | 시도 1이 마방진이면 결과는 `[r1,c1,small,r2,c2,large]`이다(시도 2 미수행). | I4 + 결정성 | Domain (FR-05) |
| **BR-13** | 시도 1이 비-마방진이고 시도 2가 마방진이면 결과는 `[r1,c1,large,r2,c2,small]`이다. | I4 + 결정성 | Domain (FR-05) |
| **BR-14** | 두 시도 모두 비-마방진이면 `E_UNSOLVABLE` 예외를 발생시킨다. 다른 코드로 대체하지 않는다. | I4 (실패 식별성) | Domain (FR-05) |
| **BR-15** | 결정성: 동일 입력에 대해 100회 호출 시 동일한 출력(또는 동일한 예외)이 반환된다. | I5 | 전 도메인 |
| **BR-16** | 부작용 금지: 호출 전·후 입력 행렬은 byte-equal하다(원본 불변). 채움 시뮬레이션은 *복사본* 위에서만 수행된다. | I5 보강 | Domain (FR-04, FR-05) |
| **BR-17** | 의존성 방향: Domain은 Boundary를 모른다(import 금지, `.cursorrules` `architecture.dependency_direction`). | (메타) | 전 컴포넌트 |
| **BR-18** | 누락 숫자 결과는 항상 오름차순(`small < large`)이다. | I3 보강 | Domain (FR-03) |
| **BR-19** | Boundary 검증 위반 시 단 하나의 실패 코드만 반환한다(다중 코드 금지). 코드 결정은 FR-01 ①~⑤ 순서에 따른다. | I5 보강 | Boundary (FR-01) |
| **BR-20** | 표준 에러 메시지는 §0.3·FR-01·FR-05의 정확한 영문 문구와 byte-equal해야 한다. | I5 보강 | Boundary + Domain |

---

## 7. Non-Functional Requirements

| ID | 요구사항 | 검증 가능 임계 / 도구 | 미달 시 정책 |
|---|---|---|---|
| **NFR-01** | **Domain Logic 테스트 커버리지** ≥ 95% (라인), ≥ 90% (분기) | `pytest --cov=<domain> --cov-fail-under=95` (`Report/04` SC-1) | 미커버 분기에 대해 RED 테스트 추가. `# pragma: no cover`는 정당한 사유 주석 동반 시에만 허용. |
| **NFR-02** | **Boundary Validation 테스트 커버리지** ≥ 85% (라인) **및** Boundary 계약 테스트 통과율 100% | `pytest --cov=<boundary> --cov-fail-under=85` + `pytest tests/boundary/ -v` (실패/스킵 0건) (`Report/02` 4.4, `Report/04` SC-2) | Boundary 테스트 단 1건 실패/스킵 시 비합격. |
| **NFR-03** | **결정성 (Determinism)**: 동일 입력 → 동일 출력(또는 동일 예외) | `pytest`에서 100회 반복 단정 (BR-15) | 결과 분기 발생 시 즉시 RED 추가, 비결정 원인(전역 상태/난수/I/O) 제거. |
| **NFR-04** | **부작용 금지 (Input Immutability)**: 호출 전·후 입력 행렬은 byte-equal | 호출 전 deep-copy를 보관하고 사후 동등성 단정 (BR-16) | 입력 변형 발견 시 채움 시뮬레이션 코드를 *복사본 기반*으로 수정. |
| **NFR-05** | **성능 상한**: 4x4 단일 입력 처리(FR-05 한 번 호출) ≤ 50ms (단일 코어, 표준 데스크톱 환경) | `time.perf_counter()` 또는 `pytest-benchmark`로 P95 측정 | 회귀 발견 시 알고리즘 단순성 우선 검토(과도한 자료구조 도입 금지). |
| **NFR-06** | **하드코딩/매직 넘버 금지**: 4, 16, 34, 6, 0 등 도메인 상수는 `Final` 상수로 외부화 | `ruff check`(룰 `PLR2004` 활성화) + 코드 리뷰 (`Report/04` SC-3, SC-4) | 발견 즉시 상수 모듈로 추출 후 일괄 교체(부분 교체 금지). |
| **NFR-07** | **표준 에러 메시지 byte-equal**: 5개 에러 메시지는 정확한 영문 문구로 고정 | 문자열 동등성 단정(`assert msg == "..."`) (`Report/02` 2.4.1 M-1) | 문구 변경 시 12절 Traceability Matrix와 모든 영향 테스트 동시 갱신. |
| **NFR-08** | **추적성 (Traceability)**: I1~I5 각각이 최소 1개 이상의 Test ID와 명시적으로 연결됨 | 12절 매트릭스 + 테스트 docstring (`Report/04` SC-5) | 누락 발견 시 테스트 추가 또는 Invariant 정의 수정. *paper-only fix* 금지. |
| **NFR-09** | **의존성 방향**: Domain은 Boundary를 import하지 않는다 | `import-linter` 또는 정적 grep | Domain → Boundary import 발견 시 빌드 실패 처리. |

---

## 8. Dual-Track TDD Strategy

> 본 PRD의 핵심 전제: Boundary와 Domain은 **각자 독립된 RED→GREEN→REFACTOR 사이클**을 가진다.
> *“도메인을 다 끝낸 후 경계를 추가”* 하는 진행은 본 절에 의해 명시적으로 금지된다.

### 8.1 Track A — Boundary (UI) TDD

**핵심 원칙**: Domain은 Mock으로 가정하고, Boundary가 *위임 직전 검증*을 정확히 수행하는지만 검증한다.

#### 8.1.1 Contract-first 테스트 항목 (필수 RED)

| Test ID | 검증 대상 | 보호 BR / AC |
|---|---|---|
| `T-U-001`~`T-U-005` | 형태 오류(3행/5행/한 행 짧음/한 행 김/빈 배열) → `E_SHAPE` | BR-01 / AC-01-01, AC-01-02 |
| `T-U-010`~`T-U-013` | 값 범위 오류(음수/17/100/`locus`) → `E_VALUE_RANGE` | BR-02 / AC-01-03, AC-01-04 |
| `T-U-020`~`T-U-023` | 빈칸 개수 오류(0/1/3/4개) → `E_BLANK_COUNT` | BR-03 / AC-01-05 |
| `T-U-030`~`T-U-032` | 중복 오류(2회/3회) 및 0 두 개 허용 정상 위임 | BR-04 / AC-01-06 |
| `T-U-040`~`T-U-042` | 검증 우선순위(형태>범위>빈칸>중복) | BR-19 / AC-01-07~AC-01-09 |
| `T-U-050`~`T-U-052` | Domain Mock 호출 횟수 (정상=1, 위반=0, 결과 변형 없음) | FR-01 / AC-01-10, AC-01-11 |
| `T-U-060`~`T-U-061` | Domain `E_UNSOLVABLE` 그대로 노출 | BR-14 / AC-05-04 |
| `T-U-070`~`T-U-074` | 출력 포맷 검증(길이 6 / 1-index / row-major / `n1≠n2` / `n∈{1..16}`) | BR-08, BR-09, BR-18 / AC-05-05~AC-05-07 |

#### 8.1.2 실패 정책 표준

| 코드 | 예외 타입 (개념) | 표준 메시지 (byte-equal) |
|---|---|---|
| `E_SHAPE` | `BoundaryError` 하위 `ShapeError` | `"Input must be a 4x4 matrix."` |
| `E_VALUE_RANGE` | `BoundaryError` 하위 `ValueRangeError` | `"Each cell must be 0 or an integer in [1, 16]."` |
| `E_BLANK_COUNT` | `BoundaryError` 하위 `BlankCountError` | `"Input must contain exactly 2 blanks (zeros)."` |
| `E_DUPLICATE` | `BoundaryError` 하위 `DuplicateError` | `"Non-zero values must be unique."` |
| `E_UNSOLVABLE` | `DomainError` 하위 `UnsolvableError` | `"No valid magic square completion exists for the given input."` |

> 메시지는 *byte-equal*로 고정(NFR-07). 한 입력에 다중 위반이 있어도 *단 하나*의 코드만 반환한다(BR-19).

---

### 8.2 Track B — Domain (Logic) TDD

**핵심 원칙**: Boundary를 모른다. 입력은 *사전조건이 충족된 상태*로 가정한다.

#### 8.2.1 메서드 단위 테스트 (필수 RED)

| Test ID | 컴포넌트 | 보호 FR / AC |
|---|---|---|
| `T-D-001` | `MagicSquareJudge`: 표준 마방진 → `true` | FR-04 / AC-04-01 |
| `T-D-002` | `MagicSquareJudge`: 회전 변형 → `true` | FR-04 / AC-04-01 |
| `T-D-003` | `MagicSquareJudge`: 한 행 합 33 → `false` | FR-04 / AC-04-02 |
| `T-D-004` | `MagicSquareJudge`: 한 열 합 35 → `false` | FR-04 / AC-04-03 |
| `T-D-005` | `MagicSquareJudge`: 주대각만 어긋남 → `false` | FR-04 / AC-04-04 |
| `T-D-006` | `MagicSquareJudge`: 부대각만 어긋남 → `false` | FR-04 / AC-04-05 |
| `T-D-007` | `MagicSquareJudge`: 합은 34지만 숫자 중복 → `false` | FR-04 / AC-04-06 |
| `T-D-008` | `MagicSquareJudge`: 호출 전·후 입력 격자가 byte-equal (부작용 금지, 컴포넌트 단위) | FR-04 / AC-04-08 (BR-16 보강) |
| `T-D-009` | `MagicSquareJudge`: 동일 입력 100회 호출 시 동일 boolean 반환 (결정성, 컴포넌트 단위) | FR-04 / AC-04-07 (BR-15 보강) |
| `T-D-010`~`T-D-014` | `BlankFinder`: 같은 행/다른 행/인접/스캔 순서/1-index | FR-02 / AC-02-01~AC-02-04 |
| `T-D-020`~`T-D-023` | `MissingNumberFinder`: 경계값/인접/오름차순/결정성 | FR-03 / AC-03-01~AC-03-05 |
| `T-D-030` | `FillPlanResolver`: 조합 A 정답 → `(small,large)` 반환 | FR-05 / AC-05-01 |
| `T-D-031` | `FillPlanResolver`: 조합 B 정답 → `(large,small)` 반환 | FR-05 / AC-05-02 |
| `T-D-032` | `FillPlanResolver`: 둘 다 실패 → `E_UNSOLVABLE` | FR-05 / AC-05-04 |
| `T-D-040`~`T-D-042` | `MagicResultAssembler`: 1-index 좌표/중간 좌표/길이 6 | FR-05 / AC-05-05~AC-05-07 |
| `T-D-050`~`T-D-052` | 도메인 오케스트레이션 End-to-End (정상/결정성/실패) | FR-05 전체 / AC-05-09 |

#### 8.2.2 불변조건 테스트 (Invariant Tests)

| Test ID | Invariant | 단정 |
|---|---|---|
| `T-INV-I1` | I1 형태 불변성 | Domain 진입 시점 격자가 4x4임을 단정(사전조건 가드, debug-mode assert 가능) |
| `T-INV-I2` | I2 정의역 불변성 | 채움 시뮬레이션 후 모든 셀 ∈ `{1..16}` |
| `T-INV-I3` | I3 유일성 불변성 | 채움 후 16개 셀이 `{1..16}` 다중집합과 정확히 일치 |
| `T-INV-I4` | I4 합 균질 불변성 | FR-04가 `true` 반환 시 행/열/대각 10개 합이 모두 34임을 단정 |
| `T-INV-I5` | I5 결정성 | 동일 입력에 대한 100회 반복 호출 결과가 모두 동일 (BR-15) |
| `T-INV-BR16` | BR-16 부작용 금지 | 호출 전 deep-copy와 호출 후 입력이 byte-equal |

---

### 8.3 병렬 진행 규칙

| 규칙 ID | 규칙 (검증 가능) |
|---|---|
| **DT-1** | Track A의 첫 RED와 Track B의 첫 RED는 *같은 타임 윈도우*(같은 작업 세션 내) 안에 모두 작성된다. |
| **DT-2** | 진행 순서는 `[A.RED] & [B.RED] → [A.GREEN] & [B.GREEN] → [A.REFACTOR] & [B.REFACTOR]`이며, 각 단계는 양 Track 모두에서 완료된 뒤에만 다음 단계로 진입한다. |
| **DT-3** | *“도메인을 모두 구현한 뒤 경계를 추가”* 또는 *“경계를 모두 구현한 뒤 도메인을 추가”* 진행은 **금지**된다 (위반 시 `Report/04` P2 충족 증거에서 비합격). |
| **DT-4** | Track A의 RED는 Domain Mock을 사용한다. 실제 Domain 구현이 *존재하지 않아도* Track A는 RED→GREEN을 완주할 수 있어야 한다. |
| **DT-5** | Track B의 RED는 Boundary를 *호출하지 않는다*. Domain 함수에 직접 사전조건 충족 입력을 전달한다. |
| **DT-6** | 한 커밋은 하나의 Track의 하나의 phase만 담는다(혼합 커밋 금지). 위반 시 PR 리뷰 단계에서 분할 요청. |

---

## 9. Test Plan (QA)

### 9.1 시나리오 기반 테스트 목록 (대표)

#### 9.1.1 정상 시나리오 (Happy Path)

| TC ID | 상황 | 입력 (요지) | 기대 출력 |
|---|---|---|---|
| **TC-N-01** | 코너 두 칸 누락, 시도 A 성공 | §9.4 D-Std에서 (1,1)와 (4,4)를 0으로 | `[1,1,1, 4,4,16]` |
| **TC-N-02** | 같은 행 두 칸 누락, 시도 A 성공 | §9.4 D-Std에서 (2,1)과 (2,4)를 0으로 | `[2,1,5, 2,4,8]` |
| **TC-N-03** | 시도 A는 비-마방진, 시도 B만 마방진 | §11 R-2에서 명시되는 케이스 군 | `[r1,c1,large, r2,c2,small]` 형식 |
| **TC-N-04** | 한 빈칸이 주대각 위 | §9.4 D-Std에서 (1,1)과 (2,3) 0으로 | 정상 `int[6]` (구체값은 입력으로 결정) |
| **TC-N-05** | 한 빈칸이 부대각 위 | §9.4 D-Std에서 (4,1)과 (3,3) 0으로 | 정상 `int[6]` |

#### 9.1.2 실패 시나리오 (Failure Path)

| TC ID | 상황 | 입력 (요지) | 기대 |
|---|---|---|---|
| **TC-F-01** | 형태 오류 | 3행 4열 | `E_SHAPE` + 표준 메시지 |
| **TC-F-02** | 한 행만 5열 | `[4,4,4,5]` 열 분포 | `E_SHAPE` |
| **TC-F-03** | 셀 값 음수 | 어떤 셀이 `-1` | `E_VALUE_RANGE` + `locus` (1-index) |
| **TC-F-04** | 셀 값 17 | 어떤 셀이 `17` | `E_VALUE_RANGE` |
| **TC-F-05** | 빈칸 0개 | 모든 셀 채워짐 | `E_BLANK_COUNT` |
| **TC-F-06** | 빈칸 1개 | 정확히 한 개의 0 | `E_BLANK_COUNT` |
| **TC-F-07** | 빈칸 3개 | 정확히 세 개의 0 | `E_BLANK_COUNT` |
| **TC-F-08** | 중복 (7 두 번) | `7`이 두 번 등장 + 빈칸 2개 | `E_DUPLICATE` |
| **TC-F-09** | 두 조합 모두 비-마방진 | 14개 셀이 어떤 마방진과도 정합되지 않음 (§9.4 D-Uns 사용) | `E_UNSOLVABLE` |

#### 9.1.3 검증 우선순위 시나리오

| TC ID | 동시 위반 | 기대 (단일 코드) |
|---|---|---|
| **TC-P-01** | 형태 + 값 범위 | `E_SHAPE` (BR-19, AC-01-07) |
| **TC-P-02** | 값 범위 + 빈칸 개수 | `E_VALUE_RANGE` (AC-01-08) |
| **TC-P-03** | 빈칸 개수 + 중복 | `E_BLANK_COUNT` (AC-01-09) |

### 9.2 회귀 테스트 정책

| 정책 ID | 정책 |
|---|---|
| **REG-1** | RED→GREEN 단계를 거쳐 작성된 테스트는 **삭제 금지**. 사양 변경 시에만 *명시적으로* 폐기/이전한다. |
| **REG-2** | REFACTOR 단계에서는 테스트 *코드*를 수정하지 않는다(production 코드만 수정). |
| **REG-3** | 새 기능 추가로 기존 테스트가 깨지면 **반드시 GREEN으로 복귀**시킨 뒤 커밋한다(Broken Window 금지). |
| **REG-4** | 테스트 추가는 환영, 기존 단정의 *약화*(예: `==` → `is not None`)는 금지. |
| **REG-5** | 6절 BR-01 ~ BR-20 각각이 *최소 1개 이상*의 회귀 테스트로 보호된다(NFR-08, 12절 매트릭스). |

### 9.3 테스트 데이터 (대표 4x4 행렬)

#### 9.3.1 D-Std — 표준 Dürer 마방진 (모든 합 = 34)

```
[ [16,  3,  2, 13],
  [ 5, 10, 11,  8],
  [ 9,  6,  7, 12],
  [ 4, 15, 14,  1] ]
```

| 합 | 값 |
|---|---|
| 행 1~4 | 34, 34, 34, 34 |
| 열 1~4 | 34, 34, 34, 34 |
| 주대각 ↘ | 16+10+7+1 = 34 |
| 부대각 ↙ | 13+11+6+4 = 34 |

#### 9.3.2 D-In-A — 시도 A로 풀리는 입력 예 (TC-N-01)

```
[ [ 0,  3,  2, 13],
  [ 5, 10, 11,  8],
  [ 9,  6,  7, 12],
  [ 4, 15, 14,  0] ]
```

- BlankPair = `((1,1), (4,4))`, MissingPair = `(small=1, large=16)`
- 시도 A: (1,1)←1, (4,4)←16 → 마방진 ✓ → 결과 `[1,1,1, 4,4,16]`

#### 9.3.3 D-In-B — 시도 B로 풀리는 입력 예 (TC-N-03)

> §11 결정 항목 R-2에 따라, 본 PRD는 D-In-B에 해당하는 *구체 행렬*의 확정을 다음 단계의 사전 검증 작업으로 이관한다.
> 다음 사전 검증 작업이 닫히기 전까지 TC-N-03은 *xfail* 또는 보류 상태로 두며, 닫히는 즉시 정식 GREEN 대상이 된다.

#### 9.3.4 D-Uns — 두 조합 모두 비-마방진 입력 예 (TC-F-09)

> §11 결정 항목 R-2와 동일 사유로 본 PRD는 D-Uns의 구체 행렬을 다음 단계로 이관한다.
> 단, *형태/값 범위/빈칸 개수/중복 검증은 모두 통과*하면서도 두 조합 모두 비-마방진인 행렬이 *적어도 하나 존재*하는 것은 본 PRD에서 가정한다(§11 R-2).

#### 9.3.5 D-Bad-Shape, D-Bad-Range, D-Bad-Blank, D-Bad-Dup

| ID | 행렬 (요지) | 기대 코드 |
|---|---|---|
| D-Bad-Shape | 3행 4열 | `E_SHAPE` |
| D-Bad-Range | D-Std에서 (1,1)을 `-1`로 변경 | `E_VALUE_RANGE`, `locus=(1,1)` |
| D-Bad-Blank | 빈칸 3개 | `E_BLANK_COUNT` |
| D-Bad-Dup | D-Std에서 (1,1)과 (4,4)를 모두 `7`로 변경 | `E_DUPLICATE` |

### 9.4 Property / Invariant 기반 검사 항목

| Prop ID | 속성 (모든 정상 입력에 대해 항상 참) | 보호 BR |
|---|---|---|
| **P-01** | `len(result) == 6` | BR-09 |
| **P-02** | `1 ≤ result[0], result[1], result[3], result[4] ≤ 4` (1-index) | BR-08 |
| **P-03** | `result[0]*4 + result[1] < result[3]*4 + result[4]` (row-major 순서) | BR-07 |
| **P-04** | `result[2] != result[5]` ∧ `{result[2], result[5]} ⊆ {1..16}` | BR-18 |
| **P-05** | 결과의 `n1, n2`를 입력에 채운 격자는 마방진이다(행/열/대각 합 모두 34). | BR-06 |
| **P-06** | 호출 전·후 입력 행렬이 byte-equal (deep equality). | BR-16 |
| **P-07** | 동일 입력 100회 호출 시 결과(또는 예외)가 모두 동일. | BR-15 |
| **P-08** | Boundary 위반 입력 1건은 정확히 1개의 도메인 실패 코드만 반환한다(다중 코드 0건). | BR-19 |

---

## 10. Architecture Overview (High-Level)

### 10.1 레이어 정의

| 레이어 | 책임 (SRP) | 포함 컴포넌트 | 의존 가능 대상 |
|---|---|---|---|
| **Boundary Layer** | 외부 호출자와의 입출력 경계. *입력 검증*(FR-01)과 *출력 형식 보존*(`int[6]` 그대로 노출). | `InputValidator`, `ResultFormatter`(필요 시) | Domain (안쪽) |
| **Domain Layer** | 마방진 도메인 *순수 로직*. *부작용 없음*, *외부 I/O 없음*. | `Board`, `BlankFinder` (FR-02), `MissingNumberFinder` (FR-03), `MagicSquareJudge` (FR-04), `FillPlanResolver` (FR-05), `MagicResultAssembler` (FR-05 출력 조립), 도메인 상수 모듈 (`GRID_SIZE=4`, `VALUE_RANGE=1..16`, `MAGIC_CONSTANT=34`, `RESULT_LENGTH=6`, `BLANK_MARKER=0`) | (없음) |

> 본 PRD는 `Report/02`의 3계층(Boundary/Control/Entity)을 **2-Track 관점**으로 재정렬한다.
> Domain Layer 내부에서 Control(`Validator`/`UseCase`/`Service`)와 Entity(`Grid`/`Constants`/`Violation`)의 분리는 `.cursorrules` `architecture.layers`를 그대로 따른다.
>
> ※ §13에서 정의되는 **Ops Track**은 위 표의 Boundary/Domain *어느 런타임 레이어에도 속하지 않는* **메타 레이어**(빌드/CI 시점에만 작동)이며, 본 표의 *의존 가능 대상*에는 포함되지 않는다(§13.1). 즉 의존성 방향 화살표(§10.3)는 *런타임* 의존성만 묘사하고, *빌드/CI 의존성*은 §13.6 별표에서 직교적으로 추적된다.

### 10.2 책임 분리 (SRP) 와 확장 (OCP) 전략

| 원칙 | 본 PRD 적용 |
|---|---|
| **SRP** | 도메인 서비스는 *단 하나의* 책임만 갖는다. `MagicSquareJudge`는 판정만, `BlankFinder`는 탐색만, `FillPlanResolver`는 조합 결정만. 한 서비스가 다른 서비스의 *내부*를 알지 않는다(입력/반환 VO만 결합). |
| **OCP** | 새로운 검증 규칙 추가는 *기존 서비스 수정 없이* 별도 검증기를 추가하는 방식으로 확장한다. 단, 본 PRD의 5개 FR 범위 내에서만 적용. |
| **DIP** | Boundary는 Domain의 *공개 함수 시그니처*에만 의존하고, 내부 구현에는 의존하지 않는다. Track A 테스트가 Domain Mock으로 통과한다는 사실 자체가 DIP를 보장한다(DT-4). |

### 10.3 의존성 방향 (변경 금지)

```
[ Caller / Test Driver ]
            │
            ▼
[ Boundary Layer ]
   - InputValidator      ── FR-01 검증 (E_SHAPE / E_VALUE_RANGE / E_BLANK_COUNT / E_DUPLICATE)
   - (정상 시 도메인 위임 1회)
            │
            ▼
[ Domain Layer ]
   - BlankFinder              (FR-02)
   - MissingNumberFinder      (FR-03)
   - MagicSquareJudge         (FR-04)
   - FillPlanResolver         (FR-05 핵심: A→B 시도 + E_UNSOLVABLE)
   - MagicResultAssembler     (FR-05 출력 조립)
   - DomainConstants          (Final 상수)
```

| 규칙 ID | 규칙 |
|---|---|
| **A-1** | 의존성 화살표는 위→아래 단방향. Domain은 Boundary를 *알지 못한다* (BR-17, NFR-09). |
| **A-2** | Boundary는 Domain VO를 외부 호출자에게 *그대로 노출하지 않는다*. 출력은 원시 `int[6]`으로 환원한다 (`Report/02` A-4). |
| **A-3** | Domain은 *추상 시그니처*만으로 동작하며, 구체 Boundary 구현체에 결합되지 않는다(DT-4). |
| **A-4** | 도메인 상수는 *단일 진실 출처*인 상수 모듈에서만 정의된다(NFR-06). |

---

## 11. Risks & Ambiguities

> 모호한 부분은 *결정 항목(Decision)* 으로 명시하여 본 PRD 단계에서 닫는다.

### 11.1 결정 항목 (Decision Log)

| ID | 모호 영역 | **결정** | 근거 |
|---|---|---|---|
| **R-1** | 두 시도 모두 실패 시 정책 | `E_UNSOLVABLE` 도메인 예외를 발생시킨다. boolean 반환·null 반환·-1 배열 반환은 모두 금지. | `Report/02` 0.4 / 1.4 / 2.1.3 F-5 |
| **R-2** | 두 시도 모두 실패 입력의 *존재 보장* | 본 PRD는 D-Uns 행렬이 *적어도 하나 존재*함을 가정한다. D-In-B 및 D-Uns의 *구체 행렬 확정*은 다음 단계(테스트 작성 직전 사전 검증)에서 닫는다. 닫히기 전까지 TC-N-03/TC-F-09는 보류 상태(`xfail` 허용). | 본 PRD §9.3.3, §9.3.4 |
| **R-3** | 비-정수 입력(float/문자열/None) | 본 PRD는 `int[][]`만 수락한다고 정의(0.1). 비-정수는 호출자/타입 시스템 책임으로 차단된다고 가정. 런타임 검증이 필요한 환경에서는 *형태 검증 통과 후 값 범위 검증 단계에서 `E_VALUE_RANGE`로 통일*한다. | 0.1, 4.2 O-7 |
| **R-4** | 입력 행렬의 변경 가능성 | **변경 금지** (BR-16, NFR-04). 채움 시뮬레이션은 *deep-copy* 위에서 수행한다. | `Report/01` I5 / `Report/02` 1.4.1 |
| **R-5** | 좌표 인덱싱 | **1-index 고정**. 0-index는 출력에서 *어떤 경우에도* 노출되지 않는다. | 0.2, BR-08 |
| **R-6** | 스캔 순서 | **row-major 고정**. column-major/대각 우선 등 다른 순서는 사용하지 않는다. | 0.1, BR-07 |
| **R-7** | 동일 입력 다중 위반 시 코드 결정 | FR-01 ①~⑤ 순서로 *첫 위반*의 코드를 단일 반환(BR-19). 다중 코드 동시 반환·합성 코드 모두 금지. | FR-01, BR-19 |
| **R-8** | 표준 메시지의 변경 가능성 | **byte-equal 고정**(NFR-07). 변경은 PRD 개정과 동시에 12절 매트릭스 갱신을 요구. | `Report/02` 2.4.1 M-1 |
| **R-9** | Domain 단계의 방어적 재검증 | Domain은 사전조건 위반에 대해 방어적 검증을 *중복 수행하지 않는다*. 단, 디버그 모드 `assert` 가드는 허용. | `Report/02` 1.4 |

### 11.2 자주 실수하는 포인트 (Pitfalls)

| 코드 | 실수 패턴 | 방지책 |
|---|---|---|
| **PT-1** | 출력 좌표를 0-index로 반환 | T-D-014, T-U-071, P-02 (1-index 단정) |
| **PT-2** | column-major로 빈칸 스캔 | T-D-013 (스캔 순서 단정) |
| **PT-3** | 입력 행렬을 직접 변경한 뒤 다시 복구 | T-INV-BR16, P-06 (호출 전 deep-copy 단정) |
| **PT-4** | 시도 A가 마방진인데도 시도 B를 호출 | AC-05-03 (단락 평가 단정), Mock 호출 횟수 단정 |
| **PT-5** | 두 시도 모두 실패 시 *정상* 결과(예: 빈 배열) 반환 | AC-05-04, T-D-032 (`E_UNSOLVABLE` 단정) |
| **PT-6** | 합이 34지만 중복 숫자 있는 격자에 `true` 반환 | AC-04-06, T-D-007 |
| **PT-7** | 표준 메시지에 입력 값 삽입(예: `"value -1 is invalid"`) | NFR-07, M-2 (메시지 byte-equal 단정) |
| **PT-8** | Domain 코드에서 Boundary 예외 import | A-1, BR-17, NFR-09 (정적 의존성 검사) |

### 11.3 Open Risk (계속 모니터링)

| Risk ID | 잠재 위험 | 모니터링 방법 |
|---|---|---|
| **OR-1** | 4x4 마방진 *해의 다중성*으로 인해 *예상 출력값* 검증이 흔들릴 가능성 | TC-N-01 등은 §9.4 D-Std 행렬에 한정해 *유일 결과*를 단정한다. 다른 마방진을 사용 시 별도 케이스로 분리. |
| **OR-2** | NFR-05(50ms) 상한이 학습 환경에 따라 흔들릴 가능성 | 절대 시간 단정 대신 *상한 마진*(예: 100회 호출 합 ≤ 5s)으로 약화 단정 검토. |
| **OR-3** | 표준 영문 메시지 변경 요청 가능성(국제화 압력) | NFR-07 + R-8: 변경 시 PRD 개정 + 매트릭스 갱신 동시 요구. |
| **OR-4** | CI 러너 환경 차이(OS/파이썬 버전/타임존)로 OG-7 결정성 검증 또는 OG-14 성능 상한이 *흔들릴* 가능성 | 컨테이너 이미지 핀(고정 태그) + CI 매트릭스 *최소화*(Linux 단일 행 권장). 비결정 발견 시 OPS-5 위반으로 간주하고 환경 핀을 우선 정리. |
| **OR-5** | OG-9(import-linter) / OG-11(Hypothesis) / OG-12(커스텀 docstring 파서) 등 *외부 도구 의존*의 도입·교체 비용 | §13.7에 따라 *대안 도구를 사전 후보로 등록*(예: `import-linter` ↔ `pydeps`/정적 grep, `Hypothesis` ↔ 수기 parametrize). 도구 교체 시 OG-12로 동등 보호 수준 자동 검증. |

---

## 12. Traceability Matrix (Concept → Rule → Use Case → Contract → Test → Component)

> 모든 행은 **6단 추적**(Concept/Invariant → Business Rule → Feature/Use Case → Acceptance Criteria(=Contract) → Test Case → Component) 이 가능해야 한다.
> 본 절은 NFR-08(추적성)의 산출물이며 **변경 금지** 대상이다.
>
> ※ 본 매트릭스는 *런타임 컴포넌트*(Boundary / Domain)만 추적한다. **Ops 게이트(OG-1 ~ OG-14)의 NFR/BR 보호 매핑은 §13.6 별표** 가 담당하며, *빌드/CI 메타 레이어*로서 본 매트릭스에 *직교*한다(§10.1 메모, §13.1 메타 트랙 정의 참조).

| Concept / Invariant | Business Rule | Feature (FR / Use Case) | Acceptance Criteria (Contract) | Test Case | Component |
|---|---|---|---|---|---|
| **I1** 형태 불변성 | BR-01, BR-03 | FR-01 (UC: 입력 검증) | AC-01-01, AC-01-02, AC-01-05 | T-U-001~T-U-005, T-U-020~T-U-023, TC-F-01, TC-F-02, TC-F-05~TC-F-07, T-INV-I1 | Boundary / `InputValidator` |
| **I2** 정의역 불변성 | BR-02 | FR-01 | AC-01-03, AC-01-04 | T-U-010~T-U-013, TC-F-03, TC-F-04, T-INV-I2 | Boundary / `InputValidator` |
| **I3** 유일성 불변성 (입력측) | BR-04 | FR-01 | AC-01-06 | T-U-030~T-U-032, TC-F-08 | Boundary / `InputValidator` |
| **I3** 유일성 불변성 (누락측) | BR-18 | FR-03 (UC: 누락 숫자 결정) | AC-03-03, AC-03-04 | T-D-020~T-D-023, T-INV-I3 | Domain / `MissingNumberFinder` |
| **I1** 보강 (스캔 순서) | BR-07 | FR-02 (UC: 빈칸 결정) | AC-02-01~AC-02-04 | T-D-010~T-D-014, P-03 | Domain / `BlankFinder` |
| **I4** 합 균질 (Magic) | BR-05, BR-06 | FR-04 (UC: 마방진 판정) | AC-04-01~AC-04-06 | T-D-001~T-D-007, T-INV-I4, P-05 | Domain / `MagicSquareJudge` |
| **I4** + 순서 규칙 (시도 A 우선) | BR-10, BR-12 | FR-05 (UC: 해 찾기) | AC-05-01, AC-05-03 | T-D-030, TC-N-01, TC-N-02 | Domain / `FillPlanResolver` |
| **I4** + 순서 규칙 (시도 B 차선) | BR-11, BR-13 | FR-05 | AC-05-02 | T-D-031, TC-N-03 | Domain / `FillPlanResolver` |
| **I4** 실패 식별성 | BR-14 | FR-05 | AC-05-04 | T-D-032, T-U-060, T-U-061, TC-F-09 | Domain / `FillPlanResolver` + Boundary 통과 |
| **I5** 결정성 | BR-15 | FR-02, FR-03, FR-04, FR-05 | AC-02-05, AC-03-05, AC-04-07, AC-05-09 | T-D-009, T-D-023, T-D-051, T-INV-I5, P-07 | All Domain |
| **I5** 부작용 금지 | BR-16 | FR-04, FR-05 | AC-04-08, AC-05-08 | T-INV-BR16, P-06 | Domain (전체) |
| **I5** 출력 좌표 규약 | BR-08, BR-09 | FR-05 (출력 조립) | AC-05-05, AC-05-07 | T-D-040~T-D-042, T-U-070~T-U-072, P-01, P-02, P-03 | Domain / `MagicResultAssembler` |
| **I5** 검증 우선순위 | BR-19 | FR-01 | AC-01-07~AC-01-09 | T-U-040~T-U-042, TC-P-01~TC-P-03 | Boundary / `InputValidator` |
| **I5** 메시지 byte-equal | BR-20 | FR-01, FR-05 | AC-01-12 | (메시지 동등성 단정 — Boundary/Domain 양 트랙) | Boundary + Domain |
| (메타) 의존성 방향 | BR-17 | (전 FR) | (NFR-09) | 정적 의존성 검사(import-linter), 코드 리뷰 | All |

### 12.1 역추적 체크리스트 (Reverse Traceability)

| 체크 | 항목 |
|---|---|
| ☐ | I1~I5의 *모든* Invariant가 최소 1개 이상의 BR로 환원되었는가? |
| ☐ | BR-01~BR-20의 *모든* 규칙이 최소 1개 이상의 Test Case로 보호되는가? |
| ☐ | FR-01~FR-05의 *모든* AC가 최소 1개 이상의 Test Case와 연결되는가? |
| ☐ | 모든 Test Case가 *정확히 하나*의 Component에 귀속되는가? |
| ☐ | 모든 도메인 실패 코드(`E_SHAPE`, `E_VALUE_RANGE`, `E_BLANK_COUNT`, `E_DUPLICATE`, `E_UNSOLVABLE`)가 *어디서 발생*하고 *어디서 노출*되는지 명시되었는가? |
| ☐ | 11절 결정 항목(R-1~R-9)의 *모든* 결정이 BR 또는 NFR 또는 AC에 반영되었는가? |
| ☐ | NFR-01~NFR-09의 *모든* 항목이 측정 도구·임계·미달 정책 3종을 갖추었는가? |

---

## 13. Ops & Automation (Quality Gates)

> 본 절은 §1 Executive Summary가 약속한 *"외부 도구가 자동 강제할 수 있는 형태"*의 **운영 계층**을 정의한다.
> 본 절은 §0 입출력 계약, §6 BR, §12 Traceability Matrix 그 어느 것도 *변경하지 않으며*, 오직 *자동 강제 메커니즘*만을 추가한다.
> 본 PRD가 다루는 것은 **Ops(자동화·품질 게이트)** 이며, **MLOps가 아니다** (OO-1 참조).

### 13.1 Ops Track의 위치 (§8 Dual-Track과 직교)

§8의 Track A(Boundary)·Track B(Domain)와 *직교하는 메타 트랙*으로 **Ops Track**을 둔다. Ops Track은 RED→GREEN→REFACTOR 사이클이 아니라 다음의 **G→GP→GR** 사이클을 따른다.

| Phase | 의미 | 산출 | 보호 대상 |
|---|---|---|---|
| **G — Gate 추가** | 새 자동화 게이트(워크플로/훅/검사기)를 추가하고 *현재 코드베이스가 통과/실패하는지* 확인한다. | CI 워크플로, pre-commit 훅, lint/type 설정 | §7 NFR |
| **GP — Gate Pass** | 추가된 게이트가 모든 PR/커밋에서 *결정적으로* 초록을 유지한다. | 게이트 통과 로그 | §6 BR-15 결정성 |
| **GR — Gate Refine** | 거짓 양성/거짓 음성 정리, 임계값 조정. *NFR을 약화하는 방향의 임계값 완화는 금지*. | 임계값 변경 PR | §7 NFR-01/02/03/05/08 |

### 13.2 자동화 게이트 카탈로그

| Gate ID | 게이트 | 도구 (예시) | 보호 NFR / BR | 실패 시 정책 |
|---|---|---|---|---|
| **OG-1** | 코드 포맷 강제 | Black | (코드 스타일) | PR 머지 차단 |
| **OG-2** | Lint (PEP 8 + pyflakes + PLR2004 매직 넘버) | Ruff | NFR-06 | PR 머지 차단 |
| **OG-3** | 타입 검사 | `mypy --strict` | (타입 안전성, `.cursorrules` `type_hints.enforcement`) | PR 머지 차단 |
| **OG-4** | 전체 단위 테스트 통과 | pytest | NFR-02, BR-19, BR-20 | PR 머지 차단 |
| **OG-5** | Domain 커버리지 ≥ 95% (라인) / ≥ 90% (분기) | `pytest-cov --cov-fail-under=95` | NFR-01 | PR 머지 차단 |
| **OG-6** | Boundary 커버리지 ≥ 85% (라인) | `pytest-cov --cov-fail-under=85` | NFR-02 | PR 머지 차단 |
| **OG-7** | 결정성 회귀 (동일 입력 100회 반복 동등성) | pytest 내 반복 단정 (T-INV-I5) | NFR-03 / BR-15 | PR 머지 차단 |
| **OG-8** | 부작용 금지 (호출 전·후 입력 byte-equal) | pytest 내 deep-copy 단정 (T-INV-BR16) | NFR-04 / BR-16 | PR 머지 차단 |
| **OG-9** | 의존성 방향 검사 (Domain → Boundary import 0건) | import-linter 또는 정적 grep 워크플로 | NFR-09 / BR-17 | PR 머지 차단 |
| **OG-10** | 표준 에러 메시지 byte-equal 회귀 (5종) | 문자열 동등성 단정 | NFR-07 / BR-20 | PR 머지 차단 |
| **OG-11** | Property-based 검사 (P-01 ~ P-08) | Hypothesis (선택) | §9.4 P-01 ~ P-08 | PR 머지 차단 |
| **OG-12** | Traceability 무결성 (Test ID ↔ §12 매핑 누락 0건) | 커스텀 스크립트 (테스트 docstring 파서) | NFR-08 | PR 머지 차단 |
| **OG-13** | Phase 혼합 커밋 검사 (DT-6 위반 0건) | 커밋 메시지 파서 + 변경 파일 분석 | DT-6 | PR 분할 요청 |
| **OG-14** | 성능 상한 회귀 (FR-05 단일 호출 P95 ≤ 50ms) | `pytest-benchmark` 또는 `time.perf_counter()` | NFR-05 | 회귀 발견 시 RED 추가 (즉시 차단은 아님) |

### 13.3 CI/CD 파이프라인 단계 (Stage Order)

다음 순서는 변경 가능하지만 *순서가 결정적이어야 한다*(BR-15 정신). 각 Stage 내 모든 게이트가 통과해야 다음 Stage로 진입한다(early-fail).

```
[Stage 1: Static]      OG-1  → OG-2  → OG-3
[Stage 2: Test]        OG-4  → OG-5  → OG-6
[Stage 3: Invariant]   OG-7  → OG-8  → OG-10 → OG-11
[Stage 4: Architecture] OG-9 → OG-12 → OG-13
[Stage 5: Performance] OG-14 (참고용, 차단성은 NFR-05 정책 따름)
```

| 규칙 ID | 규칙 |
|---|---|
| **OPS-1** | 로컬 pre-commit 훅과 CI 워크플로는 *동일 게이트 집합*을 실행한다. "로컬은 통과, CI는 실패" 상황을 만들지 않는다. |
| **OPS-2** | 게이트 임계값(예: 95%, 50ms)은 §7 NFR을 *약화하는 방향으로 변경할 수 없다*. 강화는 PR로 자유. |
| **OPS-3** | Ops Track의 변경(워크플로/훅/검사기 추가·교체)은 *별도 PR*로 제출한다. Track A/B의 RED·GREEN·REFACTOR 커밋과 혼합하지 않는다(DT-6 정신의 확장). |
| **OPS-4** | 게이트 일시 비활성화는 금지. 임시 우회가 필요하면 *PR을 닫고 게이트를 먼저 수정*한다(Broken Window 금지, REG-3 정신). |
| **OPS-5** | 모든 게이트는 *결정적*이어야 한다. 같은 커밋에 대해 100회 실행 시 동일 결과(통과/실패)를 반환한다(BR-15의 운영 측 확장). |

### 13.4 학습 관점에서의 Ops Track 가치

| 가치 ID | 가치 | 설명 |
|---|---|---|
| **V-1** | 외부 강제력 (Externalized Discipline) | "사람이 잊지 않으면 통과한다"가 아니라 "도구가 통과시키지 않으면 머지 못 한다"로 변환. C-2(검증 우선) 학습을 *자동화 수준*으로 끌어올린다. |
| **V-2** | 회귀 보호의 자동화 | §9.2 REG-1~REG-5를 사람이 아닌 게이트가 보호한다(특히 OG-7·OG-8·OG-10). |
| **V-3** | Trust Layer | Track A/B의 모든 RED→GREEN 전이가 *증명 가능한 형태*로 외부에 노출된다 — NFR-08의 Traceability를 OG-12가 자동 검사. |
| **V-4** | 학습 비용 → 0 한계 비용 | 학습자가 새 케이스를 추가할 때마다 *동일한 보호 수준*이 자동 적용. 학습 사이클의 *한계 비용*이 0에 수렴. |

### 13.5 명시적 비범위 (Ops Track Out-of-Scope)

| 코드 | 항목 | 사유 |
|---|---|---|
| **OO-1** | **MLOps 본래 의미의 모든 구성요소** (모델 학습/재학습 파이프라인, 학습 데이터 버저닝, 피처 스토어, 모델 레지스트리, 추론 서빙, 데이터/모델 드리프트 모니터링, A/B 테스트, 카나리 배포, 실험 추적) | 본 PRD의 도메인은 *결정론적* 마방진 판정이며, 학습 가능한 모델·학습 데이터셋·드리프트 개념이 *수학적으로 적용 불가능*. 형식만 빌리는 것은 §1 C-4("형식지로 환원") 원칙에 정면으로 위배됨. |
| **OO-2** | 컨테이너/오케스트레이션 (Docker / Kubernetes) | 학습 단위는 로컬 개발 환경 + CI 러너. 운영 배포는 본 PRD 범위 밖(§4.2 O-2 정신과 일관). |
| **OO-3** | APM / 런타임 모니터링 SaaS (Datadog, NewRelic 등) | 결정론적 단위 테스트가 1순위 보호 수단. 런타임 모니터링은 후속 단계로 이관. |
| **OO-4** | 시크릿 관리 / IAM / 인증 | UI/네트워크가 §4.2 O-1·O-2로 이미 배제되어 있어 시크릿 자체가 발생하지 않음. |
| **OO-5** | 인프라 프로비저닝 (Terraform 등) | 본 PRD는 *코드의 자동 강제*만 다룸. 인프라는 다음 학습 사이클. |

### 13.6 Traceability 보강 (Ops Gate ↔ NFR / BR)

> 본 표는 §12를 *대체하지 않으며*, §12의 행에 *직교하는 운영 측 추적*을 제공한다.

| Ops Gate | 보호 NFR | 보호 BR | 비고 |
|---|---|---|---|
| OG-1, OG-2, OG-3 | NFR-06 | — | Static stage |
| OG-4 | NFR-02 | BR-19, BR-20 | 전체 회귀 |
| OG-5 | NFR-01 | (Domain 전체 보호) | Domain 커버리지 |
| OG-6 | NFR-02 | (Boundary 전체 보호) | Boundary 커버리지 |
| OG-7 | NFR-03 | BR-15 | 결정성 회귀 |
| OG-8 | NFR-04 | BR-16 | 부작용 금지 회귀 |
| OG-9 | NFR-09 | BR-17 | 의존성 방향 |
| OG-10 | NFR-07 | BR-20 | 메시지 byte-equal |
| OG-11 | (NFR-08 보강) | BR-06 ~ BR-09 | Property로 환원 |
| OG-12 | NFR-08 | (메타) | Traceability 무결성 |
| OG-13 | (DT-6 운영) | (메타) | 혼합 커밋 차단 |
| OG-14 | NFR-05 | — | 성능 상한 회귀 |

### 13.7 본 절의 변경 통제

본 절은 **유연 변경 허용** 영역이다(§0/§6/§12와 달리 Frozen이 아님). 단:
- *임계값을 약화하는* 변경은 OPS-2에 따라 거부된다(예: 커버리지 임계 95% → 90% 하향 금지).
- *게이트를 삭제하는* 변경은 보호 NFR/BR이 *다른 게이트로 이전됨*이 증명될 때에만 허용된다.
- *도구 교체*(예: Ruff → 다른 린터)는 자유. 단 동일 보호 수준 유지가 OG-12 무결성 검사로 확인되어야 한다.

---

## 부록 A. 본 PRD 합의 게이트 (Pre-RED Gate)

다음 항목 *모두*에 ✅가 찍혔을 때에만 본 PRD를 *닫고* RED 테스트 작성 단계로 진입한다.

- [ ] 0절 입출력 계약이 *추가 변경 없이* 합의되었는가?
- [ ] 5절 FR-01~FR-05의 모든 AC가 *테스트 가능 문장*으로 환원되었는가?
- [ ] 6절 BR-01~BR-20이 *항상 참이어야 하는 술어*로 진술되었는가?
- [ ] 7절 NFR-01~NFR-09가 *측정 도구·임계·미달 정책*까지 명시되었는가?
- [ ] 8절 Dual-Track 병렬 진행 규칙(DT-1~DT-6)이 *진행 순서로 결정적*인가?
- [ ] 9절 테스트 데이터 D-Std/D-In-A의 모든 합이 34임이 *수기 검산*으로 확인되었는가?
- [ ] 11절 R-2(D-In-B/D-Uns 구체 행렬 확정)가 *다음 단계 작업*으로 *공식 이관*되었는가?
- [ ] 12절 매트릭스의 모든 행이 *Concept→Component까지 6단*이 비어 있지 않은가?
- [ ] 13절 Ops 게이트 카탈로그(OG-1 ~ OG-14)가 *모두 도입 가능한 도구*로 매핑되었고, OPS-1~OPS-5의 운영 규칙이 결정적인가?
- [ ] 13.5절 OO-1~OO-5(Ops Out-of-Scope)가 *명시적으로 배제*되어, "MLOps"라는 단어가 본 PRD에서 *오직 배제·구분 목적으로만* 등장함(§1, §13 인트로, §13.5 OO-1, 본 부록 A)을 확인했는가?

---

## 부록 B. 본 PRD가 후속 단계에 부과하는 제약

| 후속 단계 | 본 PRD가 부과한 제약 |
|---|---|
| **RED 테스트 작성** | 모든 새 테스트는 (a) docstring 또는 ID에 *어느 BR/AC를 보호*하는지 명시, (b) §8 Track 분류와 §12 매트릭스에 *동시 등록*. |
| **GREEN 구현** | 0절 계약·6절 BR·7절 NFR을 *위반하는 어떤 코드도* 작성하지 않는다. 임시 구현(하드코딩)은 REFACTOR에서 즉시 정리. |
| **REFACTOR** | 외부 동작·계약·메시지·검증 순서 *어느 것도* 변경하지 않는다(NFR-07, R-8). 모든 기존 테스트가 GREEN을 유지한다. |
| **PR 리뷰** | DT-6(혼합 커밋 금지)을 위반한 PR은 분할 요청 대상. |
| **회귀** | §9.2 REG-1~REG-5를 위반하는 어떤 변경도 거부된다. |
| **Ops 게이트 도입** | 모든 게이트 추가/교체는 *별도 PR*로 제출(OPS-3, DT-6 정신의 확장). 임계값 변경은 *강화 방향만* 허용(OPS-2 — NFR 약화 거부). 게이트 *일시 비활성화 금지*(OPS-4, REG-3 정신). 로컬 pre-commit과 CI는 *동일 게이트 집합*을 실행(OPS-1). |

---

## 마무리 진술

> **"본 PRD는 마방진을 풀기 위한 명세가 아니다.
> 본 PRD는 *불변 조건(I1~I5)을 먼저 진술하고, 검증을 먼저 설계하며, 입출력 계약을 byte-equal 수준으로 고정*한 채,
> Boundary와 Domain을 *각자 독립된 RED→GREEN→REFACTOR 사이클*로 운영하는 학습 시스템의 — *외부에서 검증 가능한* — 명세다."**

본 PRD가 닫히는 순간, RED 테스트는 *작성될 준비가 된 상태*가 된다. 그 RED는 본 PRD의 어떤 줄도 새로 만들 필요 없이, **§8 Test ID와 §12 매트릭스가 가리키는 자리**로 정확히 진입할 수 있어야 한다.
