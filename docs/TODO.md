# Magic Square (4x4) — 작업 보드 (To-Do)

> 본 보드는 **라이브 작업 큐**다. 진행 상황에 따라 *수시로 갱신*된다.
> *결정 박제용 스냅샷*은 `Report/10_*.md` (별도 PR로 산출)으로 분리한다 (PRD §13.7 OPS-3 정신).
>
> **출처 매핑**:
> - 항목 / 완료 조건 / 검증 기준 → `docs/PRD.md` (단일 진실 출처, 756줄)
> - 스토리 표현 → `Report/04_사용자여정_Epic.md`, `Report/06_사용자여정_UserStories.md`
> - 오류·계약 요약 → `docs/PRD.md` §0 / §0.3 / §8.1.2
> - 실행·ECB·TDD 규약 → `pyproject.toml` + `.cursorrules` + `Report/03_프로젝트_규약_정의.md`
> - 작업 분할/순서 → `Report/08` §6 + `Report/09` §6·§7
>
> **방법론**: Concept-to-Code Traceability(§12) · Dual-Track UI+Logic TDD(§8) · ECB(§10.1) · RED→GREEN→REFACTOR(DT-1~DT-6).
> **Scenario Level**: **L0** 기능 개요 / **L1** 정상 / **L2** 경계 / **L3** 실패.
> **상태 토큰**: ✅ PASS · 🔴 RED · 🟦 TODO · ⏸ BLOCKED · 🚧 IN_PROGRESS

---

## Epic-001 — 4x4 Magic Square 완성 시스템

**Goal**: 임의의 4x4 정수 격자(빈칸 정확히 2칸)에 대해 (a) Boundary 계약 위반은 5종 도메인 실패 코드 중 *단 하나*로 거부하고, (b) 누락된 두 숫자를 PRD §0.2의 두 시도(A→B) 규칙대로 채워 *byte-equal* `int[6]`을 결정적으로 반환하거나, 두 시도 모두 실패 시 `E_UNSOLVABLE`을 발생시키는 *순수 로직* 시스템을 Dual-Track TDD로 산출한다.

**Definition of Done**
- [ ] PRD §12 Traceability Matrix의 모든 행이 *최소 1개* GREEN 테스트로 보호됨 (NFR-08)
- [ ] OG-1 ~ OG-8, OG-10 모두 CI에서 결정적 통과 (PRD §13.3 Stage 1·2·3)
- [ ] OG-5(Domain 95% 라인 / 90% 분기), OG-6(Boundary 85% 라인) 통과
- [ ] PRD §11.3 R-2가 닫히고 D-In-B / D-Uns 구체 행렬이 §9.3에 박제됨
- [ ] `Report/09` §5의 미충족 항목 중 OG-9/11/12/13가 별도 PR로 도입됨 (OPS-3)

---

## User Stories (Report/06 발췌)

| US ID | 페르소나 (PRD §3) | 요지 |
|---|---|---|
| **US-001** | U-1 TDD 학습자 | Track A·B의 첫 RED를 *같은 작업 세션 안에* 동시 작성 (DT-1) |
| **US-002** | U-3 호출자 | `int[][]` 한 개에 대해 *항상* `int[6]` 또는 5종 중 *정확히 하나*의 도메인 예외 (BR-15·19) |
| **US-003** | U-2 코드 리뷰어 | 임의 테스트 ID → §12 매트릭스로 30초 내 역추적 (NFR-08) |
| **US-004** | U-4 Ops 운영자 | OG-1~14 결정적 통과 + *임계값 약화 PR 0건* (OPS-2·5) |

---

## US-000: Pre-RED 진입 게이트 박제 *(PRD 부록 A)*

- [ ] **TASK-001**: 부록 A 10개 항목 ✅ 박제
  - `Code: Report/10_Pre_RED_Closure_Log.md (신설)`  ·  `ECB: (메타)`  ·  `Req: PRD 부록 A`
  > [Checkpoint] 10개 항목 모두 ✅ — 미충족은 *왜 닫지 않는지* 외부화

- [ ] **TASK-002**: D-In-B / D-Uns 구체 4x4 행렬 확정 *(R-2 종결)*
  - `Code: docs/PRD.md §9.3.3, §9.3.4`  ·  `ECB: Entity (테스트 데이터)`  ·  `Req: PRD §11.3 R-2`
  * 선택: 수기 검산 vs Hypothesis 자동 탐색 → **수기 검산** (학습 목적)
  > [Checkpoint] D-In-B = 시도A `false` ∧ 시도B `true`, D-Uns = 두 시도 모두 `false`

