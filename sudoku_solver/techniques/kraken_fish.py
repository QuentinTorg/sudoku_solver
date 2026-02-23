"""Kraken Fish technique (restricted implementation).

Meaning:
    Fish structures combined with chain forcing can produce deeper eliminations.
    This restricted version reuses classic fish eliminations.

When used:
    On expert stalled grids after fish and chain techniques.
"""

from sudoku_solver.engines.fish_engine import find_standard_fish_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_kraken_fish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted kraken-fish elimination, else return None."""
    for digit in range(1, 10):
        for fish in (
            find_standard_fish_elimination(
                candidates,
                digit,
                size=4,
                exact_line_size=False,
            ),
            find_standard_fish_elimination(
                candidates,
                digit,
                size=3,
                exact_line_size=False,
            ),
            find_standard_fish_elimination(
                candidates,
                digit,
                size=2,
                exact_line_size=True,
            ),
        ):
            if fish is None:
                continue
            return Step(
                technique=TechniqueName.KRAKEN_FISH,
                placements=[],
                eliminations=list(fish.eliminations),
                affected_units=list(fish.affected_units),
                rationale="Kraken fish (restricted) reused fish-compatible elimination.",
                grid_snapshot_after=format_grid(grid),
            )
    return None
