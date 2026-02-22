"""Naked triple technique skeleton.

Meaning:
    Three cells in a unit contain only three combined digits, allowing those
    digits to be removed from all other cells in the same unit.

When used:
    After pair-based eliminations are exhausted.
"""

from sudoku_solver.types import Grid, Step


def apply_naked_triple(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a naked-triple elimination, else return None."""
    _ = (grid, candidates)
    raise NotImplementedError("apply_naked_triple is not implemented yet")
