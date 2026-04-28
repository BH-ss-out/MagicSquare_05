"""Boundary Layer — 외부 호출자와의 입출력 경계 (PRD §8.1 / §10.1).

본 계층은 PRD §0 입출력 계약을 *위임 직전*에 검증하고,
위반 시 단일 도메인 실패 코드(``E_SHAPE`` / ``E_VALUE_RANGE`` /
``E_BLANK_COUNT`` / ``E_DUPLICATE``)와 표준 영문 메시지(byte-equal, NFR-07)를 반환한다.

Components (예정):
    InputValidator: FR-01 입력 검증 — 5단계 순서(BR-19) 평가.
    ResultFormatter: 도메인 ``int[6]`` 결과의 외부 노출(필요 시).

Test ID Prefix:
    ``T-U-001`` ~ ``T-U-074`` (PRD §8.1.1 Contract-first RED 테스트).

Constraints:
    - Domain의 *공개 함수 시그니처* 에만 의존(DIP, A-3).
    - Domain VO를 외부 호출자에게 그대로 노출하지 않는다(A-2).
"""
