"""Domain failure code exception hierarchy (PRD §0.3).

본 모듈은 PRD §0.3·§7 NFR-07이 정의한 *5종 도메인 실패 코드*의 *최소 stub*만
정의한다. 비즈니스 로직 0줄 — 본 모듈의 존재 이유는 *RED 테스트의 컬렉션
실패 회피*에 한정된다 (TC-Spec §6.1 ①).

Hierarchy (PRD §0.3 / TC-Spec §2.1):
    Exception
    ├── BoundaryError              ← Track A 실패의 공통 부모
    │   ├── ShapeError             ← E_SHAPE
    │   ├── ValueRangeError        ← E_VALUE_RANGE
    │   ├── BlankCountError        ← E_BLANK_COUNT
    │   └── DuplicateError         ← E_DUPLICATE
    └── DomainError                ← Track B 실패의 공통 부모
        └── UnsolvableError        ← E_UNSOLVABLE

표준 메시지(NFR-07 byte-equal)는 ``docs/MagicSquare_TestCaseSpecification.md``
§2.1 표를 단일 진실 출처로 둔다. 본 stub에는 메시지 상수를 두지 않는다
(TDD: 미요구 자산 금지 — GREEN 구현이 raise 시점에 직접 전달).

Constraints (.cursorrules + PRD §8):
    - 클래스 본문은 ``pass`` — 속성·로직 일체 추가 금지.
    - 메시지 변경(NFR-07)은 OPS-2의 *NFR 약화 금지*에 따라 별도 PR로만 가능.

See Also:
    - ``docs/PRD.md`` §0.3 표준 실패 코드
    - ``docs/MagicSquare_TestCaseSpecification.md`` §2.1 표준 메시지
"""

from __future__ import annotations


class BoundaryError(Exception):
    """Track A(Boundary) 실패의 공통 부모 — 입력 계약 위반."""


class ShapeError(BoundaryError):
    """E_SHAPE — 입력이 4x4 행렬이 아님 (BR-01 / I1)."""


class ValueRangeError(BoundaryError):
    """E_VALUE_RANGE — 셀 값이 ``{0} ∪ {1..16}`` 밖 (BR-02 / I2)."""


class BlankCountError(BoundaryError):
    """E_BLANK_COUNT — 빈칸(0) 개수가 정확히 2가 아님 (BR-03 / I3)."""


class DuplicateError(BoundaryError):
    """E_DUPLICATE — 비-영(非零) 값에 중복 존재 (BR-04 / I3)."""


class DomainError(Exception):
    """Track B(Domain) 실패의 공통 부모 — 사전조건 충족 후의 풀이 실패."""


class UnsolvableError(DomainError):
    """E_UNSOLVABLE — 시도 A·B 모두 실패, 마방진 완성 불가 (BR-14)."""
