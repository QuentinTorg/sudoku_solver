"""BUG+1 technique.

Meaning:
    If every unsolved cell is bivalue except one tri-value cell, and one digit
    has odd candidate parity in that cell's row/column/box, that digit is forced.

When used:
    Late in human-only solving on near-complete grids.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_cells, box_index, col_cells, col_index, row_cells, row_index


def apply_bug_plus_one(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply BUG+1 placement, else return None."""
    if not candidates:
        return None

    non_bivalue = [cell_index for cell_index, options in candidates.items() if len(options) != 2]
    if len(non_bivalue) != 1:
        return None

    target = non_bivalue[0]
    target_options = candidates[target]
    if len(target_options) != 3:
        return None

    target_row = row_index(target)
    target_col = col_index(target)
    target_box = box_index(target)

    odd_digits = []
    for digit in sorted(target_options):
        row_count = _candidate_count(row_cells(target_row), candidates, digit)
        col_count = _candidate_count(col_cells(target_col), candidates, digit)
        box_count = _candidate_count(box_cells(target_box), candidates, digit)
        if row_count % 2 == 1 and col_count % 2 == 1 and box_count % 2 == 1:
            odd_digits.append(digit)

    if len(odd_digits) != 1:
        return None

    placed_digit = odd_digits[0]
    return Step(
        technique=TechniqueName.BUG_PLUS_ONE,
        placements=[(target, placed_digit)],
        eliminations=[],
        affected_units=[
            f"row{target_row + 1}",
            f"col{target_col + 1}",
            f"box{target_box + 1}",
        ],
        rationale=(
            f"BUG+1 at cell {target}: digit {placed_digit} has odd parity in row/column/box."
        ),
        grid_snapshot_after=format_grid(grid),
    )


def _candidate_count(unit_cells: list[int], candidates: dict[int, set[int]], digit: int) -> int:
    return sum(1 for cell_index in unit_cells if digit in candidates.get(cell_index, set()))
