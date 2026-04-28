"""Domain constants — single source of truth for grid dimensions/markers (NFR-06).

본 모듈은 PRD §0 입출력 계약과 §6 BR가 *동일 정수 리터럴*을 여러 곳에서 사용하지
않도록 강제하기 위한 *도메인 상수의 단일 진실 출처*다 (TASK-020 / NFR-06 /
``.cursorrules`` ``forbidden`` #2).

Public Constants (현 GREEN 사이클 한정 — 후속 RED가 요구할 때 추가):
    GRID_SIZE              : 격자 한 변의 길이 (= 4). I1 형태 불변의 단일 출처.
    BLANK_MARKER           : 빈칸을 나타내는 셀 값 (= 0). PRD §0.1.
    EXPECTED_BLANK_COUNT   : 정상 입력의 빈칸 개수 (= 2). I3 / BR-03.

상수 정책 (D-4):
    - 모든 상수는 ``Final[int]`` — 재바인딩·shadowing 차단(타입 시스템 강제).
    - ``GRID_SIZE`` 는 본 모듈을 단일 진실 출처로 둔다. *기존 모듈
      (`boundary/input_validator.py`, `control/magic_square_judge.py`) 의 지역
      ``Final`` 정의는* 본 GREEN 사이클의 *비-refactor 원칙*에 따라 유지하며,
      후속 REFACTOR 사이클에서 본 모듈 import로 통일한다.

Constraints (.cursorrules + PRD §8.2):
    - 본 모듈은 *어떤 외부 계층에도 의존하지 않는다* (Entity = 가장 안쪽 계층).
    - 부수 효과 0건 (BR-16 / NFR-04).
    - 본 GREEN 한정으로 *후속 RED가 요구하지 않는 상수*는 정의하지 않는다
      (TDD 원칙 — 미요구 자산 금지).

See Also:
    - ``docs/PRD.md`` §0.1 입력 계약, §6 BR-01/03
    - ``docs/MagicSquare_TestCaseSpecification.md`` §2.1 표준 메시지
    - ``docs/TODO.md`` TASK-020 (도메인 상수 모듈 신설)
"""

from __future__ import annotations

from typing import Final

GRID_SIZE: Final[int] = 4
BLANK_MARKER: Final[int] = 0
EXPECTED_BLANK_COUNT: Final[int] = 2
