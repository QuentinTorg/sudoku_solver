"""X-Wing technique skeleton.

Meaning:
    A single digit forms a rectangle across two rows and two columns, allowing
    eliminations in those columns/rows outside the rectangle.

When used:
    After local candidate techniques stall and digit-level scanning is needed.
"""

from sudoku_solver.types import Grid, Step


def apply_x_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an X-Wing elimination, else return None."""
    if not candidates:
        return None
    return None
