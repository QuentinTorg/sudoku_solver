"""XY-Wing technique skeleton.

Meaning:
    A pivot cell with two candidates links to two matching pincer cells, forcing
    eliminations of a shared digit from common peers.

When used:
    After pair/triple eliminations stop producing progress.
"""

from sudoku_solver.types import Grid, Step


def apply_xy_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an XY-Wing elimination, else return None."""
    if not candidates:
        return None
    return None
