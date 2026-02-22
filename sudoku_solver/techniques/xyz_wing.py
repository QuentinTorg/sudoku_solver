"""XYZ-Wing technique skeleton.

Meaning:
    A tri-value pivot and two bivalue pincers constrain a shared digit so it
    can be eliminated from common peer cells.

When used:
    After triple-based eliminations for harder stalled states.
"""

from sudoku_solver.types import Grid, Step


def apply_xyz_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an XYZ-Wing elimination, else return None."""
    _ = (grid, candidates)
    raise NotImplementedError("apply_xyz_wing is not implemented yet")
