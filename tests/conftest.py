"""Shared pytest fixtures — grid data only (no domain logic)."""

import pytest

from entity.constants import GRID_SIZE


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1: partial 4×4 grid; blanks at (2,2) and (3,3) 1-index; missing {7, 10}."""
    grid = [
        [1, 2, 3, 4],
        [5, 0, 6, 8],
        [9, 11, 0, 12],
        [13, 14, 15, 16],
    ]
    assert len(grid) == GRID_SIZE
    assert all(len(row) == GRID_SIZE for row in grid)
    return grid
