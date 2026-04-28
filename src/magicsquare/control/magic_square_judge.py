"""Magic square judgement (FR-04, Track B).

본 모듈은 채워진 4x4 격자가 *마방진 정의(I4)* 를 만족하는지 판정하는
``is_magic_square`` 함수를 제공한다. T-D-001 GREEN — 표준 Dürer 마방진
(D-Std) 입력에 대해 ``True`` 를 반환하는 *최소 구현*.

Public API (계약 — TC-Spec §4.2):
    is_magic_square(board) -> bool
        모든 행/열/두 대각의 합이 ``MAGIC_CONSTANT`` (= 34) 와 일치하면
        ``True`` 반환. 그렇지 않으면 ``False``.

상수 정책 (D-4 — REFACTOR 사이클로 SSOT 일원화 완료):
    ``GRID_SIZE`` 와 ``MAGIC_CONSTANT`` 는 ``entity.constants`` 의 단일 진실
    출처를 import 한다 (NFR-06 매직 넘버 금지 + ruff PLR2004 회피).

Constraints (.cursorrules + PRD §8.2):
    - Boundary 호출 금지 (DT-5 / BR-17 / NFR-09).
    - 입력 행렬 변경 금지 (BR-16 — T-D-008 회귀 보호).
    - 결정성 100회 동일 결과 (BR-15 — T-D-009 회귀 보호).

See Also:
    - ``docs/PRD.md`` §5 FR-04, §6 BR-05·06
    - ``docs/MagicSquare_TestCaseSpecification.md`` §4.2 / §5.4
"""

from __future__ import annotations

from magicsquare.entity.constants import GRID_SIZE, MAGIC_CONSTANT


def is_magic_square(board: list[list[int]]) -> bool:
    """4x4 격자의 마방진 여부 판정.

    Args:
        board: 판정 대상 4x4 정수 격자. 본 함수의 사전조건은
            *모든 셀이 채워져 있고 ``{1..16}`` 다중집합과 일치*함이며,
            사전조건 보장은 호출자(Boundary)의 책임이다 (R-9).

    Returns:
        모든 행/열/두 대각의 합이 ``34`` 와 일치하면 ``True``, 아니면 ``False``.
    """
    for row in board:
        if sum(row) != MAGIC_CONSTANT:
            return False

    for c in range(GRID_SIZE):
        if sum(board[r][c] for r in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False

    main_diag_sum = sum(board[i][i] for i in range(GRID_SIZE))
    if main_diag_sum != MAGIC_CONSTANT:
        return False

    anti_diag_sum = sum(board[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE))
    return anti_diag_sum == MAGIC_CONSTANT
