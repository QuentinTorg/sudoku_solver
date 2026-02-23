"""Unique Rectangle technique skeleton.

Meaning:
    A near-rectangle with two digits would create multiple solutions unless extra
    candidates are removed from one corner.

When used:
    On harder stalled states to avoid deadly-pattern ambiguity.
"""

from sudoku_solver.engines.uniqueness_engine import find_unique_rectangle_type1_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_unique_rectangle(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a unique-rectangle elimination, else return None."""
    if not candidates:
        return None

    elimination = find_unique_rectangle_type1_elimination(candidates)
    if elimination is None:
        return None

    return Step(
        technique=TechniqueName.UNIQUE_RECTANGLE,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=[
            f"row{elimination.rows[0] + 1}",
            f"row{elimination.rows[1] + 1}",
            f"col{elimination.cols[0] + 1}",
            f"col{elimination.cols[1] + 1}",
        ],
        rationale="Unique Rectangle pattern removes extra candidates from one corner.",
        grid_snapshot_after=format_grid(grid),
    )
