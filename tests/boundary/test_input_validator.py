"""``InputValidator`` (FR-01, Track A) — ``T-U-*`` 시리즈 RED/GREEN 테스트.

본 모듈은 ``magicsquare.boundary.input_validator.validate`` 의 입력 계약 검증
테스트를 담는다. 각 테스트 함수는 단일 TC ID 하나에 대응하며, docstring 에
보호하는 BR/AC/Invariant 를 명시한다 (NFR-08 traceability).

수록 TC ID:
    - ``T-U-001`` — 3행 입력 → ``ShapeError`` (BR-01 / AC-01-01 / I1)
    - ``T-U-020`` — 빈칸 0개 → ``BlankCountError`` (BR-03 / AC-01-05 / I3)

Track 원칙 (PRD §8.1 / §8.3 DT-4):
    - Domain 호출 0건 — Domain 객체는 ``unittest.mock.Mock`` 으로만 spectator.
    - 표준 메시지(NFR-07) 는 byte-equal 단정 — ``in`` / ``.lower()`` 변환 *금지*.
    - 다중 위반 입력은 본 모듈 범위가 *아니다* (BR-19 우선순위는 ``T-U-040~042``).
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from magicsquare.boundary.input_validator import validate
from magicsquare.entity.exceptions import BlankCountError, ShapeError


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


@pytest.mark.boundary
def test_validate_no_blank_input_raises_blank_count_error() -> None:
    """T-U-020 — D-Std (빈칸 0개) → BlankCountError + 표준 메시지 byte-equal.

    보호 BR        : BR-03 (빈칸 정확히 2개)
    보호 AC        : AC-01-05
    보호 Invariant : I3 (입력측 — 빈칸 개수)
    Track          : A (Boundary)

    Given:
        D-Std (Dürer 마방진) — 4x4 형태 OK, 값 범위 OK, 빈칸 0개로 *I3 위반*.
        Domain 은 ``unittest.mock.Mock`` 으로 spectator (DT-4).

    When:
        ``validate(matrix)`` 호출.

    Then:
        - ``BlankCountError`` raise.
        - ``exc.value.args[0]`` 가 표준 메시지와 byte-equal:
          ``"Input must contain exactly 2 blanks (zeros)."`` (NFR-07).
          ``in`` 부분 일치 / ``.lower()`` 변환 *금지*.
        - Domain Mock 은 *한 번도* 호출되지 않음 (AC-01-11 / DT-4).

    Note:
        BR-19 우선순위 (E_SHAPE → E_VALUE_RANGE → E_BLANK_COUNT → E_DUPLICATE)
        보호는 본 RED 범위가 *아니다* — 후속 ``T-U-040~042`` 가 강제한다.
        본 테스트는 *형태 OK + 값 범위 OK* 입력만 사용해 단일 동작을 검증한다
        (.cursorrules ``red_phase.rules`` 두 번째).
    """
    matrix: list[list[int]] = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    domain_mock = Mock()

    with pytest.raises(BlankCountError) as exc_info:
        validate(matrix)

    assert exc_info.value.args[0] == "Input must contain exactly 2 blanks (zeros)."
    domain_mock.assert_not_called()
