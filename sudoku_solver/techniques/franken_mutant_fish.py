"""Franken/Mutant Fish technique (expanded implementation).

Meaning:
    Extends fish logic by allowing box-based base units alongside row/column
    bases. The expanded implementation checks both size-2 and size-3 mixed-base
    structures.

When used:
    On expert stalled grids after standard and finned fish scans.
"""

from sudoku_solver.engines.fish_engine import find_franken_mutant_fish_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_franken_mutant_fish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an expanded franken/mutant fish elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        fish = find_franken_mutant_fish_elimination(candidates, digit)
        if fish is None:
            continue
        return Step(
            technique=TechniqueName.FRANKEN_MUTANT_FISH,
            placements=[],
            eliminations=list(fish.eliminations),
            affected_units=list(fish.affected_units),
            rationale=(
                f"Digit {digit} forms an expanded franken/mutant fish "
                "with mixed line/box base units."
            ),
            grid_snapshot_after=format_grid(grid),
        )

    return None
