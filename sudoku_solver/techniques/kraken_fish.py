"""Kraken Fish technique (restricted implementation).

Meaning:
    Fish structures combined with chain forcing can produce deeper eliminations.
    This restricted version reuses classic fish eliminations.

When used:
    On expert stalled grids after fish and chain techniques.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.techniques.jellyfish import apply_jellyfish
from sudoku_solver.techniques.swordfish import apply_swordfish
from sudoku_solver.techniques.x_wing import apply_x_wing
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_kraken_fish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted kraken-fish elimination, else return None."""
    for fish_step in (
        apply_jellyfish(grid, candidates),
        apply_swordfish(grid, candidates),
        apply_x_wing(grid, candidates),
    ):
        if fish_step is None:
            continue
        return Step(
            technique=TechniqueName.KRAKEN_FISH,
            placements=[],
            eliminations=fish_step.eliminations,
            affected_units=fish_step.affected_units,
            rationale="Kraken fish (restricted) reused fish-compatible elimination.",
            grid_snapshot_after=format_grid(grid),
        )
    return None
