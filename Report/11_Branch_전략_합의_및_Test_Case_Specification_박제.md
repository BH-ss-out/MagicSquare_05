# 4x4 Magic Square — Branch 전략 합의 및 Test Case Specification 박제 보고서

> 본 문서는 `Report/10` 직후 발생한 **두 사이클** — (a) *Branch 전략 합의 + `red` 작업면 확보*와 (b) *Test Case Specification 박제 + 첫 docs PR 파이프라인 시운전* — 의 결정·산출·검증을 외부화한다.
> 산출물 자체는 **1개 파일** — `docs/MagicSquare_TestCaseSpecification.md` (374줄, 신설) — 이며, 본 보고서는 그 파일에 도달하기까지의 *어떤 결정으로 어떤 워크플로를 어떤 도구로 합의했는가*를 박제한다.
> 본 단계는 **TDD 출발점 직전(Pre-RED 상태)을 *PR 파이프라인 단위로* 결정적으로 고정한 단계**다. 프로덕션 코드 0줄, 테스트 0건, *Pre-RED 게이트 미닫힘* 상태는 결함이 아니라 *본 단계의 의도된 종착점*이다.

---

## 문서 메타데이터

| 항목 | 내용 |
|---|---|
| 문서 ID | `11_Branch_전략_합의_및_Test_Case_Specification_박제` |
| 단계 | Pre-RED 진입 직전 — **PR 파이프라인 정립 + 테스트 카탈로그 4-섹션 환원** (`Report/10` G-Phase의 *논리적 후속*, Pre-RED Closure Log는 아님) |
| 선행 문서 | `Report/10_To-Do_보드_정립_및_README_통합`, `docs/PRD.md`(756줄), `docs/TODO.md`(404줄), `.cursorrules`(265줄) |
| 후행 단계 | (재배정) **`Report/12_Pre_RED_Closure_Log`** — TASK-001(PRD 부록 A 10개 항목 ✅ 박제). 그 직후 첫 RED 한 쌍(TASK-010-1 + TASK-030-1) |
| 산출물 | 1개 파일 — `docs/MagicSquare_TestCaseSpecification.md` 374줄 (신설) + 본 보고서 |
| 산출물 형식 | Markdown |
| 학습 초점 | *PR 파이프라인 시운전의 정직성* / *4-섹션 양식의 외부화* / *외부 카탈로그 ↔ 본 프로젝트 Test ID 무손실 매핑* / *브랜치 꼬임 해소의 외부화* / *Report/10의 번호 약속을 다음 보고서로 *재배정*하는 정직한 회계* |

---

## 0. 본 단계의 위치와 책무

### 0.1 직전 상태 (`Report/10` 종료 직후)

| 항목 | 상태 |
|---|---|
| `docs/PRD.md` (§0/§6/§12 Frozen, §13 유연) | ✅ 합의 (756줄) |
| `Report/01` ~ `Report/10` 10개 보고서 | ✅ 박제 |
| `docs/TODO.md` (404줄, 39행 추적 매트릭스 + 진입 큐 5건) | ✅ 라이브 보드 |
| `README.md` (347줄, 4층 문서 모델 명시) | ✅ 진입점 |
| `.cursorrules` + `pyproject.toml` + `.pre-commit-config.yaml` + `ci.yml` | ✅ OG-1~3 활성, 4~14 슬롯 |
| `src/` + `tests/` 디렉토리 (15개 `__init__.py` + `conftest.py`) | ✅ 스캐폴딩 |
| **Branch 전략** | ❌ 부재 — `main` 단일 브랜치 + 4커밋 직접 푸시. PR 보호 / 게이트 트리거 표면이 *논리적으로만* 정의됨 |
| **PR 워크플로** | ❌ 부재 — 사용자가 PR을 어떻게 만들 것인지 합의되지 않음. `Report/10` §6의 후행 제약은 *문서-only 커밋*만 진술 |
| **Test Case 4-섹션 양식** | ❌ 부재 — PRD §8.1.1·§8.2.1의 Test ID 50건이 *카탈로그 형태*로만 존재. *테스트 환경 / 전제 / 기준 / 절차*로 환원되지 않음 |
| **Pre-RED 게이트 (TASK-001~003)** | ❌ 미닫힘 — `Report/10`이 큐 머리에 박제만 함 |

→ **PR이 발생할 표면이 합의되지 않은 상태**. `Report/10`의 진입 큐 ④(TASK-010-1 + TASK-030-1, DT-1 한 쌍)에 진입하려 해도 *어느 브랜치에서 어떤 커밋 단위로 어느 PR로* 올라갈지 결정되지 않음.

### 0.2 본 단계의 트리거

사용자 위임 6건이 **연속**으로 발생:

