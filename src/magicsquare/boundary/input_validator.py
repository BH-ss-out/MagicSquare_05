"""Input validation entrypoint (FR-01, Track A).

본 모듈은 PRD §0 입출력 계약을 *Domain 위임 직전*에 강제하는 ``validate``
함수를 제공한다. 본 GREEN 단계 누적:

    - T-U-001 : 행 개수 ≠ 4 → ``ShapeError`` + 표준 메시지 (BR-01 / I1)
    - T-U-020 : 빈칸 개수 ≠ 2 → ``BlankCountError`` + 표준 메시지 (BR-03 / I3)

Public API (계약 — TC-Spec §4.1):
    validate(matrix) -> None
        위반 시 ``BoundaryError`` 하위 5종 중 하나를 byte-equal 표준
        메시지(NFR-07)와 함께 raise. 정상 시 ``None`` 반환.

본 GREEN의 *현재 보호 범위* (의도된 최소 구현 — DT-2 / TC-Spec §부록 A):
    - **AC-01-01**: 행 개수 ≠ 4 → ``ShapeError`` + 표준 메시지 (T-U-001).
    - **AC-01-05**: 빈칸 개수 ≠ 2 → ``BlankCountError`` + 표준 메시지
      (T-U-020). 호출 직전 BR-19 우선순위는 *현재 단계까지의 부분순서*만
      보호된다 (E_SHAPE → E_BLANK_COUNT). 값 범위·중복·우선순위 회귀는
      후속 RED (T-U-010~ / T-U-030~ / T-U-040~042) 가 강제한다.

상수 정책 (D-4 — 본 사이클 결정):
    - ``GRID_SIZE`` 는 *지역 ``Final``* 로 둔다 (기존 정의 유지 — 비-refactor).
      ``entity/constants.py`` 로의 통일은 후속 REFACTOR 사이클에서 처리.
    - ``BLANK_MARKER`` 와 ``EXPECTED_BLANK_COUNT`` 는 ``entity.constants`` 의
      단일 진실 출처를 import (NFR-06 매직 넘버 회피).
    - 표준 메시지는 *지역 ``Final``* 로 둔다 (NFR-07 byte-equal — 본 모듈에서
      직접 raise).

Constraints (.cursorrules + PRD §8.1):
    - Domain 호출 0건 (DT-4 — Track A는 Domain Mock 으로 완주 가능해야 함).
    - 입력 행렬 변경 금지 (BR-16 — 호출 후 byte-equal 보존).
    - 검증 우선순위 ``E_SHAPE → E_VALUE_RANGE → E_BLANK_COUNT → E_DUPLICATE``
      (BR-19 / R-7) 는 *후속 RED* 가 단정 형태로 강제한다.

See Also:
    - ``docs/PRD.md`` §5 FR-01, §6 BR-01·02·03·04·19
    - ``docs/MagicSquare_TestCaseSpecification.md`` §4.1 / §5.1
"""

from __future__ import annotations

from typing import Final

from magicsquare.entity.constants import BLANK_MARKER, EXPECTED_BLANK_COUNT
from magicsquare.entity.exceptions import BlankCountError, ShapeError

GRID_SIZE: Final[int] = 4
_SHAPE_MESSAGE: Final[str] = "Input must be a 4x4 matrix."
_BLANK_COUNT_MESSAGE: Final[str] = "Input must contain exactly 2 blanks (zeros)."


def validate(matrix: list[list[int]]) -> None:
    """4x4 입력 행렬의 입력 계약 검증.

    Args:
        matrix: 검증 대상 4x4 정수 행렬. 셀은 ``0`` (빈칸) 또는 ``1..16``.

    Raises:
        ShapeError: 행 개수가 4가 아닌 경우 (BR-01 / AC-01-01 / I1).
            byte-equal 메시지: ``"Input must be a 4x4 matrix."`` (NFR-07).
        BlankCountError: 빈칸(``BLANK_MARKER``) 개수가 정확히 2가 아닌 경우
            (BR-03 / AC-01-05 / I3).
            byte-equal 메시지: ``"Input must contain exactly 2 blanks (zeros)."``
            (NFR-07).
    """
    if len(matrix) != GRID_SIZE:
        raise ShapeError(_SHAPE_MESSAGE)

    blank_count = sum(1 for row in matrix for cell in row if cell == BLANK_MARKER)
    if blank_count != EXPECTED_BLANK_COUNT:
        raise BlankCountError(_BLANK_COUNT_MESSAGE)
