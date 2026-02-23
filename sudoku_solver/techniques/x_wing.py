"""X-Wing technique skeleton.

Meaning:
    A single digit forms a rectangle across two rows and two columns, allowing
    eliminations in those columns/rows outside the rectangle.

When used:
    After local candidate techniques stall and digit-level scanning is needed.
"""

from sudoku_solver.engines.fish_engine import find_standard_fish_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_x_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an X-Wing elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        fish = find_standard_fish_elimination(
            candidates,
            digit,
            size=2,
            exact_line_size=True,
        )
        if fish is None:
            continue

        if fish.orientation == "row":
            rationale = (
                f"Digit {digit} forms an X-Wing on rows {fish.base_units[0] + 1} and "
                f"{fish.base_units[1] + 1}."
            )
        else:
            rationale = (
                f"Digit {digit} forms an X-Wing on columns {fish.base_units[0] + 1} and "
                f"{fish.base_units[1] + 1}."
            )

        return Step(
            technique=TechniqueName.X_WING,
            placements=[],
            eliminations=list(fish.eliminations),
            affected_units=list(fish.affected_units),
            rationale=rationale,
            grid_snapshot_after=format_grid(grid),
        )

    return None