| Cycle | 사용자 발화 (요지) | 본 단계가 닫은 부분 |
|---|---|---|
| 1 | *"GitHub 정보와 로컬 정보가 동일한지 확인해줘"* | 4축 정합성 검증 (원격·커밋·트리·README 본문) — 모두 동일 박제 |
| 2 | *"README.md 작업을 하려고 하는데, git branch 전략을 어떻게 하면 좋을지 알려줘"* | GitHub Flow + 명명 규칙 + main 보호 + Squash 정책 합의 |
| 3 | *"우선, red 브랜치 만들어줘"* + *"너가 생각하기에 알맞은 방향으로 진행해. 내가 원하는건 'red'라는 이름의 branch가 생성되는거야"* | `red` 브랜치 생성 (명명 규약 *일회 예외* 박제) |
| 4 | *"테스트 케이스를 작성하고싶어. 프로젝트 문서 구조를 확인하고, 첨부한 파일의 테스트 케이스를 참고해서 [4-섹션] 양식에 맞춰서 작성해줘"* + 외부 카탈로그 슬라이드 첨부 | 외부 카탈로그(TC-MS-A/B/C/D 24건) ↔ 본 프로젝트 Test ID(50+건) 매핑 + 4-섹션 양식 1차 산출 |
| 5 | *"docs/ 디렉토리에 MagicSquare_TestCaseSpecification.md 파일을 생성해줘. 지금 우리의 모든 작업은 red 브랜치에서 진행되어야 하는거야. 꼬임이 있다면 알아서 잘 해결하면서 진행해"* | `red` 브랜치 복귀 + 잉여 브랜치 정리 + 파일 박제 (374줄) |
| 6 | *"git branch -d docs/test-case-specification 진행해줘"* + *"GitHub에 'docs: add formal test case specification' PR을 올리고 싶어. 너는 PR을 올리지는 않아도 되는데, commit과 push를 진행해줘"* | 잉여 브랜치 삭제 + 단일 커밋 박제 + `origin/red` push (PR 생성 직링 출력) |

### 0.3 본 단계가 *해야 하는 것*

- `main` 단일 브랜치 + 직접 푸시 패턴을 **PR 기반 워크플로**로 전환한다 (Branch 전략 명시 + 명명 규약 + 머지 정책).
- `Report/10` 진입 큐 ④의 *DT-1 한 쌍*이 안전하게 진입할 수 있는 **작업 표면(`red` 브랜치)**을 확보한다.
- PRD §8.1.1·§8.2.1의 Test ID 50+건과 외부 카탈로그(첨부 슬라이드의 24건)를 **4-섹션 양식**으로 *손실 없이* 환원한다 — 본 환원이 RED 작성 직전의 *결정적 진입 지반*이 된다.
- 첫 docs-only PR(`docs: add formal test case specification`)을 *시운전*하여, OPS-1(로컬·CI 동일 게이트)·OPS-3(별도 PR)·DT-6(혼합 커밋 금지) 정신이 PR 단위로 결정적으로 작동함을 외부에 노출한다.
- 본 단계가 닫히는 순간, 모든 후속 작업이 *어느 브랜치에서 어떤 커밋 단위로 어느 PR로 올라갈지*를 30초 내 결정할 수 있어야 한다.

### 0.4 본 단계가 *하지 않는 것*

- **TASK-001 (PRD 부록 A 10개 항목 ✅ 박제 = Pre-RED Closure Log)** — `Report/10` §6이 *예약*했던 `Report/11_Pre_RED_Closure_Log` 작업. 본 단계가 *번호를 사용*하므로 후행은 **`Report/12_Pre_RED_Closure_Log`로 재배정** (TD-8 참조).
- **TASK-002 (D-In-B / D-Uns 행렬 확정 — R-2 종결)** — 본 단계는 영향 받는 TC를 *xfail로 마킹*만 함. 행렬 확정은 별도 작업 세션.
- **TASK-003 (`pre-commit run --all-files` 환경 박제)** — 본 단계는 첫 docs PR을 *push까지만* 진행. 로컬 pre-commit 환경 박제는 후속.
- **첫 RED 테스트 작성 (TASK-010-1 / TASK-030-1)** — TDD 원칙. 본 단계는 *카탈로그 박제*이지 *RED 작성*이 아님. `red` 브랜치는 *PR 머지 후*에야 다음 RED 커밋을 받을 수 있음 (TD-9 참조).
- **PR 생성 자체** — 사용자 명시 위임 (*"너는 PR을 올리지는 않아도 되는데"*). 본 단계는 push까지 + GitHub 직링 출력까지.
- **PRD/Report Frozen 영역 변경** — `Report/10` TD-3·TD-7 정신 보존.

---

## 1. 작업 진행 단계 (Cycle-by-Cycle)

본 단계는 **6개 사이클**로 진행되었다. 각 사이클의 입력·결정·산출을 분리해 기록한다.

### CYCLE 1 — 원격 ↔ 로컬 정합성 검증

| 항목 | 내용 |
|---|---|
| 입력 | *"https://github.com/BH-ss-out/MagicSquare_05.git 에 있는 프로젝트 정보와 로컬 정보가 동일한지 확인해줘"* + GitHub README HTML 캡처 첨부 |
| 결정 | 4축 정합성 검증 — ① Remote URL ② 커밋(개수·HEAD SHA) ③ 트리(`git ls-tree -r`) ④ README 본문 절 구조. 4축 모두 일치하면 *완전 동기화*로 박제. |
| 산출 | 4축 표 + `git status`(`up to date with 'origin/main'`, working tree clean) + 4커밋 히스토리 + 12개 트리 항목 모두 일치 박제. |
| 영향 | 후속 모든 작업이 *손실 없는 출발선*에서 시작됨이 외부 검증 가능. 잠재적 동기 위반(stale local / unsigned push 등) 0건 확정. |

### CYCLE 2 — Branch 전략 합의 (GitHub Flow 채택)

