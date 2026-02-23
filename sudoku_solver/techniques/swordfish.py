"""Swordfish technique.

Meaning:
    A digit aligns across three rows and three columns, allowing eliminations
    from the shared columns/rows outside the fish.

When used:
    As an advanced single-digit pattern after X-Wing.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import col_cells, col_index, row_cells, row_index


def apply_swordfish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a swordfish elimination, else return None."""
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
            if 2 <= len(cols) <= 3:
                row_positions[row] = cols

        for rows in combinations(sorted(row_positions), 3):
            union_cols = set().union(*(row_positions[row] for row in rows))
            if len(union_cols) != 3:
                continue
            eliminations = [
                (cell_index, digit)
                for col in sorted(union_cols)
                for cell_index in col_cells(col)
                if row_index(cell_index) not in rows
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.SWORDFISH,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[
                        f"row{rows[0] + 1}",
                        f"row{rows[1] + 1}",
                        f"row{rows[2] + 1}",
                    ],
                    rationale=(
                        f"Digit {digit} forms a swordfish on rows "
                        f"{rows[0] + 1}, {rows[1] + 1}, and {rows[2] + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

        col_positions: dict[int, set[int]] = {}
        for col in range(9):
            rows = {
                row_index(cell_index)
                for cell_index in col_cells(col)
                if cell_index in candidates and digit in candidates[cell_index]
            }
            if 2 <= len(rows) <= 3:
                col_positions[col] = rows

        for cols in combinations(sorted(col_positions), 3):
            union_rows = set().union(*(col_positions[col] for col in cols))
            if len(union_rows) != 3:
                continue
            eliminations = [
                (cell_index, digit)
                for row in sorted(union_rows)
                for cell_index in row_cells(row)
                if col_index(cell_index) not in cols
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.SWORDFISH,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[
                        f"col{cols[0] + 1}",
                        f"col{cols[1] + 1}",
                        f"col{cols[2] + 1}",
                    ],
                    rationale=(
                        f"Digit {digit} forms a swordfish on columns "
                        f"{cols[0] + 1}, {cols[1] + 1}, and {cols[2] + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
