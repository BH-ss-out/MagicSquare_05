"""Input validation entrypoint (FR-01, Track A).

본 모듈은 PRD §0 입출력 계약을 *Domain 위임 직전*에 강제하는 ``validate``
함수의 *공개 시그니처 stub*만 둔다. 비즈니스 로직 0줄 — 본 모듈의 존재
이유는 *T-U-001 RED 테스트의 컬렉션 실패 회피*에 한정된다 (TC-Spec §6.1 ①).

Public API (계약 합의 — TC-Spec §4.1 전제조건 1):
    validate(matrix) -> None
        위반 시 ``BoundaryError`` 하위 5종 중 하나를 byte-equal 표준
        메시지(NFR-07)와 함께 raise. 정상 시 ``None`` 반환.

Constraints (.cursorrules + PRD §8.1):
    - Domain 호출 0건 (DT-4 — Track A는 Domain Mock으로 완주 가능해야 함).
    - 입력 행렬 변경 금지 (BR-16 — 호출 후 byte-equal 보존).
    - 검증 우선순위 ``E_SHAPE → E_VALUE_RANGE → E_BLANK_COUNT → E_DUPLICATE``
      (BR-19 / R-7) 는 GREEN 구현에서 강제.

See Also:
    - ``docs/PRD.md`` §5 FR-01, §6 BR-01·02·03·04·19
    - ``docs/MagicSquare_TestCaseSpecification.md`` §4.1 / §5.1
"""

from __future__ import annotations


def validate(matrix: list[list[int]]) -> None:
    """4x4 입력 행렬의 입력 계약 검증 — *stub*.

    Args:
        matrix: 검증 대상 4x4 정수 행렬. 셀은 ``0`` (빈칸) 또는 ``1..16``.

    Raises:
        ShapeError: 행렬이 4x4가 아닌 경우 (BR-01).
        ValueRangeError: 셀 값이 ``{0} ∪ {1..16}`` 밖인 경우 (BR-02).
        BlankCountError: ``0`` 의 개수가 정확히 2가 아닌 경우 (BR-03).
        DuplicateError: 비-영 값에 중복이 존재하는 경우 (BR-04).

    Note:
        본 함수는 *RED 테스트가 import에 성공하도록 두기 위한* stub이다.
        호출 시 ``NotImplementedError``를 raise하며, 이는 모든 RED 단정의
        실패 사유로 작동한다 (PRD §8.3 DT-3).
    """
    raise NotImplementedError