- [ ] **TASK-003**: pre-commit 환경 1회 실행 박제 *(`Report/09` §7)*
  - `Code: (없음)`  ·  `ECB: (메타·Ops G)`  ·  `Req: OG-1·2·3 / OPS-1`
  > [Checkpoint] black/ruff/mypy 0건 + `mirrors-mypy` 환경 호환성 확인

---

## US-001: Boundary 입력 검증 *(FR-01)*

- [ ] **TASK-010**: 형태 검증 (`E_SHAPE`)
  - [ ] **TASK-010-1**: `T-U-001` RED — 3행 입력 → `E_SHAPE` *(DT-1 짝)*
  - [ ] **TASK-010-2**: `T-U-002`~`T-U-005` GREEN — 5행 / 한 행 짧음 / 한 행 김 / 빈 배열
  - [ ] **TASK-010-3**: REFACTOR — 5규칙 평가를 *결정적 순서 체인*으로 정리
  - `Code: src/magicsquare/boundary/input_validator.py`  ·  `ECB: Boundary`  ·  `Req: FR-01①, BR-01, AC-01-01·02`
  > [Checkpoint] 메시지 byte-equal: `"Input must be a 4x4 matrix."`

- [ ] **TASK-011**: 값 범위 검증 (`E_VALUE_RANGE`)
  - [ ] **TASK-011-1**: `T-U-010` RED — 음수 셀
  - [ ] **TASK-011-2**: `T-U-011`~`T-U-013` GREEN — 17 / 100 / `locus` 좌표(1-index)
  - [ ] **TASK-011-3**: REFACTOR — `locus` 추출을 별도 함수로 분리
  - `Code: boundary/input_validator.py`  ·  `ECB: Boundary`  ·  `Req: FR-01③, BR-02, AC-01-03·04`
  * 선택: `locus` 반환 형식 → **튜플 `(r,c)` 1-index** (PT-1 회피)
  > [Checkpoint] 메시지에 입력 값 미포함 (NFR-07 / PT-7)

- [ ] **TASK-012**: 빈칸 개수 검증 (`E_BLANK_COUNT`)
  - [ ] **TASK-012-1**: `T-U-020` RED — 빈칸 0개
  - [ ] **TASK-012-2**: `T-U-021`~`T-U-023` GREEN — 1 / 3 / 4개
  - [ ] **TASK-012-3**: REFACTOR
  - `Code: boundary/input_validator.py`  ·  `ECB: Boundary`  ·  `Req: FR-01④, BR-03, AC-01-05`

- [ ] **TASK-013**: 중복 검증 (`E_DUPLICATE`)
  - [ ] **TASK-013-1**: `T-U-030` RED — 7이 두 번 등장
  - [ ] **TASK-013-2**: `T-U-031`~`T-U-032` GREEN — 3회 중복 + 0 두 개 정상 위임
  - [ ] **TASK-013-3**: REFACTOR — multiset 비교 로직 통합
  - `Code: boundary/input_validator.py`  ·  `ECB: Boundary`  ·  `Req: FR-01⑤, BR-04, AC-01-06`

- [ ] **TASK-014**: 검증 우선순위 *(다중 위반 시 단일 코드)*
  - [ ] **TASK-014-1**: `T-U-040` RED — 형태+값 동시 → `E_SHAPE`
  - [ ] **TASK-014-2**: `T-U-041`~`T-U-042` GREEN — 값+빈칸 / 빈칸+중복
  - [ ] **TASK-014-3**: REFACTOR — *순서 변경 시 깨지는 회귀 테스트*가 존재하도록 보강
  - `Code: boundary/input_validator.py`  ·  `ECB: Boundary`  ·  `Req: BR-19, AC-01-07·08·09, R-7`
  > [Checkpoint] 한 입력 → *단 하나의 코드*만 반환 (다중/합성 코드 0건)

