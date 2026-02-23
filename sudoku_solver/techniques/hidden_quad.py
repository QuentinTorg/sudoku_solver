"""Hidden quad technique.

Meaning:
    Four digits in a unit can only appear in the same four cells, so those
    cells can drop other candidate digits.

When used:
    After hidden triple if extra unit-level reduction is possible.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units


def apply_hidden_quad(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a hidden-quad elimination, else return None."""
    if not candidates:
        return None

    for unit_name, unit_cells in all_units():
        unit_candidate_cells = [cell_index for cell_index in unit_cells if cell_index in candidates]
        if len(unit_candidate_cells) < 4:
            continue

        digit_to_cells: dict[int, set[int]] = {
            digit: {
                cell_index for cell_index in unit_candidate_cells if digit in candidates[cell_index]
            }
            for digit in range(1, 10)
        }

        for quad_digits in combinations(range(1, 10), 4):
            if any(len(digit_to_cells[digit]) == 0 for digit in quad_digits):
                continue

            positions = set().union(*(digit_to_cells[digit] for digit in quad_digits))
            if len(positions) != 4:
                continue

            quad_digit_set = set(quad_digits)
            eliminations: list[tuple[int, int]] = []
            for cell_index in sorted(positions):
                for digit in sorted(candidates[cell_index]):
                    if digit not in quad_digit_set:
                        eliminations.append((cell_index, digit))

            if eliminations:
                return Step(
                    technique=TechniqueName.HIDDEN_QUAD,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[unit_name],
                    rationale=(f"Digits {quad_digits} form hidden quad in {unit_name}."),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
