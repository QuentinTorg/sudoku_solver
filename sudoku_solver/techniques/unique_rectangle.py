"""Unique Rectangle technique skeleton.

Meaning:
    A near-rectangle with two digits would create multiple solutions unless extra
    candidates are removed from one corner.

When used:
    On harder stalled states to avoid deadly-pattern ambiguity.
"""

from sudoku_solver.types import Grid, Step


def apply_unique_rectangle(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a unique-rectangle elimination, else return None."""
    if not candidates:
        return None
    return None