- [ ] **TASK-015**: Domain 위임 횟수 + 결과 패스스루
  - [ ] **TASK-015-1**: `T-U-050` RED — Domain Mock 호출 1회 (정상)
  - [ ] **TASK-015-2**: `T-U-051`~`T-U-052` GREEN — 위반 시 0회 / 결과 변형 없음
  - [ ] **TASK-015-3**: REFACTOR — Mock 인터페이스 추상화
  - `Code: boundary/input_validator.py`  ·  `ECB: Boundary (DT-4 Mock)`  ·  `Req: AC-01-10·11, A-3 DIP`

- [ ] **TASK-016**: Domain 예외 패스스루 + 출력 포맷 보존
  - [ ] **TASK-016-1**: `T-U-060`~`T-U-061` RED — `E_UNSOLVABLE` 가공 없이 노출
  - [ ] **TASK-016-2**: `T-U-070`~`T-U-074` GREEN — 길이 6 / 1-index / row-major / `n1≠n2` / `n∈{1..16}`
  - [ ] **TASK-016-3**: REFACTOR — `result_formatter` 분리 (필요 시)
  - `Code: boundary/result_formatter.py`  ·  `ECB: Boundary`  ·  `Req: BR-08·09·14·18, AC-05-04·05·06·07, A-2`

---

## US-002: Domain Entity 골격 *(상태 표현)*

- [ ] **TASK-020**: 도메인 상수 모듈 신설
  - [ ] **TASK-020-1**: 첫 RED(`T-U-001`+`T-D-001`)가 import 요구하는 시점에 RED 트리거
  - [ ] **TASK-020-2**: GREEN — `GRID_SIZE=4`, `VALUE_RANGE=(1,16)`, `MAGIC_CONSTANT=34`, `RESULT_LENGTH=6`, `BLANK_MARKER=0`, 5종 메시지
  - [ ] **TASK-020-3**: REFACTOR — `Final` 타입 강제 + `__all__` 정리
  - `Code: src/magicsquare/entity/constants.py`  ·  `ECB: Entity`  ·  `Req: NFR-06, BR-05·20, A-4`
  > [Checkpoint] `ruff check` PLR2004 = 0건

- [ ] **TASK-021**: `Board` 불변 VO
  - [ ] **TASK-021-1**: 부작용 금지 RED — `__setattr__` 차단 단정
  - [ ] **TASK-021-2**: GREEN — `@dataclass(frozen=True)` 또는 `tuple[tuple[int,...],...]` 래퍼
  - [ ] **TASK-021-3**: REFACTOR — 좌표 접근자(`at(r, c)` 1-index) 캡슐화
  - `Code: src/magicsquare/entity/board.py`  ·  `ECB: Entity`  ·  `Req: BR-16, NFR-04, R-4`
  * 선택: dataclass(frozen) vs 명시적 tuple 래퍼 → **dataclass(frozen=True)** (가독성)

- [ ] **TASK-022**: VO 분리 (`BlankPair`, `MissingPair`, `Violation`)
  - [ ] **TASK-022-1**: RED — VO 생성 시 사전조건(빈칸 2개 / 누락 2개) 단정
  - [ ] **TASK-022-2**: GREEN — `entity/blank_pair.py`, `entity/missing_pair.py`, `entity/violation.py`
  - [ ] **TASK-022-3**: REFACTOR — VO 간 *내부 모름* (SRP) 검증
  - `Code: entity/blank_pair.py · entity/missing_pair.py`  ·  `ECB: Entity`  ·  `Req: SRP, A-3`

- [ ] **TASK-023**: 도메인 예외 계층
  - [ ] **TASK-023-1**: RED — `UnsolvableError` raise 단정
  - [ ] **TASK-023-2**: GREEN — `BoundaryError`/`DomainError` 계층 + 5종 표준 메시지 결합
  - [ ] **TASK-023-3**: REFACTOR
  - `Code: entity/exceptions.py`  ·  `ECB: Entity`  ·  `Req: PRD §0.3, NFR-07, BR-20`

---

## US-003: 마방진 판정 *(FR-04 — Logic Track 첫 RED)*

- [ ] **TASK-030**: D6 술어 — 표준 마방진
  - [ ] **TASK-030-1**: `T-D-001` RED — D-Std → `true` *(DT-1 짝, TASK-010-1과 같은 세션)*
  - [ ] **TASK-030-2**: GREEN — 행/열/주대각/부대각 4종 합 단정
  - [ ] **TASK-030-3**: REFACTOR — 합 계산을 `sum()` 기반으로 단순화
  - `Code: src/magicsquare/control/magic_square_judge.py`  ·  `ECB: Control`  ·  `Req: FR-04, AC-04-01, BR-06, I4`
  > [Checkpoint] DT-6 — TASK-010-1과 *다른 커밋*