| 항목 | 내용 |
|---|---|
| 입력 | *"@README.md 작업을 하려고 하는데, git branch 전략을 어떻게 하면 좋을지 알려줘"* |
| 결정 | (a) **GitHub Flow** 채택 (vs Trunk-based / GitFlow). 근거: 단독 개발자 + `ci.yml`이 이미 PR 트리거 + OPS-1(로컬·CI 동일 게이트)과 정합. (b) **명명 규약 5종**: `task/TASK-XXX-N-<phase>-*`(TDD), `docs/<area>-*`(문서, 본 단계가 첫 사용), `ops/OG-NN-*`(OPS-3), `chore/*`, `fix/*`. (c) **`main` 보호 5규칙**: PR 의무화 / status check 의무화 / branches up-to-date / linear history / no force push. (d) **머지 정책 차등**: `docs|chore|fix` → Squash, `task/TASK-*` → Rebase 또는 일반(phase별 커밋 *보존* — DT-6·OG-13 미래 활성화 정합), `ops/OG-*` → Squash. |
| 산출 | 4표 외부화 (전략 / 명명 / 보호 / 머지) + README 작업의 구체 워크플로 명령 5단계 + 게이트 영향 분석(README 단독 PR은 mypy/ruff/black이 `^src/` 또는 `src tests` 한정이라 미트리거) (응답 본문) — 본 보고서 §3에 *결정 항목*으로 박제. |
| 영향 | 본 단계 이후 *모든 코드/문서 변경이 PR 표면을 거침*. `Report/09` OPS-1·`Report/10` TD-9의 *문서-only 커밋 분리* 정신이 *브랜치 단위*로 강화됨. |

### CYCLE 3 — `red` 브랜치 생성 (명명 규약 *1회 예외* 박제)

| 항목 | 내용 |
|---|---|
| 입력 | *"우선, red 브랜치 만들어줘"* → 명명 규약 정합 4지 선택지 제시 → *"너가 생각하기에 알맞은 방향으로 진행해. 내가 원하는건 'red'라는 이름의 branch가 생성되는거야"* (literal name 요청) |
| 결정 | (a) 사용자 *literal* 요청을 *우선 수용* — `red` 브랜치 생성 (CYCLE 2 권장 명명 `task/TASK-010-1-red-tu001-shape`와 의도적 차이). (b) *예외 박제*: 본 단계 종결 시점에 `git branch -m`으로 정식 명칭 전환 가능함을 응답 본문에 명시. (c) `git switch main → git pull --ff-only → git switch -c red` 3단계로 *최신 main 위 분기*. (d) push는 *이 시점에선 보류* — 작업이 발생한 후에만 `git push -u origin red`. |
| 산출 | `red` 브랜치(local-only, HEAD = `dda5f60`) + 4커밋 main과 동일. |
| 영향 | DT-1 한 쌍(TASK-010-1 + TASK-030-1)이 *작성될 표면*이 확보됨. 단 TASK-010-1과 TASK-030-1은 *서로 다른 커밋*이어야 하므로(DT-6) 본 브랜치 위에서 두 커밋 분리 운영이 후속 단계에 부과됨. |

### CYCLE 4 — Test Case 4-섹션 양식 1차 산출 (외부 카탈로그 ↔ 본 프로젝트 Test ID 매핑)

| 항목 | 내용 |
|---|---|
| 입력 | *"테스트 케이스를 작성하고싶어. 프로젝트 문서 구조를 확인하고, 첨부한 파일의 테스트 케이스를 참고해서 [테스트 환경 / 전제 조건 / 성공·실패 기준 / 특별하게 필요한 절차] 양식에 맞춰서 작성해줘"* + 외부 카탈로그 24건 슬라이드 첨부 |
| 결정 | (a) 외부 카탈로그의 4축(빈칸 찾기 / 마방진 검증 / solution() / 오류) → 본 프로젝트 컴포넌트(BlankFinder / MagicSquareJudge / FillPlanResolver+Assembler / InputValidator+UnsolvableError)로 1:1 매핑. (b) 본 프로젝트의 Test ID 체계(`T-U-*` Track A · `T-D-*` Track B · `TC-N/F/P-*` 통합 · `T-INV-*` 불변 · `P-*` Property)를 *손실 없이 보존* — 외부 ID는 *외부 분류축 보조* 역할. (c) **DT-1 한 쌍**(`T-U-001` + `T-D-001`)을 *완전한 4-섹션 양식*으로, 나머지 ~50건은 *4-섹션 압축 표*로 환원. (d) 공통 환경(§0)은 *모든 TC가 상속*하여 DRY. (e) PRD §11 R-2 미종결 영향 TC 4건(`T-D-031`, `T-D-032`, `TC-N-03`, `TC-F-09`)은 `@pytest.mark.xfail(reason="R-2 ... unsealed")`로 마킹 — 환원 시점에 *xfail 의무가 자동 환기되도록* 박제. |
| 산출 | 응답 본문 — 공통 환경(§0) + DT-1 한 쌍 상세 + 7개 그룹 카탈로그 표 + 진행 권고 + 다음 행동 4지선다. |
| 영향 | 본 환원이 *결정적*이므로, 후속 RED 작성자는 *"어느 BR/AC를 어떤 byte-equal 메시지로 어떤 단정 형태로"* 검증할지를 *카탈로그 1행만 보고* 결정 가능. PRD 756줄·TODO 404줄을 다시 읽지 않아도 됨. |

### CYCLE 5 — `docs/MagicSquare_TestCaseSpecification.md` 박제 + 꼬임 해소

