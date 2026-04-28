"""Tests for ``magicsquare.boundary`` — Track A (Boundary / UI) 테스트.

본 디렉토리는 PRD §8.1.1의 ``T-U-001`` ~ ``T-U-074`` 시리즈를 담는다.

Track A 핵심 원칙 (PRD §8.1):
    - Domain은 *Mock으로 가정* — 실제 Domain 구현 없이 RED→GREEN 완주 가능 (DT-4).
    - 표준 에러 메시지(byte-equal, NFR-07)와 검증 우선순위(BR-19)를 *문자 그대로* 단정.
"""