- [ ] **TASK-031**: D6 술어 — 비-마방진 케이스
  - [ ] **TASK-031-1**: `T-D-002`·`T-D-003` RED — 회전 변형 / 행 합 33
  - [ ] **TASK-031-2**: `T-D-004`~`T-D-006` GREEN — 열 35 / 주대각 어긋남 / 부대각 어긋남
  - [ ] **TASK-031-3**: REFACTOR
  - `Code: control/magic_square_judge.py`  ·  `ECB: Control`  ·  `Req: AC-04-02·03·04·05`

- [ ] **TASK-032**: I3 보호 — 합 34 + 중복 → false *(PT-6)*
  - [ ] **TASK-032-1**: `T-D-007` RED — 한 값을 4회 반복한 격자
  - [ ] **TASK-032-2**: GREEN — multiset 단정 추가
  - [ ] **TASK-032-3**: REFACTOR — 단정 순서를 *짧은 회피* 우선으로 정리
  - `Code: control/magic_square_judge.py`  ·  `ECB: Control`  ·  `Req: AC-04-06, I3, PT-6`

- [ ] **TASK-033**: 부작용 금지 + 결정성 *(컴포넌트 단위)*
  - [ ] **TASK-033-1**: `T-D-008` RED — 호출 전·후 byte-equal
  - [ ] **TASK-033-2**: `T-D-009` GREEN — 100회 반복 동등성
  - [ ] **TASK-033-3**: REFACTOR — read-only 인터페이스 명시
  - `Code: control/magic_square_judge.py`  ·  `ECB: Control`  ·  `Req: BR-15·16, AC-04-07·08, NFR-03·04`
  > [Checkpoint] OG-7·OG-8 첫 적용 지점

---

## US-004: 빈칸 탐지 *(FR-02)*

- [ ] **TASK-040**: `BlankFinder` 구현
  - [ ] **TASK-040-1**: `T-D-010` RED — 같은 행 두 빈칸 → `c1 < c2`
  - [ ] **TASK-040-2**: `T-D-011`~`T-D-014` GREEN — 다른 행 / 인접 / row-major 순서 / 1-index
  - [ ] **TASK-040-3**: REFACTOR — generator 기반으로 단일 패스
  - `Code: src/magicsquare/control/blank_finder.py`  ·  `ECB: Control + Entity(BlankPair)`  ·  `Req: FR-02, BR-07, AC-02-01~04, I1`
  * 선택: row-major 단일 패스 vs `numpy.where` → **순수 Python 단일 패스** (NFR-09: 외부 의존 0건)
  > [Checkpoint] 0-index 누설 0건 (PT-1)

---

## US-005: 후보값 필터링 *(FR-03 — 누락 숫자 결정)*

- [ ] **TASK-050**: `MissingNumberFinder` 구현
  - [ ] **TASK-050-1**: `T-D-020` RED — 1과 16 누락 → `(1, 16)`
  - [ ] **TASK-050-2**: `T-D-021`~`T-D-022` GREEN — 7,8 누락 / (12,3) 발견 시 (3,12) 정렬
  - [ ] **TASK-050-3**: REFACTOR — `set` 차집합 기반 단순화
  - `Code: control/missing_number_finder.py`  ·  `ECB: Control + Entity(MissingPair)`  ·  `Req: FR-03, BR-18, AC-03-01~03, I3(누락측)`
  * 선택: `set({1..16}) - filled` vs 카운팅 정렬 → **set 차집합** (가독성 + 결정성)

- [ ] **TASK-051**: 결정성 단정 + `small != large` 보장
  - [ ] **TASK-051-1**: `T-D-023` RED — 100회 호출 동등성
  - [ ] **TASK-051-2**: GREEN — 사후 단정 추가
  - [ ] **TASK-051-3**: REFACTOR
  - `Code: control/missing_number_finder.py`  ·  `ECB: Control`  ·  `Req: AC-03-04·05, BR-15`

---

## US-006: 완성 로직 *(FR-05 — 두 시도 + 결과 조립)*

