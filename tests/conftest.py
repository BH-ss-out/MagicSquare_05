"""Shared pytest configuration and fixtures.

본 ``conftest.py``는 ``.cursorrules`` ``testing.fixture_scope``에 따라:
    - 기본 fixture 스코프는 ``function`` (테스트 간 독립성 최우선).
    - 가변 상태 공유 fixture는 절대 ``session`` 스코프로 두지 않는다.
    - 적용 범위는 fixture별로 주석에 명시한다.

현재는 *공통 fixture 0개* 상태(스캐폴딩 직후). 첫 RED 테스트가 *명시적으로 요구*할 때
fixture를 추가한다 (TDD 원칙: 호출 측이 요구하기 전 추가하지 않는다).

See Also:
    - PRD §8.1.1 Track A 필수 RED (T-U-* 시리즈)
    - PRD §8.2.1 Track B 필수 RED (T-D-* 시리즈)
    - PRD §9.3 표준 테스트 데이터 (D-Std, D-In-A 등)
"""
