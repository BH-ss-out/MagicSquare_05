"""T-D-001 — Domain 첫 RED: 표준 마방진(D-Std) → True.

본 모듈은 ``MagicSquareJudge`` 컴포넌트의 첫 RED 테스트를 담는다.

추적 (TC-Spec §4.2 / PRD §12 행 6):
    Test ID         : T-D-001
    TODO 매핑       : TASK-030-1
    요건 추적       : FR-04 / AC-04-01 / BR-06 / I4 / NFR-07·BR-20
    Track           : B (Domain) — DT-5에 의해 ``magicsquare.boundary`` import 금지.

현재 RED 사유:
    ``is_magic_square``가 ``NotImplementedError``를 raise하므로
    ``assert ... is True`` 단정이 ``AssertionError``로 도달하지 못하고 실패.
    이는 *함수 미구현으로 인한 의도된 RED*다 (PRD §8.3 DT-3).

다음 단계 (DT-2):
    GREEN 구현 — ``is_magic_square``가 D-Std에 대해 ``True`` 반환.
    같은 PR 안에서 진행하지 않는다 (DT-6).
"""

from __future__ import annotations

import pytest

from magicsquare.control.magic_square_judge import is_magic_square

D_STD: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


@pytest.mark.domain
def test_is_magic_square_returns_true_for_standard_durer_square() -> None:
    """T-D-001 — D-Std → True.

    보호 BR        : BR-06 (마방진 상수 = 34)
    보호 AC        : AC-04-01
    보호 Invariant : I4 (모든 행/열/대각 합 = 34)
    Track          : B (Domain)

    Given:
        D-Std (Dürer 마방진) — 빈칸 0개, 모든 행/열/주대각/부대각의 합 = 34.

    When:
        ``is_magic_square(D_STD)`` 호출.

    Then:
        반환값이 ``True`` (정확히 ``is True`` — ``truthy`` 대용 금지,
        ``==`` 비교는 PEP8 E712 위반).
    """
    assert is_magic_square(D_STD) is True