- [ ] **TASK-060**: `FillPlanResolver` — 시도 A
  - [ ] **TASK-060-1**: `T-D-030` RED — D-In-A → `(small, large)` 반환
  - [ ] **TASK-060-2**: GREEN — `(first ← small, second ← large)` 채움 후 FR-04 호출
  - [ ] **TASK-060-3**: REFACTOR — 채움 시뮬레이션을 `_attempt(plan)` 헬퍼로 추출
  - `Code: src/magicsquare/control/fill_plan_resolver.py`  ·  `ECB: Control`  ·  `Req: FR-05③, BR-10·12, AC-05-01`

- [ ] **TASK-061**: `FillPlanResolver` — 시도 B *(차선)*
  - [ ] **TASK-061-1**: `T-D-031` RED — D-In-B → `(large, small)` 반환
  - [ ] **TASK-061-2**: GREEN — 시도 A 실패 시에만 시도 B 호출
  - [ ] **TASK-061-3**: REFACTOR
  - `Code: control/fill_plan_resolver.py`  ·  `ECB: Control`  ·  `Req: FR-05④, BR-11·13, AC-05-02`
  > [Checkpoint] TASK-002 종결 전에는 `xfail` 마크 (PRD §11 R-2)

- [ ] **TASK-062**: 시도 A 성공 시 시도 B 미호출 *(단락 평가, PT-4)*
  - [ ] **TASK-062-1**: RED — Mock 호출 횟수 단정 추가
  - [ ] **TASK-062-2**: GREEN — early-return 구현
  - [ ] **TASK-062-3**: REFACTOR
  - `Code: control/fill_plan_resolver.py`  ·  `ECB: Control`  ·  `Req: AC-05-03`

- [ ] **TASK-063**: `MagicResultAssembler` — `int[6]` 조립
  - [ ] **TASK-063-1**: `T-D-040` RED — 1-index 좌표 + 길이 6
  - [ ] **TASK-063-2**: `T-D-041`~`T-D-042` GREEN — 중간 좌표 / row-major 순서
  - [ ] **TASK-063-3**: REFACTOR — Resolver와의 책임 분리 검증
  - `Code: src/magicsquare/control/magic_result_assembler.py`  ·  `ECB: Control`  ·  `Req: BR-08·09, AC-05-05·07`

- [ ] **TASK-064**: 도메인 End-to-End 오케스트레이션
  - [ ] **TASK-064-1**: `T-D-050` RED — 정상 입력 → `int[6]`
  - [ ] **TASK-064-2**: `T-D-051`~`T-D-052` GREEN — 결정성 / 실패 경로
  - [ ] **TASK-064-3**: REFACTOR — `solve(matrix) -> int[6]` 단일 진입점
  - `Code: src/magicsquare/control/magic_square_solver.py`  ·  `ECB: Control`  ·  `Req: FR-05 전체, AC-05-09`

---

## US-007: 잘못된 입력 처리 *(통합 실패 시나리오)*

- [ ] **TASK-070**: `E_UNSOLVABLE` — 두 시도 모두 실패
  - [ ] **TASK-070-1**: `T-D-032` RED — D-Uns 입력 → `UnsolvableError`
  - [ ] **TASK-070-2**: `TC-F-09` GREEN — 통합 시나리오로 검증
  - [ ] **TASK-070-3**: REFACTOR — 메시지 byte-equal 보강
  - `Code: control/fill_plan_resolver.py`  ·  `ECB: Control + Entity(예외)`  ·  `Req: BR-14, AC-05-04, R-1`
  > [Checkpoint] 메시지 byte-equal: `"No valid magic square completion exists for the given input."`

- [ ] **TASK-071**: 부작용 금지 — 채움은 *복사본* 위에서만 *(BR-16, R-4)*
  - [ ] **TASK-071-1**: `T-INV-BR16` RED — 호출 전 deep-copy 단정
  - [ ] **TASK-071-2**: GREEN — `copy.deepcopy` 또는 frozen tuple 변환
  - [ ] **TASK-071-3**: REFACTOR
  - `Code: control/fill_plan_resolver.py`  ·  `ECB: Control`  ·  `Req: BR-16, NFR-04, PT-3`

