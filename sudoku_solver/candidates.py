"""Candidate generation and maintenance utilities."""

from sudoku_solver.types import Grid
from sudoku_solver.units import peers

Cell = int


def get_candidates(grid: Grid) -> dict[Cell, set[int]]:
    """Return a candidate set for each unsolved cell."""
    if len(grid.cells) != 81:
        msg = "Grid must contain exactly 81 cells."
        raise ValueError(msg)

    candidates: dict[Cell, set[int]] = {}
    for index, value in enumerate(grid.cells):
        if value != 0:
            continue
        disallowed = _peer_values(grid, index)
        candidates[index] = {digit for digit in range(1, 10) if digit not in disallowed}

    return candidates


def _peer_values(grid: Grid, index: int) -> set[int]:
    values: set[int] = set()
    for peer_index in peers(index):
        peer_value = grid.cells[peer_index]
        if peer_value != 0:
            values.add(peer_value)
    return values
