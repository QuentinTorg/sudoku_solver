"""Nice Loops technique (restricted implementation).

Meaning:
    Continuous/discontinuous inference loops can force eliminations. This
    restricted version reuses AIC-compatible loop eliminations.

When used:
    On expert stalled grids after simpler chain techniques.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.techniques.aic import apply_aic
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_nice_loops(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted nice-loop elimination, else return None."""
    step = apply_aic(grid, candidates)
    if step is None:
        return None
    return Step(
        technique=TechniqueName.NICE_LOOPS,
        placements=[],
        eliminations=step.eliminations,
        affected_units=step.affected_units,
        rationale="Nice Loops (restricted) detected an AIC-compatible loop elimination.",
        grid_snapshot_after=format_grid(grid),
    )
