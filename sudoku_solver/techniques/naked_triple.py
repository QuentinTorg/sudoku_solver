"""Naked triple technique skeleton.

Meaning:
    Three cells in a unit contain only three combined digits, allowing those
    digits to be removed from all other cells in the same unit.

When used:
    After pair-based eliminations are exhausted.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step
from sudoku_solver.types import TechniqueName
from sudoku_solver.units import all_units


def apply_naked_triple(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a naked-triple elimination, else return None."""
    if not candidates:
        return None

    for unit_name, unit_cells in all_units():
        eligible_cells = [
            cell_index
            for cell_index in unit_cells
            if cell_index in candidates and 2 <= len(candidates[cell_index]) <= 3
        ]

        for triple_cells in combinations(eligible_cells, 3):
            triple_digits = set().union(*(candidates[cell_index] for cell_index in triple_cells))
            if len(triple_digits) != 3:
                continue

            eliminations: list[tuple[int, int]] = []
            for cell_index in unit_cells:
                if cell_index in triple_cells or cell_index not in candidates:
                    continue
                for digit in sorted(triple_digits):
                    if digit in candidates[cell_index]:
                        eliminations.append((cell_index, digit))

            if eliminations:
                ordered_cells = sorted(triple_cells)
                ordered_digits = sorted(triple_digits)
                return Step(
                    technique=TechniqueName.NAKED_TRIPLE,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[unit_name],
                    rationale=(
                        f"Cells {ordered_cells[0]}, {ordered_cells[1]}, and {ordered_cells[2]} "
                        f"form naked triple {ordered_digits}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
