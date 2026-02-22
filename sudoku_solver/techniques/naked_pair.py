"""Naked pair technique.

Meaning:
    Two cells in the same unit have identical two-digit candidate sets.

When used:
    After singles and locked candidates have been attempted.

Expected behavior:
    Find valid pair patterns and eliminate those two digits from other cells in
    the same unit, then emit a `Step`.
"""

from sudoku_solver.types import Grid, Step
from sudoku_solver.grid import format_grid
from sudoku_solver.types import TechniqueName
from sudoku_solver.units import all_units


def apply_naked_pair(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a naked-pair elimination, else return None."""
    if not candidates:
        return None

    for unit_name, unit_cells in all_units():
        pair_to_cells: dict[tuple[int, int], list[int]] = {}
        for cell_index in unit_cells:
            if cell_index not in candidates:
                continue
            options = sorted(candidates[cell_index])
            if len(options) != 2:
                continue
            pair = (options[0], options[1])
            pair_to_cells.setdefault(pair, []).append(cell_index)

        for pair in sorted(pair_to_cells):
            cells = sorted(pair_to_cells[pair])
            if len(cells) != 2:
                continue

            eliminations: list[tuple[int, int]] = []
            for cell_index in unit_cells:
                if cell_index in cells or cell_index not in candidates:
                    continue
                for digit in pair:
                    if digit in candidates[cell_index]:
                        eliminations.append((cell_index, digit))

            if eliminations:
                return Step(
                    technique=TechniqueName.NAKED_PAIR,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[unit_name],
                    rationale=f"Cells {cells[0]} and {cells[1]} form naked pair {pair}.",
                    grid_snapshot_after=format_grid(grid),
                )

    return None
