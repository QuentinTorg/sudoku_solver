"""W-Wing technique skeleton.

Meaning:
    Two matching bivalue cells are linked by a strong candidate chain, allowing
    elimination of the opposite digit from their common peers.

When used:
    After XY/XYZ-Wing and pair/triple methods no longer progress.
"""

from sudoku_solver.types import Grid, Step


def apply_w_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a W-Wing elimination, else return None."""
    if not candidates:
        return None
    return None
