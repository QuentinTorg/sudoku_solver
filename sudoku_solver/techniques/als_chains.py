"""ALS Chains technique (restricted implementation).

Meaning:
    Chains of almost-locked sets can force eliminations. This restricted
    version first checks 3-ALS RCC chains, then falls back to ALS-XZ style.

When used:
    On advanced stalled grids where direct ALS-XZ is insufficient.
"""

from sudoku_solver.engines.als_engine import find_als_chain_elimination, find_als_xz_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_als_chains(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted ALS-chain elimination, else return None."""
    elimination = find_als_chain_elimination(candidates)
    rationale = "ALS RCC-chain (restricted) found a 3-ALS elimination."
    if elimination is None:
        elimination = find_als_xz_elimination(candidates)
        rationale = "ALS Chains (restricted) reused ALS-XZ-compatible elimination."
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