| 항목 | 내용 |
|---|---|
| 입력 | *"docs/ 디렉토리에 MagicSquare_TestCaseSpecification.md 파일을 생성해줘. 지금 우리의 모든 작업은 red 브랜치에서 진행되어야 하는거야. 꼬임이 있다면 알아서 잘 해결하면서 진행해"* |
| 발견된 꼬임 3건 | ① 직전 세션 외부에서 활성 브랜치가 `red`가 아닌 `docs/test-case-specification`(별 브랜치, 같은 SHA `dda5f60`)으로 전환되어 있음. ② DT-6(혼합 커밋 금지) — `red` 브랜치는 본래 *RED 코드용*인데 *docs 산출물*이 함께 들어옴. ③ R-2 미종결로 D-In-B/D-Uns 의존 TC 4건이 RED 단정 시점에 자동 실패 위험. |
| 해결 | ① `git switch red` (작업 손실 0건, 같은 SHA). 잉여 브랜치는 같은 SHA라 무해, 정리는 사용자 지시 대기. ② 브랜치 *수준*이 아닌 *커밋 수준*에서 분리 — `docs(test): ...` 단일 커밋으로 박제하면 DT-6 정합. ③ §2.2 + §5 + §5.5 + §5.6에 xfail 마커 명시 + §6.2 갱신 정책에 *TASK-002 종결 시 일괄 제거* 의무 박제. |
| 산출 | `docs/MagicSquare_TestCaseSpecification.md` (374줄, 8개 절 + 부록 A). 헤더 + 메타데이터 + 문서 위치 + 공통 환경 + Test ID 체계 + DT-1 한 쌍 상세 + 후속 카탈로그(7그룹) + 진행 권고 + 추적 매트릭스 + 변경 로그 + 부록 A. |
| 영향 | 본 파일이 *Test Case 카탈로그의 단일 진실 출처*로 박제. PRD §9를 *대체하지 않으며* 보강하는 4-섹션 환원층. NFR-08 traceability를 *카탈로그 단위*로 강화. |

### CYCLE 6 — 잉여 브랜치 정리 + 단일 커밋 박제 + `origin/red` push

| 항목 | 내용 |
|---|---|
| 입력 | *"git branch -d docs/test-case-specification 진행해줘. 그 다음 GitHub에 올리는 작업에 대해 내가 안내해줄게"* → *"https://github.com/BH-ss-out/MagicSquare_05.git 여기에 'docs: add formal test case specification'이라는 이름으로 PR을 올리고 싶어. 너는 PR을 올리지는 않아도 되는데, 내가 PR을 github에서 바로 올릴 수 있도록 commit과 push를 진행해줘. (마찬가지로 모두 red 브랜치 상태를 유지하고 진행하는거야)"* |
| 결정 | (a) `git branch -d docs/test-case-specification` — 같은 SHA에 있어 -d로 *안전 삭제* 가능. (b) 커밋 메시지 *PR 제목과 정확히 일치* — `docs: add formal test case specification` (subject) + 본문 2단락(파일 설명 + Refs). 단일 커밋 PR이므로 GitHub가 PR 제목을 *자동 채움*. (c) `git push -u origin red` — upstream 설정 포함. (d) push 응답의 GitHub 직링(`https://github.com/BH-ss-out/MagicSquare_05/pull/new/red`)을 사용자에게 노출. (e) PR 생성 자체는 사용자 위임. |
| 산출 | 신규 커밋 `bc8c0ed` (red 브랜치, +373/-0, 1 file changed). 원격 `origin/red` 신설. PR 생성 직링 + Description 템플릿 + 머지 정책 권장(squash) 응답. |
| 영향 | 첫 docs-only PR이 *PR 표면을 거치는 형태*로 진입함. main 보호 규칙(CYCLE 2 §c) 미설정 상태에서도 PR 워크플로의 *형식*은 시운전됨. 사용자가 GitHub UI에서 *수동으로* PR 생성·squash 머지·브랜치 삭제하면 본 사이클이 닫힘. |

---

## 2. 외부화된 결정 (Decision Log)

> 본 절은 본 단계에서 발생한 *합의된 결정*을 TD-1 ~ TD-10으로 외부화한다.

