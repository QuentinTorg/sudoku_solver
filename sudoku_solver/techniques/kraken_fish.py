"""Kraken Fish technique (expanded implementation).

Meaning:
    Fish structures combined with chain forcing can produce deeper eliminations.
    The expanded implementation scans classic fish plus finned-fish-compatible
    structures to widen late-game fish coverage.

When used:
    On expert stalled grids after fish and chain techniques.
"""

from sudoku_solver.engines.fish_engine import (
    find_finned_swordfish_elimination,
    find_finned_x_wing_elimination,
    find_standard_fish_elimination,
)
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_kraken_fish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an expanded kraken-fish elimination, else return None."""
    for digit in range(1, 10):
        for fish in (
            find_standard_fish_elimination(
                candidates,
                digit,
                size=4,
                exact_line_size=False,
            ),
            find_finned_swordfish_elimination(candidates, digit),
            find_finned_x_wing_elimination(candidates, digit),
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
                rationale=(
                    "Kraken fish (expanded) found a fish-compatible elimination "
                    "from classic/finned fish structure."
                ),
                grid_snapshot_after=format_grid(grid),
            )
    return None
