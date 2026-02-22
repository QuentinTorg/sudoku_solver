"""X-Wing technique skeleton.

Meaning:
    A single digit forms a rectangle across two rows and two columns, allowing
    eliminations in those columns/rows outside the rectangle.

When used:
    After local candidate techniques stall and digit-level scanning is needed.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import col_cells, col_index, row_cells, row_index


def apply_x_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an X-Wing elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        row_positions: dict[int, list[int]] = {}
        for row in range(9):
            cols = [
                col_index(cell_index)
                for cell_index in row_cells(row)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(cols) == 2:
                row_positions[row] = cols

        for first_row, second_row in combinations(sorted(row_positions), 2):
            if row_positions[first_row] != row_positions[second_row]:
                continue
            first_col, second_col = row_positions[first_row]
            eliminations = [
                (cell_index, digit)
                for col in (first_col, second_col)
                for cell_index in col_cells(col)
                if row_index(cell_index) not in (first_row, second_row)
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.X_WING,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[
                        f"row{first_row + 1}",
                        f"row{second_row + 1}",
                        f"col{first_col + 1}",
                        f"col{second_col + 1}",
                    ],
                    rationale=(
                        f"Digit {digit} forms an X-Wing on rows {first_row + 1} and "
                        f"{second_row + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

        col_positions: dict[int, list[int]] = {}
        for col in range(9):
            rows = [
                row_index(cell_index)
                for cell_index in col_cells(col)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(rows) == 2:
                col_positions[col] = rows

        for first_col, second_col in combinations(sorted(col_positions), 2):
            if col_positions[first_col] != col_positions[second_col]:
                continue
            first_row, second_row = col_positions[first_col]
            eliminations = [
                (cell_index, digit)
                for row in (first_row, second_row)
                for cell_index in row_cells(row)
                if col_index(cell_index) not in (first_col, second_col)
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.X_WING,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[
                        f"col{first_col + 1}",
                        f"col{second_col + 1}",
                        f"row{first_row + 1}",
                        f"row{second_row + 1}",
                    ],
                    rationale=(
                        f"Digit {digit} forms an X-Wing on columns {first_col + 1} and "
                        f"{second_col + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
