"""Finned X-Wing / Sashimi X-Wing technique.

Meaning:
    A near X-Wing with one extra fin candidate allows eliminations in the fin's
    box along the base columns/rows.

When used:
    After standard X-Wing when one extra candidate blocks the pure rectangle.
"""

from sudoku_solver.engines.fish_engine import find_finned_x_wing_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_finned_x_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a finned/sashimi x-wing elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        fish = find_finned_x_wing_elimination(candidates, digit)
        if fish is None:
            continue

        if fish.orientation == "row":
            rationale = (
                f"Digit {digit} forms a finned/sashimi X-Wing on rows "
                f"{fish.base_units[0] + 1} and {fish.base_units[1] + 1}."
            )
        else:
            rationale = (
                f"Digit {digit} forms a finned/sashimi X-Wing on columns "
                f"{fish.base_units[0] + 1} and {fish.base_units[1] + 1}."
            )

        return Step(
            technique=TechniqueName.FINNED_X_WING,
            placements=[],
            eliminations=list(fish.eliminations),
            affected_units=list(fish.affected_units),
            rationale=rationale,
            grid_snapshot_after=format_grid(grid),
        )

    return None
