"""Sue de Coq technique (restricted implementation).

Meaning:
    Candidates in a box-line intersection can be split into disjoint row/box
    subsets, enabling eliminations outside those subsets.

When used:
    On advanced stalled grids with dense intersection candidates.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_cells, box_index, col_cells, col_index, row_cells, row_index


def apply_sue_de_coq(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted Sue de Coq elimination, else return None."""
    if not candidates:
        return None

    for box in range(9):
        step = _scan_box_row_intersections(grid, candidates, box)
        if step is not None:
            return step
        step = _scan_box_col_intersections(grid, candidates, box)
        if step is not None:
            return step

    return None


def _scan_box_row_intersections(
    grid: Grid,
    candidates: dict[int, set[int]],
    box: int,
) -> Step | None:
    rows = sorted({row_index(cell_index) for cell_index in box_cells(box)})
    for row in rows:
        intersection = [
            cell_index
            for cell_index in box_cells(box)
            if row_index(cell_index) == row and cell_index in candidates
        ]
        step = _sue_de_coq_on_intersection(
            grid,
            candidates,
            box,
            row,
            intersection,
            line_cells=row_cells(row),
            line_unit=f"row{row + 1}",
            box_unit=f"box{box + 1}",
            line_axis="row",
        )
        if step is not None:
            return step
    return None


def _scan_box_col_intersections(
    grid: Grid,
    candidates: dict[int, set[int]],
    box: int,
) -> Step | None:
    cols = sorted({col_index(cell_index) for cell_index in box_cells(box)})
    for col in cols:
        intersection = [
            cell_index
            for cell_index in box_cells(box)
            if col_index(cell_index) == col and cell_index in candidates
        ]
        step = _sue_de_coq_on_intersection(
            grid,
            candidates,
            box,
            col,
            intersection,
            line_cells=col_cells(col),
            line_unit=f"col{col + 1}",
            box_unit=f"box{box + 1}",
            line_axis="col",
        )
        if step is not None:
            return step
    return None


def _sue_de_coq_on_intersection(
    grid: Grid,
    candidates: dict[int, set[int]],
    box: int,
    line_index: int,
    intersection: list[int],
    *,
    line_cells: list[int],
    line_unit: str,
    box_unit: str,
    line_axis: str,
) -> Step | None:
    if len(intersection) != 2:
        return None

    intersection_digits = set().union(*(candidates[cell_index] for cell_index in intersection))
    if len(intersection_digits) != 4:
        return None

    line_only_cells = [
        cell_index
        for cell_index in line_cells
        if box_index(cell_index) != box and cell_index in candidates
    ]
    box_only_cells = [
        cell_index
        for cell_index in box_cells(box)
        if (
            (
                row_index(cell_index) != line_index
                if line_axis == "row"
                else col_index(cell_index) != line_index
            )
            and cell_index in candidates
        )
    ]
    if not line_only_cells or not box_only_cells:
        return None

    for line_digits_tuple in combinations(sorted(intersection_digits), 2):
        line_digits = set(line_digits_tuple)
        box_digits = intersection_digits - line_digits

        line_subset = _find_subset_cover(line_only_cells, candidates, line_digits)
        if line_subset is None:
            continue
        box_subset = _find_subset_cover(box_only_cells, candidates, box_digits)
        if box_subset is None:
            continue

        eliminations: list[tuple[int, int]] = []
        for cell_index in line_only_cells:
            if cell_index in line_subset:
                continue
            for digit in sorted(line_digits):
                if digit in candidates[cell_index]:
                    eliminations.append((cell_index, digit))
        for cell_index in box_only_cells:
            if cell_index in box_subset:
                continue
            for digit in sorted(box_digits):
                if digit in candidates[cell_index]:
                    eliminations.append((cell_index, digit))

        if eliminations:
            return Step(
                technique=TechniqueName.SUE_DE_COQ,
                placements=[],
                eliminations=sorted(set(eliminations)),
                affected_units=[line_unit, box_unit],
                rationale=(
                    f"Sue de Coq split in {box_unit}/{line_unit} intersection "
                    f"with digits {sorted(intersection_digits)}."
                ),
                grid_snapshot_after=format_grid(grid),
            )

    return None


def _find_subset_cover(
    source_cells: list[int],
    candidates: dict[int, set[int]],
    required_digits: set[int],
) -> set[int] | None:
    eligible = [
        cell_index
        for cell_index in source_cells
        if candidates[cell_index].issubset(required_digits) and candidates[cell_index]
    ]
    for size in (1, 2):
        if len(eligible) < size:
            continue
        for subset in combinations(eligible, size):
            union = set().union(*(candidates[cell_index] for cell_index in subset))
            if union == required_digits:
                return set(subset)
    return None
