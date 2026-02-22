"""XY-Wing technique skeleton.

Meaning:
    A pivot cell with two candidates links to two matching pincer cells, forcing
    eliminations of a shared digit from common peers.

When used:
    After pair/triple eliminations stop producing progress.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import peers


def apply_xy_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an XY-Wing elimination, else return None."""
    if not candidates:
        return None

    for pivot in sorted(candidates):
        pivot_digits = candidates[pivot]
        if len(pivot_digits) != 2:
            continue

        pivot_peers = peers(pivot)
        pincer_cells = [
            cell_index
            for cell_index in sorted(pivot_peers)
            if cell_index in candidates
            and len(candidates[cell_index]) == 2
            and len(candidates[cell_index] & pivot_digits) == 1
        ]

        for first, second in combinations(pincer_cells, 2):
            first_digits = candidates[first]
            second_digits = candidates[second]

            if len((first_digits & pivot_digits) | (second_digits & pivot_digits)) != 2:
                continue

            shared = (first_digits & second_digits) - pivot_digits
            if len(shared) != 1:
                continue
            if second in peers(first):
                continue

            wing_digit = next(iter(shared))
            eliminations = [
                (cell_index, wing_digit)
                for cell_index in sorted(peers(first) & peers(second))
                if cell_index in candidates and wing_digit in candidates[cell_index]
            ]
            if not eliminations:
                continue

            return Step(
                technique=TechniqueName.XY_WING,
                placements=[],
                eliminations=eliminations,
                affected_units=[],
                rationale=(
                    f"Pivot {pivot} with pincers {first} and {second} forms XY-Wing "
                    f"eliminating digit {wing_digit}."
                ),
                grid_snapshot_after=format_grid(grid),
            )

    return None
