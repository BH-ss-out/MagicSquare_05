"""T-D-010 — Domain: 같은 행 두 빈칸 → row-major 순서 1-index 좌표 반환.

본 모듈은 ``BlankFinder`` 컴포넌트 (`magicsquare.control.blank_finder`)
의 첫 RED 테스트를 담는다.

추적 (TC-Spec §5.2 / TODO TASK-040 / PRD §12 행 5):
    Test ID         : T-D-010 (사용자 정의 라벨: ``L-RED-01``)
    TODO 매핑       : TASK-040-1
    요건 추적       : FR-02 / AC-02-01 / BR-07 / I1·I3 / NFR-07·BR-20
    Track           : B (Domain) — DT-5에 의해 ``magicsquare.boundary`` import 금지.

현재 RED 사유:
    ``find_blank_coords``가 ``NotImplementedError``를 raise 하므로
    ``assert ...`` 단정 도달 전에 실패. *함수 미구현으로 인한 의도된 RED*다.

다음 단계 (DT-2 — 본 커밋 안에서 GREEN 동시 진행):
    GREEN 구현 — row-major 단일 패스로 ``BLANK_MARKER`` 셀 두 개의
    *1-index* 좌표를 ``((r1, c1), (r2, c2))`` 튜플로 반환.
"""

from __future__ import annotations

import pytest

from magicsquare.control.blank_finder import find_blank_coords


@pytest.mark.domain
def test_find_blank_coords_returns_two_blanks_in_row_major_order() -> None:
    """T-D-010 — 같은 행 두 빈칸: D-Std에서 (2,1)·(2,4) 0 → 1-index 좌표 2개.

    보호 BR        : BR-07 (row-major 스캔 순서)
    보호 AC        : AC-02-01
    보호 Invariant : I1 (4x4 형태) / I3 (빈칸 2개)
    Track          : B (Domain)

    Given:
        D-Std 격자에서 (2,1)·(2,4) 두 셀을 ``BLANK_MARKER`` 로 치환.

    When:
        ``find_blank_coords(board)`` 호출.

    Then:
        - 반환값이 ``((2, 1), (2, 4))`` 와 byte-equal (1-index, c1<c2).
        - 0-index 누설 *금지* (PT-1) — 좌표 모두 ``1..4``.
        - 입력 행렬은 호출 전·후 byte-equal (BR-16).

    Note:
        본 RED는 *단일 동작*만 단정한다 (.cursorrules ``red_phase.rules`` 두 번째).
        결정성·다른 입력 형태는 후속 RED (T-D-011~014) 가 보호.
    """
    board: list[list[int]] = [
        [16, 3, 2, 13],
        [0, 10, 11, 0],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    board_before = [row[:] for row in board]

    coords = find_blank_coords(board)

    assert coords == ((2, 1), (2, 4))
    assert board == board_before
