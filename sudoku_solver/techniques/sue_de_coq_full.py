"""Sue de Coq full/generalized (restricted implementation).

Meaning:
    Generalized box-line intersection decomposition extends basic Sue de Coq.

When used:
    On expert stalled grids with rich intersection candidate sets.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.techniques.sue_de_coq import apply_sue_de_coq
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import box_cells, box_index, row_cells, row_index


def apply_sue_de_coq_full(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply generalized restricted Sue de Coq elimination, else return None."""
    base_step = apply_sue_de_coq(grid, candidates)
    if base_step is not None:
        return Step(
            technique=TechniqueName.SUE_DE_COQ_FULL,
            placements=[],
            eliminations=base_step.eliminations,
            affected_units=base_step.affected_units,
            rationale="Sue de Coq full reused base Sue de Coq elimination.",
            grid_snapshot_after=format_grid(grid),
        )

    # Extra restricted coverage: allow 3-cell intersection in row mode.
    for box in range(9):
        rows = sorted({row_index(cell_index) for cell_index in box_cells(box)})
        for row in rows:
            intersection = [
                cell_index
                for cell_index in box_cells(box)
                if row_index(cell_index) == row and cell_index in candidates
            ]
            if len(intersection) != 3:
                continue

            intersection_digits = set().union(
                *(candidates[cell_index] for cell_index in intersection)
            )
            if len(intersection_digits) != 5:
                continue

            line_only_cells = [
                cell_index
                for cell_index in row_cells(row)
                if box_index(cell_index) != box and cell_index in candidates
            ]
            box_only_cells = [
                cell_index
                for cell_index in box_cells(box)
                if row_index(cell_index) != row and cell_index in candidates
            ]
            if not line_only_cells or not box_only_cells:
                continue

            for line_digits_tuple in combinations(sorted(intersection_digits), 2):
                line_digits = set(line_digits_tuple)
                box_digits = intersection_digits - line_digits
                if len(box_digits) != 3:
                    continue

                line_subset = _find_cover(line_only_cells, candidates, line_digits, max_size=2)
                box_subset = _find_cover(box_only_cells, candidates, box_digits, max_size=3)
                if line_subset is None or box_subset is None:
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
                        technique=TechniqueName.SUE_DE_COQ_FULL,
                        placements=[],
                        eliminations=sorted(set(eliminations)),
                        affected_units=[f"row{row + 1}", f"box{box + 1}"],
                        rationale=(
                            "Generalized Sue de Coq (restricted 3-cell intersection) elimination."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

    return None


def _find_cover(
    source_cells: list[int],
    candidates: dict[int, set[int]],
    required_digits: set[int],
    *,
    max_size: int,
) -> set[int] | None:
    eligible = [
        cell_index
        for cell_index in source_cells
        if candidates[cell_index].issubset(required_digits) and candidates[cell_index]
    ]
    for size in range(1, max_size + 1):
        if len(eligible) < size:
            continue
        for subset in combinations(eligible, size):
            union = set().union(*(candidates[cell_index] for cell_index in subset))
            if union == required_digits:
                return set(subset)
    return None
