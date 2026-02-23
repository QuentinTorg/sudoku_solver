"""Finned Swordfish technique.

Meaning:
    A near-swordfish with one extra fin candidate allows eliminations inside the
    fin's box along the swordfish base columns/rows.

When used:
    After standard swordfish if a single extra candidate prevents a pure fish.
"""

from sudoku_solver.engines.fish_engine import find_finned_swordfish_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_finned_swordfish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a finned-swordfish elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        fish = find_finned_swordfish_elimination(candidates, digit)
        if fish is None:
            continue

        if fish.orientation == "row":
            rationale = (
                f"Digit {digit} forms a finned swordfish on rows "
                f"{fish.base_units[0] + 1}, {fish.base_units[1] + 1}, "
                f"and {fish.base_units[2] + 1}."
            )
        else:
            rationale = (
                f"Digit {digit} forms a finned swordfish on columns "
                f"{fish.base_units[0] + 1}, {fish.base_units[1] + 1}, "
                f"and {fish.base_units[2] + 1}."
            )

        return Step(
            technique=TechniqueName.FINNED_SWORDFISH,
            placements=[],
            eliminations=list(fish.eliminations),
            affected_units=list(fish.affected_units),
            rationale=rationale,
            grid_snapshot_after=format_grid(grid),
        )

    return None
