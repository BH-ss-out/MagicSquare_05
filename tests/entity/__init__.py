"""Tests for ``magicsquare.entity`` — Track B (Domain / Logic) 도메인 단위 테스트.

본 디렉토리는 PRD §8.2.1의 컴포넌트 단위 테스트와 §8.2.2의 불변조건 테스트를 담는다.

Test ID 매핑:
    ``T-D-001`` ~ ``T-D-009`` : ``MagicSquareJudge`` (FR-04)
    ``T-D-010`` ~ ``T-D-014`` : ``BlankFinder`` (FR-02)
    ``T-D-020`` ~ ``T-D-023`` : ``MissingNumberFinder`` (FR-03)
    ``T-D-030`` ~ ``T-D-032`` : ``FillPlanResolver`` (FR-05)
    ``T-D-040`` ~ ``T-D-042`` : ``MagicResultAssembler`` (FR-05 출력 조립)
    ``T-INV-I1`` ~ ``T-INV-I5`` + ``T-INV-BR16`` : 불변조건 (PRD §8.2.2)
"""
