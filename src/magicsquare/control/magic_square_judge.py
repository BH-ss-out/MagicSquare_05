"""Magic square judgement (FR-04, Track B).

본 모듈은 채워진 4x4 격자가 *마방진 정의(I4)* 를 만족하는지 판정하는
``is_magic_square`` 함수의 *공개 시그니처 stub*만 둔다. 비즈니스 로직 0줄
— 본 모듈의 존재 이유는 *T-D-001 RED 테스트의 컬렉션 실패 회피*에
한정된다 (TC-Spec §6.1 ①).

Public API (계약 합의 — TC-Spec §4.2 전제조건 1):
    is_magic_square(board) -> bool
        모든 행/열/두 대각의 합이 ``MAGIC_CONSTANT`` (= 34) 와 일치하면
        ``True`` 반환. 그렇지 않으면 ``False``.

Constraints (.cursorrules + PRD §8.2):
    - Boundary 호출 금지 (DT-5 / BR-17 / NFR-09).
    - 입력 행렬 변경 금지 (BR-16 — T-D-008 회귀).
    - 결정성 100회 동일 결과 (BR-15 — T-D-009 회귀).

See Also:
    - ``docs/PRD.md`` §5 FR-04, §6 BR-05·06
    - ``docs/MagicSquare_TestCaseSpecification.md`` §4.2 / §5.4
"""

from __future__ import annotations


def is_magic_square(board: list[list[int]]) -> bool:
    """4x4 격자의 마방진 여부 판정 — *stub*.

    Args:
        board: 판정 대상 4x4 정수 격자. 본 함수의 사전조건은
            *모든 셀이 채워져 있고 ``{1..16}`` 다중집합과 일치*함이며,
            사전조건 보장은 호출자(Boundary)의 책임이다 (R-9).

    Returns:
        모든 행/열/두 대각의 합이 ``34`` 와 일치하면 ``True``, 아니면 ``False``.

    Note:
        본 함수는 *RED 테스트가 import에 성공하도록 두기 위한* stub이다.
        호출 시 ``NotImplementedError``를 raise하며, 이는 ``T-D-001``의
        ``assert ... is True`` 단정을 ``AssertionError``로 실패시키는
        *의도된 RED 사유*다 (PRD §8.3 DT-3).
    """
    raise NotImplementedError
