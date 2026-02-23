"""Exocet technique (restricted aligned pattern).

Meaning:
    A base/target structure can constrain two digits to specific target cells.
    This restricted implementation detects aligned row- or column-based variants.

When used:
    On very hard stalled puzzles with strong structural symmetry.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_index, col_cells, col_index, row_cells, row_index


def apply_exocet(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted aligned exocet elimination, else return None."""
    if not candidates:
        return None

    bivalue_cells = [
        cell_index for cell_index in sorted(candidates) if len(candidates[cell_index]) == 2
    ]
    for first_base, second_base in combinations(bivalue_cells, 2):
        base_digits = candidates[first_base]
        if candidates[second_base] != base_digits:
            continue
        if box_index(first_base) != box_index(second_base):
            continue

        row_result = _row_oriented_exocet(candidates, first_base, second_base, base_digits)
        if row_result is not None:
            base_row, target_row, target_first, target_second, eliminations = row_result
            return Step(
                technique=TechniqueName.EXOCET,
                placements=[],
                eliminations=sorted(set(eliminations)),
                affected_units=[f"row{base_row + 1}", f"row{target_row + 1}"],
                rationale=(
                    f"Row-oriented restricted exocet base ({first_base}, {second_base}) and "
                    f"targets ({target_first}, {target_second}) constrain digits."
                ),
                grid_snapshot_after=format_grid(grid),
            )

        col_result = _col_oriented_exocet(candidates, first_base, second_base, base_digits)
        if col_result is not None:
            base_col, target_col, target_first, target_second, eliminations = col_result
            return Step(
                technique=TechniqueName.EXOCET,
                placements=[],
                eliminations=sorted(set(eliminations)),
                affected_units=[f"col{base_col + 1}", f"col{target_col + 1}"],
                rationale=(
                    f"Column-oriented restricted exocet base ({first_base}, {second_base}) and "
                    f"targets ({target_first}, {target_second}) constrain digits."
                ),
                grid_snapshot_after=format_grid(grid),
            )

    return None


def _row_oriented_exocet(
    candidates: dict[int, set[int]],
    first_base: int,
    second_base: int,
    base_digits: set[int],
) -> tuple[int, int, int, int, list[tuple[int, int]]] | None:
    if row_index(first_base) != row_index(second_base):
        return None

    first_col = col_index(first_base)
    second_col = col_index(second_base)
    base_row = row_index(first_base)
    target_rows = [
        row
        for row in range(9)
        if row != base_row
        and row * 9 + first_col in candidates
        and row * 9 + second_col in candidates
        and base_digits.issubset(candidates[row * 9 + first_col])
        and base_digits.issubset(candidates[row * 9 + second_col])
    ]
    for target_row in target_rows:
        target_first = target_row * 9 + first_col
        target_second = target_row * 9 + second_col
        eliminations: list[tuple[int, int]] = []
        for digit in sorted(base_digits):
            for cell_index in col_cells(first_col):
                if row_index(cell_index) in {base_row, target_row}:
                    continue
                if cell_index in candidates and digit in candidates[cell_index]:
                    eliminations.append((cell_index, digit))
            for cell_index in col_cells(second_col):
                if row_index(cell_index) in {base_row, target_row}:
                    continue
                if cell_index in candidates and digit in candidates[cell_index]:
                    eliminations.append((cell_index, digit))
        if eliminations:
            return base_row, target_row, target_first, target_second, eliminations
    return None


def _col_oriented_exocet(
    candidates: dict[int, set[int]],
    first_base: int,
    second_base: int,
    base_digits: set[int],
) -> tuple[int, int, int, int, list[tuple[int, int]]] | None:
    if col_index(first_base) != col_index(second_base):
        return None

    first_row = row_index(first_base)
    second_row = row_index(second_base)
    base_col = col_index(first_base)
    target_cols = [
        col
        for col in range(9)
        if col != base_col
        and first_row * 9 + col in candidates
        and second_row * 9 + col in candidates
        and base_digits.issubset(candidates[first_row * 9 + col])
        and base_digits.issubset(candidates[second_row * 9 + col])
    ]
    for target_col in target_cols:
        target_first = first_row * 9 + target_col
        target_second = second_row * 9 + target_col
        eliminations: list[tuple[int, int]] = []
        for digit in sorted(base_digits):
            for cell_index in row_cells(first_row):
                if col_index(cell_index) in {base_col, target_col}:
                    continue
                if cell_index in candidates and digit in candidates[cell_index]:
                    eliminations.append((cell_index, digit))
            for cell_index in row_cells(second_row):
                if col_index(cell_index) in {base_col, target_col}:
                    continue
                if cell_index in candidates and digit in candidates[cell_index]:
                    eliminations.append((cell_index, digit))
        if eliminations:
            return base_col, target_col, target_first, target_second, eliminations
    return None
