"""Input validation entrypoint (FR-01, Track A).

본 모듈은 PRD §0 입출력 계약을 *Domain 위임 직전*에 강제하는 ``validate``
함수를 제공한다. T-U-001 GREEN — 행 개수가 4가 아닌 입력에 대해
``ShapeError`` 를 표준 메시지(byte-equal)와 함께 raise 하는 *최소 구현*.

Public API (계약 — TC-Spec §4.1):
    validate(matrix) -> None
        위반 시 ``BoundaryError`` 하위 5종 중 하나를 byte-equal 표준
        메시지(NFR-07)와 함께 raise. 정상 시 ``None`` 반환.

본 GREEN의 *현재 보호 범위* (의도된 최소 구현 — DT-2 / TC-Spec §부록 A):
    - **AC-01-01**: 행 개수 ≠ 4 → ``ShapeError`` + 표준 메시지 (T-U-001).
    - 그 외 형태/값/빈칸/중복/우선순위 검증은 본 GREEN 범위가 *아니다*.
      후속 RED 사이클 (T-U-002 ~ T-U-042) 에서 단계적으로 추가된다.

상수 정책 (D-4 — 본 사이클 결정):
    ``GRID_SIZE`` 와 표준 메시지는 *지역 ``Final``* 로 둔다.
    ``entity/constants.py`` 로의 추출은 후속 RED 사이클 (TASK-020-1) 또는
    본 사이클 REFACTOR 단계에서 결정한다 (NFR-07 byte-equal 보존 +
    NFR-06 매직 넘버 회피).

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

from magicsquare.entity.exceptions import ShapeError

GRID_SIZE: Final[int] = 4
_SHAPE_MESSAGE: Final[str] = "Input must be a 4x4 matrix."


def validate(matrix: list[list[int]]) -> None:
    """4x4 입력 행렬의 입력 계약 검증.

    Args:
        matrix: 검증 대상 4x4 정수 행렬. 셀은 ``0`` (빈칸) 또는 ``1..16``.

    Raises:
        ShapeError: 행 개수가 4가 아닌 경우 (BR-01 / AC-01-01 / I1).
            byte-equal 메시지: ``"Input must be a 4x4 matrix."`` (NFR-07).
    """
    if len(matrix) != GRID_SIZE:
        raise ShapeError(_SHAPE_MESSAGE)
