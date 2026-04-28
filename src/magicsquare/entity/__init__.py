"""Entity Layer — 도메인 모델 + 불변 규칙 + 도메인 상수 (가장 안쪽 계층).

본 계층은 마방진 도메인의 본질을 담는다:
    - I1~I5 불변 조건 자체의 정의
    - Grid / Row / Column / Diagonal / ViolationType 등 도메인 객체
    - ``GRID_SIZE`` / ``MAGIC_CONSTANT`` 등 도메인 상수의 단일 진실 출처 (NFR-06)

Components (예정):
    Grid: Board 자료형 + 불변 보장.
    Invariants: I1~I5 술어 정의 (D6 포함, FR-04 §5).
    Violation: ViolationType, ViolationReport.
    Constants: GRID_SIZE=4, VALUE_RANGE=range(1,17), MAGIC_CONSTANT=34, ...

Test ID Prefix:
    ``T-D-001`` ~ ``T-D-052``, ``T-INV-I1`` ~ ``T-INV-I5``, ``T-INV-BR16``.

Constraints:
    - 어떠한 외부 계층에도 의존하지 않는다 (가장 안쪽).
    - I/O / 프레임워크 / 로깅 등 부수 효과 금지 (BR-16, NFR-04).
"""
