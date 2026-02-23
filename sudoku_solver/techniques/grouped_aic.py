"""Grouped AIC technique (restricted implementation).

Meaning:
    Alternating inference chains with grouped links. This restricted version
    reuses AIC chain eliminations and reports them as grouped-AIC.

When used:
    On expert stalled grids with chain-heavy candidate structures.
"""

from sudoku_solver.engines.chain_engine import find_aic_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_grouped_aic(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted grouped-AIC elimination, else return None."""
    elimination = find_aic_elimination(candidates, max_chain_nodes=12)
    if elimination is None:
        return None
    if elimination.pattern == "same_cell_discontinuity":
        rationale = (
            "Grouped AIC found a discontinuous same-cell loop "
            "and removed non-endpoint candidates."
        )
    else:
        rationale = "Grouped AIC (restricted) reused AIC-compatible chain elimination."
    return Step(
        technique=TechniqueName.GROUPED_AIC,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=[],
        rationale=rationale,
        grid_snapshot_after=format_grid(grid),
    )
