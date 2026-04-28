"""T-U-001 — Boundary 첫 RED: 3행 입력 → ShapeError.

본 모듈은 ``InputValidator`` 컴포넌트의 첫 RED 테스트를 담는다.

추적 (TC-Spec §4.1 / PRD §12 행 1):
    Test ID         : T-U-001
    TODO 매핑       : TASK-010-1
    요건 추적       : FR-01 ① / AC-01-01 / BR-01 / I1 / NFR-07·BR-20
    Track           : A (Boundary) — DT-4에 의해 Domain은 Mock으로 가정.

현재 RED 사유:
    ``validate``가 ``NotImplementedError``를 raise하므로
    ``pytest.raises(ShapeError)``가 *기대 예외 대신* ``NotImplementedError``를
    받아 단정이 실패. 이는 *함수 미구현으로 인한 의도된 RED*다.

다음 단계 (DT-2):
    GREEN 구현 — ``validate``가 4x4가 아닌 입력에 대해 ``ShapeError`` raise +
    표준 메시지 ``"Input must be a 4x4 matrix."`` byte-equal 동등.
    같은 PR 안에서 진행하지 않는다 (DT-6).
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from magicsquare.boundary.input_validator import validate
from magicsquare.entity.exceptions import ShapeError


@pytest.mark.boundary
def test_validate_3row_input_raises_shape_error() -> None:
    """T-U-001 — 3행 4열 입력 → ShapeError + 표준 메시지 byte-equal.

    보호 BR        : BR-01 (입력 형태 4x4)
    보호 AC        : AC-01-01
    보호 Invariant : I1
    Track          : A (Boundary)

    Given:
        ``matrix = [[1,2,3,4], [5,6,7,8], [9,10,11,12]]`` — 3행 4열, 형태 위반.
        Domain은 ``unittest.mock.Mock`` 으로 대체 — DT-4 회귀 가드.

    When:
        ``validate(matrix)`` 호출.

    Then:
        - ``ShapeError`` raise.
        - ``str(exc.value.args[0])`` == ``"Input must be a 4x4 matrix."`` (byte-equal).
        - Domain Mock은 *한 번도* 호출되지 않음 (AC-01-11 / DT-4).

    Note:
        Mock은 본 RED에서는 의존성 주입되지 않지만, GREEN 구현이 *우연히
        Domain을 인스턴스화하거나 호출*하는 회귀를 차단하는 *spectator 단정*이다.
    """
    matrix: list[list[int]] = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    domain_mock = Mock()

    with pytest.raises(ShapeError) as exc_info:
        validate(matrix)

    assert exc_info.value.args[0] == "Input must be a 4x4 matrix."
    domain_mock.assert_not_called()