| ID | 결정 | 근거 | 후행 단계 영향 |
|---|---|---|---|
| **TD-1** | **GitHub Flow** 채택 (vs Trunk-based / GitFlow). | CYCLE 2 — 단독 개발자 + `ci.yml` PR 트리거 + OPS-1 정합. GitFlow는 PRD §13.5 OO-1(배포 대상 아님)과 직접 충돌. | 모든 후속 변경은 *토픽 브랜치 → PR → main* 경로를 거친다. main 직접 푸시는 *원칙적으로 금지*. |
| **TD-2** | **브랜치 명명 5종** 채택: `task/TASK-XXX-N-<phase>-*` / `docs/<area>-*` / `ops/OG-NN-*` / `chore/*` / `fix/*`. | CYCLE 2 — TASK ID·OG ID와 1:1 매핑. *브랜치만 봐도* 어느 PRD/TODO 행을 닫는지 보임. | 후속 브랜치는 *반드시* 5종 중 하나. 위반 시 PR 리뷰에서 명명 변경 요청. `red`는 *명시적 1회 예외*(TD-3). |
| **TD-3** | **`red`는 명명 규약 1회 예외**로 사용자 literal 요청 수용. | CYCLE 3 — 사용자 명시 (*"내가 원하는건 'red'라는 이름의 branch가 생성되는거야"*). | 본 브랜치는 *작업 종결 후 정식 명칭으로 rename* 가능 (`git branch -m`). 단, push 후에는 원격 브랜치도 함께 정리 필요. 후속 브랜치는 TD-2를 따른다. |
| **TD-4** | **`main` 보호 5규칙** 권장 (PR 의무 / status check / branches up-to-date / linear history / no force push). | CYCLE 2 — OPS-1·OPS-4 정신을 *GitHub 보호 규칙으로 환원*. | 본 단계는 *권장 박제*만. 사용자가 GitHub Settings → Branches에서 *수동 활성화* 필요. 활성화 전까지 PR 리뷰가 유일한 방어. |
| **TD-5** | **머지 정책 차등**: `docs|chore|fix` → Squash, `task/TASK-*` → Rebase/일반(phase별 커밋 *보존*), `ops/OG-*` → Squash. | CYCLE 2 — DT-6(한 커밋 = 한 phase) 보존을 머지 단계에서도 강제. OG-13 미래 활성화 시 phase 단위 검사가 *깨지지 않게* 함. | 첫 docs PR(`bc8c0ed`)은 *Squash 머지*가 권장. main 히스토리는 *1 PR = 1 커밋*으로 깔끔. task/* 브랜치 도입 시 머지 방식 *변경* 의무. |
| **TD-6** | **Test Case 4-섹션 양식** 채택: 테스트 환경 / 전제 조건 / 성공·실패 기준 / 특별하게 필요한 절차. | CYCLE 4 — 사용자 지정 양식. PRD §9의 *시나리오 표*는 *입력→기대*만 있어 *환경·전제·절차*가 누락. 4-섹션은 그 누락을 보완하면서 *카탈로그 단위 외부 검증*을 가능케 함. | 후속 RED 작성 시 (a) 본 양식의 해당 행을 *복사*해 docstring으로 옮김 + (b) 새 RED 추가 시 본 문서 §5의 해당 그룹에 *한 행 추가*. OG-12 활성화 시 자동 검사 대상. |
| **TD-7** | **외부 카탈로그(첨부 24건) ↔ 본 프로젝트 Test ID(50+건) 매핑**: 4:5 형태로 환원하되 *본 프로젝트 ID를 정본*으로 보존. | CYCLE 4 — `Report/10` TD-6 정신(*손실 없는 환원*) 보존. 외부 ID는 *외부 분류축 보조*. | 후속 외부 카탈로그(예: 슬라이드 갱신, 다른 강의 자료) 도입 시 본 매핑 표만 갱신 — 본 프로젝트 ID/PRD §12 매트릭스 *변경 금지*. |
| **TD-8** | **`Report/11` 번호 *재배정***: `Report/10` §6이 예약했던 `Report/11_Pre_RED_Closure_Log`를 본 보고서가 *대체 사용*하므로, **Pre-RED Closure Log는 `Report/12`로 이관**. | CYCLE 6 — 사용자 위임 우선순위가 *Branch 전략 + Test Case Spec*으로 변동. `.cursorrules` `ai_behavior.honesty` — *"테스트를 직접 실행하지 않은 상태에서 'GREEN을 확인했다'고 단정하지 않는다"*의 *번호 회계 확장*. | 후속 작업자는 `Report/12` 번호에 Pre-RED Closure Log를 두어야 함. `Report/10` 본문 자체는 *수정하지 않음* (Frozen 정신) — 번호 재배정 사실은 *본 보고서 §0 메타·§5*가 박제. |
| **TD-9** | **첫 docs-only PR을 시운전**: `docs: add formal test case specification` 단일 커밋(`bc8c0ed`) → `origin/red` push → PR 생성은 사용자 수동. | CYCLE 6 — DT-6 정신을 *PR 단위*로 확장. PR이 *어떻게 생기고 어떻게 머지되는지*를 *처음 외부에서 검증*. | 후속 모든 PR이 본 PR을 *템플릿*으로 사용 가능 — 단일 커밋·정확한 제목·Description 템플릿(Summary / Refs / CI / Out of scope). 사용자가 PR 머지 후 `red` 브랜치를 *반드시 정리* (로컬 + 원격) — 그렇지 않으면 다음 RED 커밋이 본 PR에 *추가 push*되어 PR 범위가 의도치 않게 확장됨. |
| **TD-10** | **잉여 브랜치 (`docs/test-case-specification`) 즉시 정리**: 같은 SHA에 있어 `git branch -d`로 안전 삭제. | CYCLE 5 — 꼬임 해소 + CYCLE 6 사용자 명시. | 후속 *세션 간 활성 브랜치 변동*에 대비해 매 작업 시작 시 `git branch --show-current` 확인 의무. PRD §11.3 OR-4(환경 차이로 인한 비결정) 정신을 *브랜치 상태*로 확장. |

---

## 3. 산출물 (1개 파일 — 라인 단위)

### 3.1 `docs/MagicSquare_TestCaseSpecification.md` (374줄, 신설)

| 절 | 줄 범위 | 책임 |
|---|---|---|
| 헤더 + 1줄 요약 + 변경 통제 | 1~7 | 본 문서의 자기 진술 |
| **§0 문서 메타데이터** | 11~21 | 7행 표 — 정본 출처·매핑 약어 박제 |
| **§1 본 문서의 위치 (Document Map과의 관계)** | 25~32 | 4층 표 — README/PRD/TODO와의 관계 명시 |
| **§2 공통 테스트 환경 (모든 TC 공통)** | 36~58 | 11행 표 + §2.1 표준 메시지 5종 byte-equal + §2.2 표준 데이터(D-Std / D-In-A / D-In-B·D-Uns 미확정) |
| **§3 Test ID 체계 + 외부 카탈로그 매핑** | 88~96 | 4행 표 — 외부 분류축 ↔ 본 프로젝트 컴포넌트/Test ID 1:1 매핑 |
| **§4 DT-1 한 쌍 — 첫 RED (상세 4-섹션)** | 100~159 | §4.1 `T-U-001` + §4.2 `T-D-001` — 각 6키 메타 + 4섹션(테스트 환경 / 전제 / 기준 / 절차) |
| **§5 후속 카탈로그 (4-섹션 압축 표)** | 163~261 | 7개 그룹 — §5.1 `T-U-*`(27행) / §5.2 `T-D-010~014`(5행) / §5.3 `T-D-020~023`(4행) / §5.4 `T-D-002~009`(8행) / §5.5 `T-D-030~052`(9행) / §5.6 `TC-N/F/P-*`(17행) / §5.7 `T-INV-*` + `P-*`(7행) |
| **§6 진행 권고 (Workflow)** | 265~290 | §6.1 현 단계 직접 작업 4단계 + 권장 커밋 메시지 + §6.2 갱신 정책 4행 |
| **§7 추적 매트릭스 (TC ID → PRD §12 행)** | 294~319 | 20행 표 — NFR-08 역추적 인덱스 |
| **§8 변경 로그** | 323~327 | 본 문서 자체의 자기 추적 |
| **부록 A. 본 문서가 후행 단계에 부과하는 제약** | 331~374 | 5행 표 — RED/GREEN/REFACTOR/PR 리뷰/TASK-002 종결 |

### 3.2 본 보고서 (`Report/11_*.md`)

본 보고서 자체는 *결정 박제용 스냅샷*이며, `docs/MagicSquare_TestCaseSpecification.md`와 *같은 사이클*의 산출이지만 **별도 커밋**(또는 별도 PR — TD-9 정신 보존)으로 분리된다. 본 보고서가 *없으면* 후속 작업자는 첫 docs PR(`bc8c0ed`)의 *결정 근거*(왜 GitHub Flow였는가, 왜 `red` 이름이었는가, 왜 4섹션이었는가)를 추적할 수 없다.

---

## 4. 출처 매핑 자기 검증 (사용자 지정 적용)

> 본 절은 본 사이클이 *6개 사용자 위임*에 대해 *모두 응답했는지* 자기 외부화 검증한다.

| 사용자 위임 | 응답된 본 보고서/산출 | 검증 |
|---|---|---|
| **CYCLE 1 — GitHub ↔ 로컬 정합성** | 본 보고서 §1 CYCLE 1 + 첫 사용자 응답(4축 표) | ✅ — 4축 모두 일치 박제 |
| **CYCLE 2 — Branch 전략** | 본 보고서 §1 CYCLE 2 + TD-1·TD-2·TD-4·TD-5 + 두 번째 사용자 응답(4표 외부화) | ✅ — GitHub Flow + 명명 5종 + main 보호 5규칙 + 머지 차등 |
| **CYCLE 3 — `red` 브랜치 생성** | 본 보고서 §1 CYCLE 3 + TD-3 + 세 번째 사용자 응답(분기 + 검증) | ✅ — `red` 생성, HEAD = main과 동일 (`dda5f60`) |
| **CYCLE 4 — 4-섹션 양식 + 외부 카탈로그 매핑** | 본 보고서 §1 CYCLE 4 + TD-6·TD-7 + 네 번째 사용자 응답(공통 환경 + DT-1 한 쌍 + 7그룹 카탈로그) | ✅ — 50+ TC를 4섹션으로 환원, 외부 24건 1:1 매핑 |
| **CYCLE 5 — `docs/MagicSquare_TestCaseSpecification.md` + 꼬임 해소** | 본 보고서 §1 CYCLE 5 + 산출 §3.1 + 다섯 번째 사용자 응답(꼬임 3건 해결 + 374줄 박제) | ✅ — 1개 파일 신설 + 잉여 브랜치 정리 옵션 안내 |
| **CYCLE 6 — `git branch -d` + commit + push** | 본 보고서 §1 CYCLE 6 + TD-9·TD-10 + 여섯 번째 사용자 응답(잉여 브랜치 삭제 + `bc8c0ed` 커밋 + `origin/red` push + PR 직링) | ✅ — push 응답에서 PR 생성 직링 노출, 사용자 수동 PR 생성 대기 |

### 4.1 *재서술 금지* 원칙 자기 검증

| 위험 | 검증 결과 |
|---|---|
| `docs/MagicSquare_TestCaseSpecification.md`가 PRD §0 입출력 계약을 *재서술*하는가? | ⚠️ 부분 — §2.1 표준 메시지 5종 byte-equal 표가 PRD §0.3·§8.1.2와 동일 내용. 단 본 문서는 *카탈로그 보조*임이 §0 메타에 명시 + PRD가 정본임이 §1에 인용됨. NFR-07 byte-equal 수준에서 *동일 출처를 인용*하는 것은 *재서술이 아닌 보호*. |
| 본 문서가 PRD §8.1.1·§8.2.1 Test ID 카탈로그를 *재서술*하는가? | ❌ — 본 문서의 모든 Test ID(`T-U-*`, `T-D-*` 등)는 PRD §8을 *그대로 인용*. 본 문서가 *4섹션 환원*만 추가. |
| 본 문서가 `docs/TODO.md` TASK-XXX-N의 sub-task를 *재서술*하는가? | ❌ — 본 문서의 *TODO 매핑* 컬럼은 TASK ID *링크*만. 진행 상태·체크포인트·코드 경로는 TODO 정본만 보유. |
| 본 보고서가 `docs/MagicSquare_TestCaseSpecification.md`의 §4 DT-1 한 쌍 상세를 *재서술*하는가? | ❌ — 본 보고서 §3.1은 *줄 범위 인덱스*만. 4섹션 내용은 산출 파일이 정본. |

---

## 5. 본 단계의 *정직한* 미충족 보고

> `.cursorrules` `ai_behavior.honesty` 직접 운영. 본 단계가 *완전히 닫지 않은* 부분을 회피 없이 보고한다.

| 미충족 항목 | 사유 | 처리 |
|---|---|---|
| **TASK-001 (PRD 부록 A 10개 항목 ✅ 박제)** | `Report/10` §6이 본 번호(`Report/11`)에 예약했던 작업이지만, 사용자 위임 6건의 *우선순위가 변동*함. 본 단계가 번호를 *대체 사용*. | TD-8에 의해 **`Report/12_Pre_RED_Closure_Log`로 재배정**. `Report/10` §6 본문은 *수정하지 않음* (Frozen 정신). 후속 작업자는 본 보고서 메타·§5의 재배정 박제를 보고 `Report/12`로 진행. |
| **TASK-002 (D-In-B / D-Uns 4x4 행렬 확정 — R-2 종결)** | 수기 검산은 *별도 작업 세션*이 필요. 본 단계는 *xfail 마커 박제*만. | `docs/MagicSquare_TestCaseSpecification.md` §2.2·§5.5·§5.6의 xfail 마커가 *TASK-002 종결 시 일괄 제거* 의무를 자동 환기 (§6.2 갱신 정책 박제). 종결 시 PRD §9.3.3·§9.3.4 + 본 문서 + `docs/TODO.md` TASK-061·070 상태가 *동일 PR*에서 갱신되어야 함. |
| **TASK-003 (`pre-commit run --all-files` 환경 박제)** | 본 사이클은 *문서-only*. push 전후 pre-commit 훅이 실제로 작동했는지 *직접 실행 검증*하지 않음. | 본 사이클의 commit이 *훅 차단 없이* 통과한 것으로 보아 (a) 훅이 설치되지 않았거나 (b) 본 .md 파일이 모든 훅을 통과한 것. *어느 쪽인지 외부 검증되지 않음*. 후속 단계 (`Report/12` 또는 `Report/13`)에서 `pre-commit install` + `pre-commit run --all-files`을 *명시적으로 실행*하고 결과를 박제. |
| **`main` 보호 규칙 활성화 (TD-4)** | 본 단계는 *권장 박제*만. GitHub UI 작업은 사용자 권한. | 사용자가 Settings → Branches에서 5규칙 활성화. 활성화 전까지는 *직접 main 푸시가 기술적으로 가능* — PR 리뷰가 유일 방어. 활성화 시점을 별도 보고서(예: `Report/13_main_보호_규칙_활성화`)로 박제 권장. |
| **첫 docs PR 자체** | 사용자 명시 위임 (*"너는 PR을 올리지는 않아도 되는데"*). 본 단계는 push까지 + 직링 출력까지. | 사용자가 GitHub UI에서 수동 생성. PR 머지 후 (a) 로컬 `git switch main && git pull && git branch -d red` (b) 원격 `red` 자동 삭제(GitHub 옵션) — 둘 다 사용자 책임. 누락 시 다음 RED 커밋이 본 PR에 *추가 push*되어 PR 범위 *오염*. |
| **`docs/test-case-specification` 잉여 브랜치 발생 원인 (CYCLE 5 꼬임 #1)** | 직전 세션 *외부*에서 활성 브랜치가 변동. 본 단계 작업 외부에서 발생한 사건이라 *원인 추적 불가*. | TD-10에 의해 매 작업 시작 시 `git branch --show-current` 확인 의무 박제. 추가 방어로 OG-13(혼합 커밋 검사) 활성화 시 브랜치 명명 규약(TD-2) 위반도 함께 검사할 수 있음 — 후속 PR(TASK-103)로 이관. |
| **본 보고서 자체의 회귀 보호** | 본 보고서가 *지워지면* 본 사이클의 결정 근거(특히 TD-8 번호 재배정)가 사라져 `Report/10` ↔ `Report/12` 사이의 *번호 공백*이 설명되지 않음. | OG-12(Traceability 무결성 스크립트) 활성화 시 *Report 디렉토리 무결성 검사*가 본 보고서를 보호. 그 전까지 PR 리뷰가 유일한 방어. |

---

## 6. 본 단계가 후행 단계에 부과하는 제약

| 후행 단계 | 본 단계가 부과한 제약 |
|---|---|
| **첫 docs PR 머지 후 로컬 정리** | (a) `git switch main && git pull --ff-only && git branch -d red` 의무 — 그렇지 않으면 다음 RED 커밋이 본 PR에 추가 push되어 *PR 범위 오염*. (b) 원격 `origin/red`도 GitHub UI에서 삭제(또는 "Automatically delete head branches" 옵션 활성화). |
| **`Report/12_Pre_RED_Closure_Log` (TASK-001 재배정)** | (a) `Report/12` 번호로 신설 — 본 보고서 TD-8이 강제. (b) PRD 부록 A 10개 항목 모두 ✅로 박제. (c) `docs/TODO.md` 추적 매트릭스에서 TASK-001 상태 *🟦 → ✅* 갱신 + 변경 로그 1행. (d) `Report/10` §6 본문은 *수정하지 않음* (Frozen 정신) — 번호 재배정 사실은 *본 보고서 §5*가 박제하는 것으로 충분. |
| **TASK-010-1 + TASK-030-1 (DT-1 한 쌍, 첫 RED)** | (a) **별도 브랜치**(`task/TASK-010-1-red-tu001-shape` + `task/TASK-030-1-red-td001-magic`)에서 진행 — TD-2 명명 규약 정합. (b) `red` 브랜치 *재사용 금지* — 첫 docs PR이 머지될 때 함께 정리됨. (c) 두 RED는 *같은 작업 세션*(DT-1) + *서로 다른 커밋*(DT-6) + *서로 다른 브랜치/PR* 권장 (DT-6 정신의 머지 단계 확장 — TD-5). (d) 각 RED 작성 시 `docs/MagicSquare_TestCaseSpecification.md` §4의 4섹션을 *복사*해 docstring으로 옮김. |
| **새 RED 추가 시** | `docs/MagicSquare_TestCaseSpecification.md` §5 해당 그룹 표에 *한 행 추가* + 본 문서 §6.2 갱신 정책 정합. NFR-08 traceability + OG-12(미래) 자동 검사 정합. 누락 시 PR 리뷰에서 차단. |
| **TASK-002 종결 시 (R-2 종결)** | (a) PRD §9.3.3·§9.3.4 행렬 본문 채움. (b) `docs/MagicSquare_TestCaseSpecification.md` §2.2·§5.5·§5.6의 xfail 마커 *일괄 제거* (동일 PR). (c) `docs/TODO.md` TASK-061·070 ⏸ BLOCKED → 🟦 TODO 동시 전이. (d) 본 보고서 §5의 R-2 의존 미충족 항목이 *닫힘*. |
| **회귀** | 본 단계의 1개 산출(`docs/MagicSquare_TestCaseSpecification.md`) + 본 보고서는 *그 자체로* 회귀 보호 대상. 누군가 본 산출의 byte-equal 메시지 5종 표(§2.1)를 *완화 변경*하면 NFR-07 + OPS-2가 *즉시 깨진다*. 이 회귀는 OG-10(메시지 byte-equal 회귀) 활성화 전까지 PR 리뷰가 유일한 방어. |
| **OPS-3 정신** | 본 보고서 + `docs/MagicSquare_TestCaseSpecification.md`는 *동일 사이클*의 산출이지만 *별 PR로 분리* 권장 — 첫 docs PR(`bc8c0ed`)은 *Test Case Spec 단독*으로 머지하고, 본 보고서는 *후속 PR* (예: `docs(report): externalize Report/11 — branch strategy + spec cycle`)로 분리. 그렇지 않으면 첫 docs PR의 *제목·범위가 일치하지 않게 됨*. |

---

## 7. 본 단계 직후 즉시 실행 가능 명령 (체크리스트)

> 본 절은 다음 작업자(또는 동일 학습자가 모자만 바꾼 상태)가 *바로 실행 가능한 명령*을 박제한다.

```powershell
# Windows PowerShell — 본 워크스페이스 루트에서

# === 즉시 (사용자 GitHub UI 작업) ===
# 1. 다음 직링으로 PR 생성 (사용자 수동)
#    https://github.com/BH-ss-out/MagicSquare_05/pull/new/red
#    Title: docs: add formal test case specification  (자동 채움)
#    Description: 본 보고서 답변에 포함된 템플릿 사용
#    Merge: Squash and merge → "Delete branch" 클릭

# === PR 머지 후 로컬 정리 ===
git switch main
git pull --ff-only origin main           # bc8c0ed가 main에 squash 머지된 형태로 들어옴
git branch -d red                        # 로컬 red 정리
git branch -vv                           # main만 남았는지 확인

# === Report/11 단독 PR (본 보고서 분리) ===
git switch -c docs/report-11             # TD-2 명명 정합
git add Report/11_Branch_전략_합의_및_Test_Case_Specification_박제.md
git commit -m "docs(report): externalize Report/11 — branch strategy + spec cycle" `
           -m "Decision log TD-1~10 for the cycle that produced docs/MagicSquare_TestCaseSpecification.md (PR #X) and reassigns Report/11 -> Report/12 for the Pre-RED Closure Log."
git push -u origin docs/report-11
# → GitHub에서 PR 생성 → squash merge → branch -d

# === Report/12 (TASK-001 재배정 — 후속 작업) ===
git switch main && git pull --ff-only
git switch -c docs/report-12-pre-red-closure
# Report/12_Pre_RED_Closure_Log.md 신설 (PRD 부록 A 10개 항목 ✅ 박제)
# docs/TODO.md TASK-001 상태 🟦 → ✅ + 변경 로그 1행
git commit -m "docs: close Pre-RED Gate (PRD appendix A — 10 items checklist)"
git push -u origin docs/report-12-pre-red-closure
```

이 직후, **TASK-002 (R-2 종결)** 또는 **TASK-010-1 + TASK-030-1 (DT-1 한 쌍, 첫 RED)** 중 사용자 우선순위에 따라 진행. *어느 쪽이든* TD-2 명명 규약을 따른 별도 브랜치 + 별도 PR.

---

## 8. 본 단계의 마무리 진술

> **"본 단계는 `Report/10`이 *2개 파일로 닫은 작업 보드*를, *PR 파이프라인 단위*로 환원한 첫 사이클이다.**
> **1개 파일이 산출되었으며 — `docs/MagicSquare_TestCaseSpecification.md`(374줄, 4-섹션 양식 카탈로그) — 본 보고서가 그 파일에 도달하기까지의 *결정 근거*(TD-1 ~ TD-10)를 박제한다.**
> **PRD §8.1.1·§8.2.1의 Test ID 50+건과 외부 카탈로그(슬라이드 24건)는 *4-섹션 양식*으로 *손실 없이* 환원되었으며, *DT-1 한 쌍*(`T-U-001` + `T-D-001`)은 다음 RED 커밋의 4섹션을 *결정적*으로 고정했다.**
> **`Report/10`이 본 번호에 예약했던 *Pre-RED Closure Log*는 사용자 위임 우선순위 변동으로 `Report/12`로 재배정되었으며, 그 사실은 본 보고서 §0 메타·TD-8·§5에 *외부에서 검증 가능한 형태*로 박제된다.**
> **다음 커밋(첫 docs PR 머지 + `Report/11` 단독 PR + `Report/12` 신설)은 *반드시* TD-2 명명 규약을 따른 별도 브랜치에서 진행되며, 그 직후 TASK-002 또는 첫 RED 한 쌍이 *같은 작업 세션, 다른 커밋, 다른 브랜치, 다른 PR*로 진입한다."**

본 단계가 닫히는 순간, *PR이 어떻게 생기고 어떻게 머지되는지*에 대한 잠재 위험은 사라졌다. 다음 작업자(또는 동일 학습자가 모자만 바꾼 상태)는 GitHub Flow + TD-2 명명 + TD-5 머지 정책을 *결정적으로* 적용해, 모든 후속 변경을 *PR 표면 단위*로 진행할 수 있다.
