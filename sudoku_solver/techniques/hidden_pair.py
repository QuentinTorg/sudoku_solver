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
from sudoku_solver.units import all_units


def apply_hidden_pair(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a hidden-pair elimination, else return None."""
    if not candidates:
        return None

    for unit_name, unit_cells in all_units():
        digit_to_cells: dict[int, set[int]] = {digit: set() for digit in range(1, 10)}
        for cell_index in unit_cells:
            if cell_index not in candidates:
                continue
            for digit in candidates[cell_index]:
                digit_to_cells[digit].add(cell_index)

        for first_digit in range(1, 10):
            for second_digit in range(first_digit + 1, 10):
                first_cells = digit_to_cells[first_digit]
                second_cells = digit_to_cells[second_digit]
                if len(first_cells) != 2 or first_cells != second_cells:
                    continue

                pair_cells = sorted(first_cells)
                allowed = {first_digit, second_digit}
                eliminations: list[tuple[int, int]] = []
                for cell_index in pair_cells:
                    for digit in sorted(candidates[cell_index]):
                        if digit not in allowed:
                            eliminations.append((cell_index, digit))

                if eliminations:
                    return Step(
                        technique=TechniqueName.HIDDEN_PAIR,
                        placements=[],
                        eliminations=sorted(eliminations),
                        affected_units=[unit_name],
                        rationale=(
                            f"Digits {first_digit} and {second_digit} are restricted to "
                            f"cells {pair_cells[0]} and {pair_cells[1]} in {unit_name}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

    return None
