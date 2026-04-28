"""Domain constants — single source of truth for grid dimensions/markers (NFR-06).

본 모듈은 PRD §0 입출력 계약과 §6 BR가 *동일 정수 리터럴*을 여러 곳에서 사용하지
않도록 강제하기 위한 *도메인 상수의 단일 진실 출처*다 (TASK-020 / NFR-06 /
``.cursorrules`` ``forbidden`` #2).

Public Constants:
    GRID_SIZE              : 격자 한 변의 길이 (= 4). I1 형태 불변의 단일 출처.
    BLANK_MARKER           : 빈칸을 나타내는 셀 값 (= 0). PRD §0.1.
    EXPECTED_BLANK_COUNT   : 정상 입력의 빈칸 개수 (= 2). I3 / BR-03.
    MAGIC_CONSTANT         : 마방진 상수 (= 34 = n·(n²+1)/2, n=GRID_SIZE).
                             I4 합 균질 불변의 단일 출처 (BR-06).

상수 정책 (D-4 — REFACTOR 사이클로 SSOT 일원화 완료):
    - 모든 상수는 ``Final[int]`` — 재바인딩·shadowing 차단(타입 시스템 강제).
    - ``GRID_SIZE`` 와 ``MAGIC_CONSTANT`` 는 본 모듈이 *유일한 정의 출처*다.
      ``boundary/input_validator.py`` 와 ``control/magic_square_judge.py`` 는
      본 모듈에서 import 하여 사용한다 (REFACTOR 단계로 지역 ``Final`` 재정의를
      제거함).
    - ``MAGIC_CONSTANT`` 는 ``GRID_SIZE`` 로부터 *식으로 도출* 한다 — 매직 리터럴
      ``34`` 의 직접 기입을 차단 (.cursorrules ``forbidden`` #2).

Constraints (.cursorrules + PRD §8.2):
    - 본 모듈은 *어떤 외부 계층에도 의존하지 않는다* (Entity = 가장 안쪽 계층).
    - 부수 효과 0건 (BR-16 / NFR-04).

See Also:
    - ``docs/PRD.md`` §0.1 입력 계약, §6 BR-01/03/06
    - ``docs/MagicSquare_TestCaseSpecification.md`` §2.1 표준 메시지
    - ``docs/TODO.md`` TASK-020 (도메인 상수 모듈 신설)
"""

from __future__ import annotations

from typing import Final

GRID_SIZE: Final[int] = 4
BLANK_MARKER: Final[int] = 0
EXPECTED_BLANK_COUNT: Final[int] = 2
MAGIC_CONSTANT: Final[int] = GRID_SIZE * (GRID_SIZE * GRID_SIZE + 1) // 2
