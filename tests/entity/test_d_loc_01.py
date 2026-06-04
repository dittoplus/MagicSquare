"""D-LOC-01 — find_blank_coords (FR-02 / FR-LOC-01)."""

from entity.loc import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1: list[list[int]]) -> None:
    """D-LOC-01: G1 blanks at (2,2) and (3,3) in row-major order."""
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    result = find_blank_coords(grid_g1)
    # Then: [(2,2),(3,3)] 반환 (1-index, row-major)
    assert result == [(2, 2), (3, 3)]
