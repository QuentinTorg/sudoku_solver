"""Hidden single technique.

Meaning:
    Within a unit (row, column, or box), a digit appears in candidates for
    exactly one cell.

When used:
    After naked singles in each solve iteration.

Expected behavior:
    Scan units for digits with a single valid position, place the digit in that
    cell, and emit a `Step`.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units, cell_label


def apply_hidden_single(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a hidden single placement, else return None."""
    for unit_name, unit_cells in all_units():
        for digit in range(1, 10):
            matching_cells = [
                cell_index
                for cell_index in unit_cells
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(matching_cells) != 1:
                continue

            cell_index = matching_cells[0]
            return Step(
                technique=TechniqueName.HIDDEN_SINGLE,
                placements=[(cell_index, digit)],
                eliminations=[],
                affected_units=[unit_name, cell_label(cell_index)],
                rationale=f"Digit {digit} can only appear once in {unit_name}.",
                grid_snapshot_after=format_grid(grid),
            )
    return None
