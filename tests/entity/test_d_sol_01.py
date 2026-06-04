"""D-SOL-01 — solution() Step A (FR-05 / invariant I8)."""

from tests._approval import assert_matches_golden

from entity.sol import solution

GOLDEN_D_SOL_01_G1_STEP_A = "golden/d_sol_01_g1_step_a.approved.txt"


def test_d_sol_01_step_a_success(grid_g1: list[list[int]]) -> None:
    """D-SOL-01: G1 Step A returns int[6] [r1,c1,n1,r2,c2,n2] (1-index)."""
    # Given: G1 격자
    # When: solution(grid_g1) 호출
    result = solution(grid_g1)
    # Then: Golden Master — int[6] 고정 포맷
    assert_matches_golden(result, GOLDEN_D_SOL_01_G1_STEP_A)
