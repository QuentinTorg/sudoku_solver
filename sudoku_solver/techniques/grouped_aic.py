"""Grouped AIC technique (restricted implementation).

Meaning:
    Alternating inference chains with grouped links. This restricted version
    reuses AIC chain eliminations and reports them as grouped-AIC.

When used:
    On expert stalled grids with chain-heavy candidate structures.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.techniques.aic import apply_aic
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_grouped_aic(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted grouped-AIC elimination, else return None."""
    step = apply_aic(grid, candidates)
    if step is None:
        return None
    return Step(
        technique=TechniqueName.GROUPED_AIC,
        placements=[],
        eliminations=step.eliminations,
        affected_units=step.affected_units,
        rationale="Grouped AIC (restricted) reused AIC-compatible chain elimination.",
        grid_snapshot_after=format_grid(grid),
    )