- [ ] **TASK-072**: 실패 시나리오 9종 통합 *(`TC-F-01`~`TC-F-09`)*
  - [ ] **TASK-072-1**: RED — 9개 시나리오 parametrize
  - [ ] **TASK-072-2**: GREEN — 모두 PASS
  - [ ] **TASK-072-3**: REFACTOR — 시나리오 데이터를 `tests/fixtures/`로 추출
  - `Code: tests/test_scenarios_failure.py`  ·  `ECB: 통합`  ·  `Req: PRD §9.1.2 전체`

- [ ] **TASK-073**: 검증 우선순위 시나리오 3종 *(`TC-P-01`~`TC-P-03`)*
  - [ ] **TASK-073-1**: RED
  - [ ] **TASK-073-2**: GREEN
  - [ ] **TASK-073-3**: REFACTOR
  - `Code: tests/test_scenarios_priority.py`  ·  `ECB: Boundary`  ·  `Req: BR-19, R-7, PRD §9.1.3`

---

## US-008: 정상 시나리오 통합 *(`TC-N-01`~`TC-N-05`)*

- [ ] **TASK-080**: 정상 시나리오 5종
  - [ ] **TASK-080-1**: `TC-N-01` RED — D-In-A 코너 두 칸
  - [ ] **TASK-080-2**: `TC-N-02`~`TC-N-05` GREEN — 같은 행 / 시도 B만 / 주대각 위 / 부대각 위
  - [ ] **TASK-080-3**: REFACTOR — fixture 추출
  - `Code: tests/test_scenarios_normal.py`  ·  `ECB: 통합`  ·  `Req: PRD §9.1.1, AC-05 전체`

- [ ] **TASK-081**: 표준 메시지 5종 byte-equal 회귀 *(NFR-07)*
  - [ ] **TASK-081-1**: RED — 5개 메시지 동등성 단정
  - [ ] **TASK-081-2**: GREEN
  - [ ] **TASK-081-3**: REFACTOR — 메시지 카탈로그 단일 진실 출처 검증
  - `Code: tests/test_standard_messages.py · entity/constants.py`  ·  `ECB: Entity`  ·  `Req: NFR-07, BR-20, OG-10, R-8`

---

## US-009: 불변조건 + Property 회귀 *(I1~I5, P-01~P-08)*

- [ ] **TASK-090**: I1~I5 불변조건 테스트
  - [ ] **TASK-090-1**: `T-INV-I1`·`T-INV-I2` RED
  - [ ] **TASK-090-2**: `T-INV-I3`·`T-INV-I4`·`T-INV-I5` GREEN
  - [ ] **TASK-090-3**: REFACTOR — 단정을 invariant 모듈로 추출
  - `Code: tests/entity/test_invariants.py`  ·  `ECB: Entity`  ·  `Req: I1~I5, BR-01·02·04·05·06·15`

- [ ] **TASK-091**: Property 검사 8종 *(P-01 ~ P-08)*
  - [ ] **TASK-091-1**: RED — Hypothesis strategy 정의
  - [ ] **TASK-091-2**: GREEN — 8개 Property 단정
  - [ ] **TASK-091-3**: REFACTOR — strategy 재사용
  - `Code: tests/control/test_properties.py`  ·  `ECB: 통합`  ·  `Req: PRD §9.4 전체`
  * 선택: Hypothesis vs 수기 `parametrize` → **Hypothesis** (OR-5 폴백 옵션 보존)
  > [Checkpoint] OG-11 별도 PR (OPS-3)

---

## US-010: 테스트 커버리지 체크포인트 *(Ops Track G→GP→GR)*

- [ ] **TASK-100**: OG-5 / OG-6 임계값 *상향* PR
  - [ ] **TASK-100-1**: 현재 커버리지 측정 (`pytest --cov` 실행)
  - [ ] **TASK-100-2**: `pyproject.toml` `--cov-fail-under=95` (Domain) / `=85` (Boundary)
  - [ ] **TASK-100-3**: REFACTOR — `# pragma: no cover` 정당 사유 주석 검증
  - `Code: pyproject.toml · ci.yml`  ·  `ECB: (메타·Ops)`  ·  `Req: NFR-01·02, OPS-2`
  > [Checkpoint] *약화 0건* 박제 — `Report/09` OD-2 의무 종결

