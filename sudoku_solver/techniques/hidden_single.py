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

from sudoku_solver.types import Grid, Step
from sudoku_solver.grid import format_grid
from sudoku_solver.types import TechniqueName


def apply_hidden_single(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a hidden single placement, else return None."""
    digit_to_cells: dict[int, list[int]] = {digit: [] for digit in range(1, 10)}
    for cell_index in sorted(candidates):
        for digit in sorted(candidates[cell_index]):
            digit_to_cells[digit].append(cell_index)

    for digit in range(1, 10):
        cells = digit_to_cells[digit]
        if len(cells) != 1:
            continue
        cell_index = cells[0]
        return Step(
            technique=TechniqueName.HIDDEN_SINGLE,
            placements=[(cell_index, digit)],
            eliminations=[],
            affected_units=[_unit_label(cell_index)],
            rationale=f"Digit {digit} appears in candidates for only one cell.",
            grid_snapshot_after=format_grid(grid),
        )
    return None


def _unit_label(cell_index: int) -> str:
    row = cell_index // 9 + 1
    col = cell_index % 9 + 1
    return f"r{row}c{col}"
