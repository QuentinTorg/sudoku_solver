"""Naked quad technique.

Meaning:
    Four cells in one unit contain only four combined digits, allowing those
    digits to be removed from other cells in the same unit.

When used:
    After triple techniques if additional local eliminations are needed.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units


def apply_naked_quad(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a naked-quad elimination, else return None."""
    if not candidates:
        return None

    for unit_name, unit_cells in all_units():
        eligible_cells = [
            cell_index
            for cell_index in unit_cells
            if cell_index in candidates and 2 <= len(candidates[cell_index]) <= 4
        ]

        for quad_cells in combinations(eligible_cells, 4):
            quad_digits = set().union(*(candidates[cell_index] for cell_index in quad_cells))
            if len(quad_digits) != 4:
                continue

            eliminations: list[tuple[int, int]] = []
            for cell_index in unit_cells:
                if cell_index in quad_cells or cell_index not in candidates:
                    continue
                for digit in sorted(quad_digits):
                    if digit in candidates[cell_index]:
                        eliminations.append((cell_index, digit))

            if eliminations:
                return Step(
                    technique=TechniqueName.NAKED_QUAD,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[unit_name],
                    rationale=(
                        f"Cells {sorted(quad_cells)} form naked quad {sorted(quad_digits)} "
                        f"in {unit_name}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