- [ ] **TASK-101**: OG-9 도입 — `import-linter` (의존성 방향)
  - `Code: .importlinter · pyproject.toml [opt-strict] · ci.yml Stage 4`  ·  `ECB: (메타·Ops)`  ·  `Req: NFR-09, BR-17, A-1, PT-8`
  > [Checkpoint] Domain → Boundary import 0건 자동 검증

- [ ] **TASK-102**: OG-12 도입 — Traceability 무결성 스크립트
  - `Code: tools/check_traceability.py`  ·  `ECB: (메타·Ops)`  ·  `Req: NFR-08, V-3`
  > [Checkpoint] PRD §12.1 역추적 체크리스트 7항목 자동화

- [ ] **TASK-103**: OG-13 도입 — Phase 혼합 커밋 차단
  - `Code: tools/check_phase_commit.py · pre-commit local hook`  ·  `ECB: (메타·Ops)`  ·  `Req: DT-6, OPS-3`

- [ ] **TASK-104**: OG-14 도입 — 성능 상한 (`pytest-benchmark`)
  - `Code: tests/perf/test_solver_perf.py · ci.yml Stage 5`  ·  `ECB: (메타·Ops)`  ·  `Req: NFR-05, OR-2`
  * 선택: 절대 시간 vs 상한 마진 → **상한 마진(100회 합 ≤ 5s)** 권장 (OR-2)

---

## Requirements 추적 매트릭스

> *Task → Req → Scenario → Test → Status* — 이 연결고리가 **C2C Traceability**의 실천.
> 진행 상태는 작업 진행에 따라 갱신.

| Task ID | Req ID | Scenario | 테스트 | 상태 |
|---|---|---|---|---|
| TASK-001 | 부록 A | L0 | (합의 게이트) | 🟦 TODO |
| TASK-002 | R-2 | L0 | TC-N-03 / TC-F-09 | 🟦 TODO |
| TASK-003 | OG-1·2·3 | L0 | pre-commit run | 🟦 TODO |
| TASK-010 | FR-01①, BR-01 | L3 Fail | T-U-001~005 | 🟦 TODO |
| TASK-011 | FR-01③, BR-02 | L3 Fail | T-U-010~013 | 🟦 TODO |
| TASK-012 | FR-01④, BR-03 | L3 Fail | T-U-020~023 | 🟦 TODO |
| TASK-013 | FR-01⑤, BR-04 | L3 Fail | T-U-030~032 | 🟦 TODO |
| TASK-014 | BR-19 | L2 Edge | T-U-040~042, TC-P-01~03 | 🟦 TODO |
| TASK-015 | AC-01-10·11 | L1 Happy | T-U-050~052 | 🟦 TODO |
| TASK-016 | BR-08·09·14 | L1 + L3 | T-U-060~061, T-U-070~074 | 🟦 TODO |
| TASK-020 | NFR-06, BR-05 | L0 | (import 트리거) | 🟦 TODO |
| TASK-021 | BR-16, NFR-04 | L2 Edge | (불변 단정) | 🟦 TODO |
| TASK-022 | SRP, A-3 | L0 | (VO 사전조건) | 🟦 TODO |
| TASK-023 | PRD §0.3, NFR-07 | L3 Fail | (예외 raise 단정) | 🟦 TODO |
| TASK-030 | FR-04, BR-06 | L1 Happy | T-D-001 | 🟦 TODO |
| TASK-031 | AC-04-02~05 | L3 Fail | T-D-002~006 | 🟦 TODO |
| TASK-032 | AC-04-06, I3 | L2 Edge | T-D-007 | 🟦 TODO |
| TASK-033 | BR-15·16 | L2 Edge | T-D-008·009 | 🟦 TODO |
| TASK-040 | FR-02, BR-07 | L1 + L2 | T-D-010~014 | 🟦 TODO |
| TASK-050 | FR-03, BR-18 | L1 + L2 | T-D-020~022 | 🟦 TODO |
| TASK-051 | AC-03-04·05 | L2 Edge | T-D-023 | 🟦 TODO |
| TASK-060 | FR-05③, BR-10·12 | L1 Happy | T-D-030, TC-N-01·02 | 🟦 TODO |
| TASK-061 | FR-05④, BR-11·13 | L2 Edge | T-D-031, TC-N-03 | ⏸ BLOCKED *(TASK-002 대기)* |
| TASK-062 | AC-05-03 | L2 Edge | (Mock 호출 횟수) | 🟦 TODO |
| TASK-063 | BR-08·09 | L1 + L2 | T-D-040~042 | 🟦 TODO |
| TASK-064 | FR-05 전체 | L1 + L2 + L3 | T-D-050~052 | 🟦 TODO |
| TASK-070 | BR-14, R-1 | L3 Fail | T-D-032, TC-F-09 | ⏸ BLOCKED *(TASK-002 대기)* |
| TASK-071 | BR-16 | L2 Edge | T-INV-BR16 | 🟦 TODO |
| TASK-072 | PRD §9.1.2 | L3 Fail | TC-F-01~09 | 🟦 TODO |
| TASK-073 | BR-19 | L2 Edge | TC-P-01~03 | 🟦 TODO |
| TASK-080 | PRD §9.1.1 | L1 Happy | TC-N-01~05 | 🟦 TODO |
| TASK-081 | NFR-07, BR-20 | L3 Fail | (메시지 동등성) | 🟦 TODO |
| TASK-090 | I1~I5 | L2 Edge | T-INV-I1~I5 | 🟦 TODO |
| TASK-091 | PRD §9.4 P-01~08 | L2 Edge | P-01~08 | 🟦 TODO |
| TASK-100 | NFR-01·02 | L0 | (커버리지 게이트) | 🟦 TODO |
| TASK-101 | NFR-09, BR-17 | L0 | (import-linter) | 🟦 TODO |
| TASK-102 | NFR-08 | L0 | (traceability 스크립트) | 🟦 TODO |
| TASK-103 | DT-6 | L0 | (phase 커밋 검사) | 🟦 TODO |
| TASK-104 | NFR-05 | L0 | (perf benchmark) | 🟦 TODO |

