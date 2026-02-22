"""Skyscraper technique skeleton.

Meaning:
    Two strong links for one digit share a base, and roof cells force eliminations
    from cells that see both roofs.

When used:
    For advanced single-digit chain eliminations after wings/fish.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import col_cells, col_index, peers, row_cells, row_index


def apply_skyscraper(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a skyscraper elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        row_links: list[tuple[int, int, int]] = []
        for row in range(9):
            cols = [
                col_index(cell_index)
                for cell_index in row_cells(row)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(cols) == 2:
                row_links.append((row, cols[0], cols[1]))

        for first_link, second_link in combinations(row_links, 2):
            first_row, first_col_a, first_col_b = first_link
            second_row, second_col_a, second_col_b = second_link
            shared_cols = {first_col_a, first_col_b} & {second_col_a, second_col_b}
            if len(shared_cols) != 1:
                continue
            shared_col = next(iter(shared_cols))
            first_roof_col = first_col_b if first_col_a == shared_col else first_col_a
            second_roof_col = second_col_b if second_col_a == shared_col else second_col_a
            if first_roof_col == second_roof_col:
                continue

            first_roof = first_row * 9 + first_roof_col
            second_roof = second_row * 9 + second_roof_col
            eliminations = [
                (cell_index, digit)
                for cell_index in sorted(peers(first_roof) & peers(second_roof))
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.SKYSCRAPER,
                    placements=[],
                    eliminations=eliminations,
                    affected_units=[f"row{first_row + 1}", f"row{second_row + 1}"],
                    rationale=(
                        f"Digit {digit} forms a skyscraper on rows {first_row + 1} and "
                        f"{second_row + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

        col_links: list[tuple[int, int, int]] = []
        for col in range(9):
            rows = [
                row_index(cell_index)
                for cell_index in col_cells(col)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(rows) == 2:
                col_links.append((col, rows[0], rows[1]))

        for first_link, second_link in combinations(col_links, 2):
            first_col, first_row_a, first_row_b = first_link
            second_col, second_row_a, second_row_b = second_link
            shared_rows = {first_row_a, first_row_b} & {second_row_a, second_row_b}
            if len(shared_rows) != 1:
                continue
            shared_row = next(iter(shared_rows))
            first_roof_row = first_row_b if first_row_a == shared_row else first_row_a
            second_roof_row = second_row_b if second_row_a == shared_row else second_row_a
            if first_roof_row == second_roof_row:
                continue

            first_roof = first_roof_row * 9 + first_col
            second_roof = second_roof_row * 9 + second_col
            eliminations = [
                (cell_index, digit)
                for cell_index in sorted(peers(first_roof) & peers(second_roof))
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.SKYSCRAPER,
                    placements=[],
                    eliminations=eliminations,
                    affected_units=[f"col{first_col + 1}", f"col{second_col + 1}"],
                    rationale=(
                        f"Digit {digit} forms a skyscraper on columns {first_col + 1} and "
                        f"{second_col + 1}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
