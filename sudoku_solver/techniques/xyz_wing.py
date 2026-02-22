"""XYZ-Wing technique skeleton.

Meaning:
    A tri-value pivot and two bivalue pincers constrain a shared digit so it
    can be eliminated from common peer cells.

When used:
    After triple-based eliminations for harder stalled states.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import peers


def apply_xyz_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an XYZ-Wing elimination, else return None."""
    if not candidates:
        return None

    for pivot in sorted(candidates):
        pivot_digits = candidates[pivot]
        if len(pivot_digits) != 3:
            continue

        pivot_peers = peers(pivot)
        pincer_cells = [
            cell_index
            for cell_index in sorted(pivot_peers)
            if cell_index in candidates
            and len(candidates[cell_index]) == 2
            and candidates[cell_index].issubset(pivot_digits)
        ]

        for first, second in combinations(pincer_cells, 2):
            first_digits = candidates[first]
            second_digits = candidates[second]

            if first_digits | second_digits != pivot_digits:
                continue

            shared = first_digits & second_digits
            if len(shared) != 1:
                continue
            wing_digit = next(iter(shared))

            common_peers = peers(pivot) & peers(first) & peers(second)
            eliminations = [
                (cell_index, wing_digit)
                for cell_index in sorted(common_peers)
                if cell_index in candidates and wing_digit in candidates[cell_index]
            ]
            if not eliminations:
                continue

            return Step(
                technique=TechniqueName.XYZ_WING,
                placements=[],
                eliminations=eliminations,
                affected_units=[],
                rationale=(
                    f"Pivot {pivot} with pincers {first} and {second} forms XYZ-Wing "
                    f"eliminating digit {wing_digit}."
                ),
                grid_snapshot_after=format_grid(grid),
            )

    return None
