"""Empty Rectangle technique.

Meaning:
    A box forms an L-shape of candidates for one digit; combining this with row
    and column strong links allows an elimination at a crossing cell.

When used:
    As an advanced single-digit chain pattern on difficult stalled grids.
"""

from itertools import product

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_cells, box_index, col_cells, col_index, row_cells, row_index


def apply_empty_rectangle(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an empty-rectangle elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        for box in range(9):
            box_positions = [
                cell_index
                for cell_index in box_cells(box)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(box_positions) < 3:
                continue

            box_rows = sorted({row_index(cell_index) for cell_index in box_positions})
            box_cols = sorted({col_index(cell_index) for cell_index in box_positions})

            for row, col in product(box_rows, box_cols):
                corner = row * 9 + col
                if box_index(corner) != box:
                    continue
                if corner in box_positions:
                    continue

                if not all(
                    row_index(cell_index) == row or col_index(cell_index) == col
                    for cell_index in box_positions
                ):
                    continue

                row_outside = [
                    cell_index
                    for cell_index in row_cells(row)
                    if box_index(cell_index) != box
                    and cell_index in candidates
                    and digit in candidates[cell_index]
                ]
                col_outside = [
                    cell_index
                    for cell_index in col_cells(col)
                    if box_index(cell_index) != box
                    and cell_index in candidates
                    and digit in candidates[cell_index]
                ]
                if len(row_outside) != 2 or len(col_outside) != 2:
                    continue

                for row_end in row_outside:
                    for col_end in col_outside:
                        target_cell = row_index(col_end) * 9 + col_index(row_end)
                        if target_cell in {row_end, col_end}:
                            continue
                        if box_index(target_cell) == box:
                            continue
                        if target_cell in candidates and digit in candidates[target_cell]:
                            return Step(
                                technique=TechniqueName.EMPTY_RECTANGLE,
                                placements=[],
                                eliminations=[(target_cell, digit)],
                                affected_units=[f"box{box + 1}", f"row{row + 1}", f"col{col + 1}"],
                                rationale=(
                                    f"Digit {digit} forms empty rectangle in box {box + 1} "
                                    f"with row {row + 1} and column {col + 1}."
                                ),
                                grid_snapshot_after=format_grid(grid),
                            )

    return None
