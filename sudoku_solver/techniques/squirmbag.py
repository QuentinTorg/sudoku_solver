"""Squirmbag technique.

Meaning:
    A size-5 fish pattern for one digit across five rows/columns. Candidates
    for that digit outside the fish footprint can be eliminated.

When used:
    Very late on expert fish-heavy stalled states.
"""

from sudoku_solver.engines.fish_engine import find_standard_fish_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_squirmbag(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a squirmbag elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        fish = find_standard_fish_elimination(
            candidates,
            digit,
            size=5,
            exact_line_size=False,
        )
        if fish is None:
            continue

        if fish.orientation == "row":
            rationale = (
                "Digit "
                f"{digit} forms a squirmbag on rows {fish.base_units[0] + 1}, "
                f"{fish.base_units[1] + 1}, {fish.base_units[2] + 1}, "
                f"{fish.base_units[3] + 1}, and {fish.base_units[4] + 1}."
            )
            affected = [f"row{unit + 1}" for unit in fish.base_units]
        else:
            rationale = (
                "Digit "
                f"{digit} forms a squirmbag on columns {fish.base_units[0] + 1}, "
                f"{fish.base_units[1] + 1}, {fish.base_units[2] + 1}, "
                f"{fish.base_units[3] + 1}, and {fish.base_units[4] + 1}."
            )
            affected = [f"col{unit + 1}" for unit in fish.base_units]

        return Step(
            technique=TechniqueName.SQUIRMBAG,
            placements=[],
            eliminations=list(fish.eliminations),
            affected_units=affected,
            rationale=rationale,
            grid_snapshot_after=format_grid(grid),
        )

    return None
