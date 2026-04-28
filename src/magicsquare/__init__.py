"""Magic Square (4x4) — TDD 학습 프로젝트의 최상위 패키지.

본 패키지는 PRD §10에 정의된 *2-Track 아키텍처*(Boundary / Domain)를
``.cursorrules`` ``architecture.layers``의 3계층(Boundary / Control / Entity)으로 매핑한다.

Subpackages:
    boundary: 외부 호출자와의 입출력 경계. PRD §8.1 Track A의 책임 영역.
    control:  유스케이스 / 검증 흐름 조율. Domain Layer의 흐름 제어 역할.
    entity:   도메인 모델 + I1~I5 불변 규칙 + 도메인 상수의 단일 진실 출처.

See Also:
    - ``docs/PRD.md`` §10 Architecture Overview
    - ``.cursorrules`` ``architecture.layers``
"""

__version__ = "0.1.0"
