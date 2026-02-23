"""Sashimi Fish technique (restricted implementation).

Meaning:
    Sashimi fish variants extend finned fish logic for additional eliminations.
    This restricted version reuses finned fish eliminations.

When used:
    On expert stalled grids after standard/finned fish passes.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.techniques.finned_swordfish import apply_finned_swordfish
from sudoku_solver.techniques.finned_x_wing import apply_finned_x_wing
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_sashimi_fish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted sashimi-fish elimination, else return None."""
    for fish_step in (
        apply_finned_swordfish(grid, candidates),
        apply_finned_x_wing(grid, candidates),
    ):
        if fish_step is None:
            continue
        return Step(
            technique=TechniqueName.SASHIMI_FISH,
            placements=[],
            eliminations=fish_step.eliminations,
            affected_units=fish_step.affected_units,
            rationale="Sashimi fish (restricted) reused finned-fish-compatible elimination.",
            grid_snapshot_after=format_grid(grid),
        )
    return None
