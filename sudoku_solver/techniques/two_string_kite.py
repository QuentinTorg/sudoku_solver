"""Two-String Kite technique skeleton.

Meaning:
    One strong row link and one strong column link for a digit intersect to force
    eliminations at cells that see both opposite endpoints.

When used:
    As an advanced single-digit chain technique on stalled boards.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_index, col_cells, peers, row_cells


def apply_two_string_kite(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a two-string-kite elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        row_links: list[tuple[int, int, int]] = []
        for row in range(9):
            positions = [
                cell_index
                for cell_index in row_cells(row)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) == 2:
                row_links.append((row, positions[0], positions[1]))

        col_links: list[tuple[int, int, int]] = []
        for col in range(9):
            positions = [
                cell_index
                for cell_index in col_cells(col)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) == 2:
                col_links.append((col, positions[0], positions[1]))

        for row, first_row_end, second_row_end in row_links:
            for col, first_col_end, second_col_end in col_links:
                row_ends = (first_row_end, second_row_end)
                col_ends = (first_col_end, second_col_end)
                for row_end in row_ends:
                    for col_end in col_ends:
                        if row_end == col_end:
                            continue
                        if box_index(row_end) != box_index(col_end):
                            continue

                        other_row_end = (
                            second_row_end if row_end == first_row_end else first_row_end
                        )
                        other_col_end = (
                            second_col_end if col_end == first_col_end else first_col_end
                        )
                        if other_row_end == other_col_end:
                            continue

                        eliminations = [
                            (cell_index, digit)
                            for cell_index in sorted(peers(other_row_end) & peers(other_col_end))
                            if cell_index not in {row_end, col_end, other_row_end, other_col_end}
                            and cell_index in candidates
                            and digit in candidates[cell_index]
                        ]
                        if eliminations:
                            return Step(
                                technique=TechniqueName.TWO_STRING_KITE,
                                placements=[],
                                eliminations=eliminations,
                                affected_units=[f"row{row + 1}", f"col{col + 1}"],
                                rationale=(
                                    f"Digit {digit} forms a two-string kite on row {row + 1} "
                                    f"and column {col + 1}."
                                ),
                                grid_snapshot_after=format_grid(grid),
                            )

    return None
