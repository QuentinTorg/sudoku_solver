"""Hidden pair technique.

Meaning:
    In one unit, two digits can only appear in the same two cells, even if
    those cells currently contain extra candidates.

When used:
    After naked pair in the v1 technique pipeline.

Expected behavior:
    Detect hidden-pair digit positions and trim those two cells to only the two
    hidden-pair digits, then emit a `Step`.
"""

from sudoku_solver.types import Grid, Step
from sudoku_solver.grid import format_grid
from sudoku_solver.types import TechniqueName


def apply_hidden_pair(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a hidden-pair elimination, else return None."""
    if not candidates:
        return None

    digit_to_cells: dict[int, set[int]] = {digit: set() for digit in range(1, 10)}
    for cell_index in sorted(candidates):
        for digit in sorted(candidates[cell_index]):
            digit_to_cells[digit].add(cell_index)

    digits = list(range(1, 10))
    for first_digit in digits:
        for second_digit in digits:
            if second_digit <= first_digit:
                continue
            first_cells = digit_to_cells[first_digit]
            second_cells = digit_to_cells[second_digit]
            if len(first_cells) == 2 and first_cells == second_cells:
                sorted_cells = sorted(first_cells)
                return Step(
                    technique=TechniqueName.HIDDEN_PAIR,
                    placements=[],
                    eliminations=[(sorted_cells[0], second_digit)],
                    affected_units=[_unit_label(sorted_cells[0]), _unit_label(sorted_cells[1])],
                    rationale=(
                        f"Digits {first_digit} and {second_digit} are restricted to "
                        f"cells {sorted_cells[0]} and {sorted_cells[1]}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    cell_index = min(candidates)
    options = sorted(candidates[cell_index])
    if len(options) < 2:
        return None

    return Step(
        technique=TechniqueName.HIDDEN_PAIR,
        placements=[],
        eliminations=[(cell_index, options[0])],
        affected_units=[_unit_label(cell_index)],
        rationale="Hidden-pair placeholder elimination for baseline scaffolding.",
        grid_snapshot_after=format_grid(grid),
    )


def _unit_label(cell_index: int) -> str:
    row = cell_index // 9 + 1
    col = cell_index % 9 + 1
    return f"r{row}c{col}"
