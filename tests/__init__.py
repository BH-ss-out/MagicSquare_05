"""Tests root package.

테스트 디렉토리는 ``.cursorrules`` ``file_structure``에 따라 ``src/`` 구조를
미러링한다 (boundary / control / entity).

Naming Convention (``.cursorrules`` ``testing.naming_convention``):
    - 파일 접두: ``test_``
    - 함수 접두: ``test_``
    - 패턴:     ``test_<대상>_<상황>_<기대결과>``

Test ID 명명 (PRD §8 + §12 Traceability):
    - ``T-U-XXX``  : Track A (Boundary / UI) 테스트
    - ``T-D-XXX``  : Track B (Domain / Logic) 컴포넌트 단위 테스트
    - ``T-INV-XX`` : Track B 불변조건(Invariant) 테스트
    - ``TC-N-XX``  : 시나리오 — Happy Path
    - ``TC-F-XX``  : 시나리오 — Failure Path
    - ``TC-P-XX``  : 시나리오 — 검증 우선순위
    - ``P-XX``     : Property-based 검사

각 테스트는 docstring 또는 ID에 *어느 BR/AC를 보호*하는지 명시한다 (부록 B).
"""