---

## 진입 큐 (다음 5개 커밋)

| 순서 | TASK | Phase | 비고 |
|---|---|---|---|
| ① | TASK-001 | (Pre-RED) | 부록 A ✅ 박제 — 본 단계가 닫혀야 PRD가 *닫힘* |
| ② | TASK-002 | (Pre-RED) | R-2 종결 — TASK-061·070의 BLOCKED 해제 |
| ③ | TASK-003 | (Pre-RED) | 환경 1회 박제 — `pre-commit run --all-files` 통과 |
| ④ | TASK-010-1 + TASK-030-1 | RED (DT-1 한 쌍) | *같은 작업 세션, 다른 커밋* (DT-6) |
| ⑤ | TASK-014 (Stage 2 우회 제거) | GREEN | 첫 GREEN 직후 `ci.yml` exit-code 5 우회 *제거 의무* (`Report/09` §6) |

---

## 회귀 보호 자동 차단 (ECB·TDD 위반)

| 위반 패턴 | 차단 도구 | 보호 출처 |
|---|---|---|
| `boundary/*.py`에서 `MAGIC_CONSTANT` 등 도메인 상수 직접 사용 | OG-2 (`PLR2004`) + 코드 리뷰 | NFR-06 / `.cursorrules` forbidden #2 |
| `boundary/*.py`에서 행/열 합 계산 등 비즈니스 규칙 수행 | 수기 리뷰 + (향후) AST 검사 | `.cursorrules` `architecture.boundary.must_not` |
| `entity/*.py` / `control/*.py`에서 `boundary` import | OG-9 (TASK-101) | BR-17 / NFR-09 / `.cursorrules` `dependency_direction` |
| `control/*.py`에서 입력 행렬 직접 변경 | OG-8 (TASK-033/071) | BR-16 / NFR-04 / R-4 |
| 표준 메시지에 입력 값 삽입 | OG-10 (TASK-081) | NFR-07 / PT-7 |
| 한 커밋에 RED + GREEN 또는 Track A + Track B 혼합 | OG-13 (TASK-103) | DT-6 / OPS-3 |
| `print()` 사용 / `bare except` / `from x import *` | OG-2 + 코드 리뷰 | `.cursorrules` forbidden #1·#3·#5 |
| 타입 힌트 누락 | OG-3 (`mypy --strict`) | `.cursorrules` `type_hints.required` |

---

## 변경 로그 (To-Do 보드 자체)

| 날짜 | 변경 | 근거 |
|---|---|---|
| 2026-04-28 | 초기 보드 신설 — US-000~010 + 추적 매트릭스 + README 통합 | `Report/10_To-Do_보드_정립_및_README_통합.md` |
