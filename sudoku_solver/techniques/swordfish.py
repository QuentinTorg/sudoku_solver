"""Swordfish technique.

Meaning:
    A digit aligns across three rows and three columns, allowing eliminations
    from the shared columns/rows outside the fish.

When used:
    As an advanced single-digit pattern after X-Wing.
"""

from sudoku_solver.engines.fish_engine import find_standard_fish_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_swordfish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a swordfish elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        fish = find_standard_fish_elimination(
            candidates,
            digit,
            size=3,
            exact_line_size=False,
        )
        if fish is None:
            continue

        if fish.orientation == "row":
            rationale = (
                "Digit "
                f"{digit} forms a swordfish on rows {fish.base_units[0] + 1}, "
                f"{fish.base_units[1] + 1}, and {fish.base_units[2] + 1}."
            )
            affected = [f"row{unit + 1}" for unit in fish.base_units]
        else:
            rationale = (
                "Digit "
                f"{digit} forms a swordfish on columns {fish.base_units[0] + 1}, "
                f"{fish.base_units[1] + 1}, and {fish.base_units[2] + 1}."
            )
            affected = [f"col{unit + 1}" for unit in fish.base_units]

        return Step(
            technique=TechniqueName.SWORDFISH,
            placements=[],
            eliminations=list(fish.eliminations),
            affected_units=affected,
            rationale=rationale,
            grid_snapshot_after=format_grid(grid),
        )

    return None
