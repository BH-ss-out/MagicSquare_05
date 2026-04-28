"""Tests for ``magicsquare.control`` — Track B의 *흐름 제어* 단위.

본 디렉토리는 ``Validator`` / ``UseCase`` / ``Service`` 계층의 단위 테스트를 담는다.
PRD §8.2.1의 ``T-D-050`` ~ ``T-D-052`` (도메인 오케스트레이션 E2E)가 이 위치에 가깝다.

Track B 핵심 원칙 (PRD §8.2):
    - Boundary를 *호출하지 않는다* (DT-5).
    - 입력은 사전조건이 충족된 상태로 직접 전달.
"""
