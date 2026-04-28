"""Blank coordinate detector (FR-02, Track B).

본 모듈은 *사전조건이 충족된* 4x4 격자에서 빈칸(``BLANK_MARKER``) 두 개의
좌표를 *row-major 순서* (BR-07) 로 반환하는 ``find_blank_coords`` 함수를
제공한다. T-D-010 GREEN — 같은 행 두 빈칸 입력에 대해 1-index 튜플을
row-major 순서로 반환하는 *최소 구현*.

Public API (계약 — TC-Spec §5.2):
    find_blank_coords(board) -> ((r1, c1), (r2, c2))
        ``BLANK_MARKER`` 셀 두 개의 *1-index* 좌표를 row-major 순서로 반환한다.
        호출자는 빈칸 개수가 정확히 2임을 *Boundary 단계에서* 검증해야 한다 (R-9).

본 GREEN의 *현재 보호 범위* (의도된 최소 구현 — DT-2 / TC-Spec §부록 A):
    - **AC-02-01**: 같은 행 두 빈칸 → ``((r1, c1), (r2, c2))`` 1-index (T-D-010).
    - 다른 입력 형태 (다른 행 / 인접 / 0-index 누설) 는 본 GREEN 범위가
      *아니다*. 후속 RED (T-D-011~014) 에서 단계적으로 추가된다.

상수 정책 (D-4):
    ``GRID_SIZE`` 와 ``BLANK_MARKER`` 는 ``entity.constants`` 의 단일 진실
    출처를 import 한다 (NFR-06 매직 넘버 회피).

Constraints (.cursorrules + PRD §8.2):
    - Boundary 호출 금지 (DT-5 / BR-17 / NFR-09).
    - 입력 행렬 변경 금지 (BR-16 — T-D-008·T-INV-BR16 회귀 보호).
    - 결과는 *1-index* — 0-index 누설 금지 (PT-1).

See Also:
    - ``docs/PRD.md`` §5 FR-02, §6 BR-07
    - ``docs/MagicSquare_TestCaseSpecification.md`` §5.2
    - ``docs/TODO.md`` TASK-040
"""

from __future__ import annotations

from typing import Final

from magicsquare.entity.constants import (
    BLANK_MARKER,
    EXPECTED_BLANK_COUNT,
    GRID_SIZE,
)

_INDEX_OFFSET: Final[int] = 1


def find_blank_coords(
    board: list[list[int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """4x4 격자에서 빈칸 두 개의 좌표를 row-major 순서로 반환.

    Args:
        board: 사전조건 충족 4x4 정수 격자. ``BLANK_MARKER`` 셀이 *정확히 2개*
            존재한다고 가정 (Boundary 검증 책임 — R-9 / I3).

    Returns:
        ``((r1, c1), (r2, c2))`` — 1-index 좌표. row-major 순서로 먼저 발견된
        빈칸이 ``(r1, c1)``.
    """
    coords: list[tuple[int, int]] = [
        (r + _INDEX_OFFSET, c + _INDEX_OFFSET)
        for r in range(GRID_SIZE)
        for c in range(GRID_SIZE)
        if board[r][c] == BLANK_MARKER
    ]
    first, second = coords[:EXPECTED_BLANK_COUNT]
    return (first, second)
