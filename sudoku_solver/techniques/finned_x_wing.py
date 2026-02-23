"""Finned X-Wing / Sashimi X-Wing technique.

Meaning:
    A near X-Wing with one extra fin candidate allows eliminations in the fin's
    box along the base columns/rows.

When used:
    After standard X-Wing when one extra candidate blocks the pure rectangle.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_cells, box_index, col_cells, col_index, row_cells, row_index


def apply_finned_x_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a finned/sashimi x-wing elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        row_positions: dict[int, set[int]] = {}
        for row in range(9):
            cols = {
                col_index(cell_index)
                for cell_index in row_cells(row)
                if cell_index in candidates and digit in candidates[cell_index]
            }
            if 1 <= len(cols) <= 3:
                row_positions[row] = cols

        step = _find_finned_x_wing_row_based(grid, candidates, digit, row_positions)
        if step is not None:
            return step

        col_positions: dict[int, set[int]] = {}
        for col in range(9):
            rows = {
                row_index(cell_index)
                for cell_index in col_cells(col)
                if cell_index in candidates and digit in candidates[cell_index]
            }
            if 1 <= len(rows) <= 3:
                col_positions[col] = rows

        step = _find_finned_x_wing_col_based(grid, candidates, digit, col_positions)
        if step is not None:
            return step

    return None


def _find_finned_x_wing_row_based(
    grid: Grid,
    candidates: dict[int, set[int]],
    digit: int,
    row_positions: dict[int, set[int]],
) -> Step | None:
    for rows in combinations(sorted(row_positions), 2):
        cols_union = row_positions[rows[0]] | row_positions[rows[1]]
        if len(cols_union) != 3:
            continue

        for base_cols in combinations(sorted(cols_union), 2):
            base_col_set = set(base_cols)
            base_counts = [len(row_positions[row] & base_col_set) for row in rows]
            if min(base_counts) < 1 or max(base_counts) > 2:
                continue
            if not any(count == 2 for count in base_counts):
                continue

            fin_rows = [row for row in rows if len(row_positions[row] - base_col_set) > 0]
            if len(fin_rows) != 1:
                continue

            fin_row = fin_rows[0]
            fin_cols = row_positions[fin_row] - base_col_set
            fin_cells = [fin_row * 9 + col for col in sorted(fin_cols)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if col_index(cell_index) in base_col_set
                and row_index(cell_index) not in rows
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.FINNED_X_WING,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[f"row{rows[0] + 1}", f"row{rows[1] + 1}", f"box{fin_box + 1}"],
                    rationale=(
                        f"Digit {digit} forms a finned/sashimi X-Wing on rows "
                        f"{rows[0] + 1} and {rows[1] + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )
    return None


def _find_finned_x_wing_col_based(
    grid: Grid,
    candidates: dict[int, set[int]],
    digit: int,
    col_positions: dict[int, set[int]],
) -> Step | None:
    for cols in combinations(sorted(col_positions), 2):
        rows_union = col_positions[cols[0]] | col_positions[cols[1]]
        if len(rows_union) != 3:
            continue

        for base_rows in combinations(sorted(rows_union), 2):
            base_row_set = set(base_rows)
            base_counts = [len(col_positions[col] & base_row_set) for col in cols]
            if min(base_counts) < 1 or max(base_counts) > 2:
                continue
            if not any(count == 2 for count in base_counts):
                continue

            fin_cols = [col for col in cols if len(col_positions[col] - base_row_set) > 0]
            if len(fin_cols) != 1:
                continue

            fin_col = fin_cols[0]
            fin_rows = col_positions[fin_col] - base_row_set
            fin_cells = [row * 9 + fin_col for row in sorted(fin_rows)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if row_index(cell_index) in base_row_set
                and col_index(cell_index) not in cols
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.FINNED_X_WING,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[f"col{cols[0] + 1}", f"col{cols[1] + 1}", f"box{fin_box + 1}"],
                    rationale=(
                        f"Digit {digit} forms a finned/sashimi X-Wing on columns "
                        f"{cols[0] + 1} and {cols[1] + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )
    return None
