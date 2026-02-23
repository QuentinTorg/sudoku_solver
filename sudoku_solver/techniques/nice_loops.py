"""Nice Loops technique (restricted implementation).

Meaning:
    Continuous/discontinuous inference loops can force eliminations. This
    restricted version reuses AIC-compatible loop eliminations.

When used:
    On expert stalled grids after simpler chain techniques.
"""

from sudoku_solver.engines.chain_engine import find_aic_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_nice_loops(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted nice-loop elimination, else return None."""
    elimination = find_aic_elimination(candidates, max_chain_nodes=12)
    if elimination is None:
        return None
    if elimination.pattern == "same_cell_discontinuity":
        rationale = (
            "Nice Loops found a discontinuous same-cell loop and removed non-endpoint candidates."
        )
    else:
        rationale = "Nice Loops (restricted) detected an AIC-compatible loop elimination."
    return Step(
        technique=TechniqueName.NICE_LOOPS,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=[],
        rationale=rationale,
        grid_snapshot_after=format_grid(grid),
    )
