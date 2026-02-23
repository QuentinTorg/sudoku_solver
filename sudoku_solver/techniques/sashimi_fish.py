"""Sashimi Fish technique (restricted implementation).

Meaning:
    Sashimi fish variants extend finned fish logic for additional eliminations.
    This restricted version reuses finned fish eliminations.

When used:
    On expert stalled grids after standard/finned fish passes.
"""

from sudoku_solver.engines.fish_engine import (
    find_finned_swordfish_elimination,
    find_finned_x_wing_elimination,
)
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_sashimi_fish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted sashimi-fish elimination, else return None."""
    for digit in range(1, 10):
        for fish in (
            find_finned_swordfish_elimination(candidates, digit),
            find_finned_x_wing_elimination(candidates, digit),
        ):
            if fish is None:
                continue
            return Step(
                technique=TechniqueName.SASHIMI_FISH,
                placements=[],
                eliminations=list(fish.eliminations),
                affected_units=list(fish.affected_units),
                rationale=(
                    "Sashimi fish (restricted) reused finned-fish-compatible elimination."
                ),
                grid_snapshot_after=format_grid(grid),
            )
    return None
