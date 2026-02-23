"""ALS-XZ technique (expanded implementation).

Meaning:
    Two almost-locked sets (ALS) with a restricted common candidate can force
    eliminations of another shared candidate.

When used:
    On advanced stalled grids after chain and fish techniques.
"""

from sudoku_solver.engines.als_engine import find_als_xz_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_als_xz(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an expanded ALS-XZ elimination, else return None."""
    if not candidates:
        return None

    elimination = find_als_xz_elimination(candidates)
    if elimination is None:
        return None

    return Step(
        technique=TechniqueName.ALS_XZ,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=list(elimination.affected_units),
        rationale=(
            f"ALS-XZ with restricted digit {elimination.restricted_digit} "
            f"eliminates digit {elimination.target_digit}."
        ),
        grid_snapshot_after=format_grid(grid),
    )
