"""Blank-cell location (FR-02)."""

from entity.constants import BLANK_CELL, COORD_ONE_BASED, GRID_SIZE


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return 1-based (row, col) of blank cells in row-major order."""
    blanks: list[tuple[int, int]] = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == BLANK_CELL:
                blanks.append((row + COORD_ONE_BASED, col + COORD_ONE_BASED))
    return blanks
