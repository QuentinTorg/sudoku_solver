"""Finned Swordfish technique.

Meaning:
    A near-swordfish with one extra fin candidate allows eliminations inside the
    fin's box along the swordfish base columns/rows.

When used:
    After standard swordfish if a single extra candidate prevents a pure fish.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_cells, box_index, col_cells, col_index, row_cells, row_index


def apply_finned_swordfish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a finned-swordfish elimination, else return None."""
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
            if 2 <= len(cols) <= 4:
                row_positions[row] = cols

        step = _find_finned_swordfish_row_based(grid, candidates, digit, row_positions)
        if step is not None:
            return step

        col_positions: dict[int, set[int]] = {}
        for col in range(9):
            rows = {
                row_index(cell_index)
                for cell_index in col_cells(col)
                if cell_index in candidates and digit in candidates[cell_index]
            }
            if 2 <= len(rows) <= 4:
                col_positions[col] = rows

        step = _find_finned_swordfish_col_based(grid, candidates, digit, col_positions)
        if step is not None:
            return step

    return None


def _find_finned_swordfish_row_based(
    grid: Grid,
    candidates: dict[int, set[int]],
    digit: int,
    row_positions: dict[int, set[int]],
) -> Step | None:
    for rows in combinations(sorted(row_positions), 3):
        union_cols = set().union(*(row_positions[row] for row in rows))
        if len(union_cols) != 4:
            continue

        for base_cols in combinations(sorted(union_cols), 3):
            base_col_set = set(base_cols)
            # Base columns in a fish must each be supported by at least two rows.
            if any(sum(1 for row in rows if col in row_positions[row]) < 2 for col in base_col_set):
                continue
            fin_rows = [row for row in rows if not row_positions[row].issubset(base_col_set)]
            if len(fin_rows) != 1:
                continue

            fin_row = fin_rows[0]
            fin_cols = row_positions[fin_row] - base_col_set
            # Keep to single-fin variants for safer eliminations.
            if len(fin_cols) != 1:
                continue
            if len(row_positions[fin_row] & base_col_set) < 2:
                continue

            fin_cells = [fin_row * 9 + col for col in sorted(fin_cols)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if col_index(cell_index) in base_col_set
                and row_index(cell_index) != fin_row
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.FINNED_SWORDFISH,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[
                        f"row{rows[0] + 1}",
                        f"row{rows[1] + 1}",
                        f"row{rows[2] + 1}",
                        f"box{fin_box + 1}",
                    ],
                    rationale=(
                        f"Digit {digit} forms a finned swordfish on rows "
                        f"{rows[0] + 1}, {rows[1] + 1}, and {rows[2] + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )
    return None


def _find_finned_swordfish_col_based(
    grid: Grid,
    candidates: dict[int, set[int]],
    digit: int,
    col_positions: dict[int, set[int]],
) -> Step | None:
    for cols in combinations(sorted(col_positions), 3):
        union_rows = set().union(*(col_positions[col] for col in cols))
        if len(union_rows) != 4:
            continue

        for base_rows in combinations(sorted(union_rows), 3):
            base_row_set = set(base_rows)
            # Base rows in a fish must each be supported by at least two columns.
            if any(sum(1 for col in cols if row in col_positions[col]) < 2 for row in base_row_set):
                continue
            fin_cols = [col for col in cols if not col_positions[col].issubset(base_row_set)]
            if len(fin_cols) != 1:
                continue

            fin_col = fin_cols[0]
            fin_rows = col_positions[fin_col] - base_row_set
            # Keep to single-fin variants for safer eliminations.
            if len(fin_rows) != 1:
                continue
            if len(col_positions[fin_col] & base_row_set) < 2:
                continue

            fin_cells = [row * 9 + fin_col for row in sorted(fin_rows)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if row_index(cell_index) in base_row_set
                and col_index(cell_index) != fin_col
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.FINNED_SWORDFISH,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[
                        f"col{cols[0] + 1}",
                        f"col{cols[1] + 1}",
                        f"col{cols[2] + 1}",
                        f"box{fin_box + 1}",
                    ],
                    rationale=(
                        f"Digit {digit} forms a finned swordfish on columns "
                        f"{cols[0] + 1}, {cols[1] + 1}, and {cols[2] + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )
    return None
