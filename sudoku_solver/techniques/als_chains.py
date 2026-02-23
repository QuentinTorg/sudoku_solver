"""ALS Chains technique (expanded implementation).

Meaning:
    Chains of almost-locked sets can force eliminations. The expanded
    implementation checks RCC-chain eliminations, then ALS XY-Wing structures,
    then ALS-XZ-compatible consequences.

When used:
    On advanced stalled grids where direct ALS-XZ is insufficient.
"""

from sudoku_solver.engines.als_engine import (
    find_als_chain_elimination,
    find_als_xy_wing_elimination,
    find_als_xz_elimination,
)
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_als_chains(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an expanded ALS-chain elimination, else return None."""
    elimination = find_als_chain_elimination(candidates)
    rationale = "ALS RCC-chain (expanded) found a chain elimination."
    if elimination is None:
        elimination = find_als_xy_wing_elimination(candidates)
        rationale = "ALS Chains (expanded) found an ALS XY-Wing elimination."
    if elimination is None:
        elimination = find_als_xz_elimination(candidates)
        rationale = "ALS Chains (expanded) reused ALS-XZ-compatible elimination."
    if elimination is None:
        return None
    return Step(
        technique=TechniqueName.ALS_CHAINS,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=list(elimination.affected_units),
        rationale=rationale,
        grid_snapshot_after=format_grid(grid),
    )
