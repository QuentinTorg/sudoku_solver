"""W-Wing technique skeleton.

Meaning:
    Two matching bivalue cells are linked by a strong candidate chain, allowing
    elimination of the opposite digit from their common peers.

When used:
    After XY/XYZ-Wing and pair/triple methods no longer progress.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units, peers


def apply_w_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a W-Wing elimination, else return None."""
    if not candidates:
        return None

    strong_links: dict[int, list[tuple[int, int, str]]] = {}
    for unit_name, unit_cells in all_units():
        for digit in range(1, 10):
            positions = [
                cell_index
                for cell_index in unit_cells
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) == 2:
                strong_links.setdefault(digit, []).append((positions[0], positions[1], unit_name))

    bivalue_cells = [
        cell_index
        for cell_index in sorted(candidates)
        if len(candidates[cell_index]) == 2
    ]

    for first, second in combinations(bivalue_cells, 2):
        first_digits = candidates[first]
        second_digits = candidates[second]
        if first_digits != second_digits:
            continue
        if second in peers(first):
            continue

        for link_digit in sorted(first_digits):
            other_digit = next(iter(first_digits - {link_digit}))
            for link_first, link_second, unit_name in strong_links.get(link_digit, []):
                aligned = (
                    link_first in peers(first)
                    and link_second in peers(second)
                ) or (
                    link_second in peers(first)
                    and link_first in peers(second)
                )
                if not aligned:
                    continue

                eliminations = [
                    (cell_index, other_digit)
                    for cell_index in sorted(peers(first) & peers(second))
                    if cell_index in candidates and other_digit in candidates[cell_index]
                ]
                if not eliminations:
                    continue

                return Step(
                    technique=TechniqueName.W_WING,
                    placements=[],
                    eliminations=eliminations,
                    affected_units=[unit_name],
                    rationale=(
                        f"Cells {first} and {second} form W-Wing via strong link "
                        f"for digit {link_digit}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
