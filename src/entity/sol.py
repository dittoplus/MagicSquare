"""Solver output (FR-05) — Step A: row-major blanks + ascending missing values."""

from entity.constants import BLANK_CELL, VALUE_MAX, VALUE_MIN
from entity.loc import find_blank_coords


def solution(grid: list[list[int]]) -> list[int]:
    """Return int[6] [r1,c1,n1,r2,c2,n2] for Step A (1-index)."""
    blanks = find_blank_coords(grid)
    present = {
        cell
        for row in grid
        for cell in row
        if cell != BLANK_CELL
    }
    missing = [v for v in range(VALUE_MIN, VALUE_MAX + 1) if v not in present]
    (r1, c1), (r2, c2) = blanks[0], blanks[1]
    return [r1, c1, missing[0], r2, c2, missing[1]]
