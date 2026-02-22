"""Hidden triple technique skeleton.

Meaning:
    Three digits in a unit can only appear in the same three cells, so those
    cells can drop any other candidate digits.

When used:
    After naked triples if additional unit-level pruning is needed.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units


def apply_hidden_triple(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a hidden-triple elimination, else return None."""
    if not candidates:
        return None

    for unit_name, unit_cells in all_units():
        unit_candidate_cells = [cell_index for cell_index in unit_cells if cell_index in candidates]
        if len(unit_candidate_cells) < 3:
            continue

        digit_to_cells: dict[int, set[int]] = {
            digit: {
                cell_index for cell_index in unit_candidate_cells if digit in candidates[cell_index]
            }
            for digit in range(1, 10)
        }

        for triple_digits in combinations(range(1, 10), 3):
            positions = set().union(*(digit_to_cells[digit] for digit in triple_digits))
            if len(positions) != 3:
                continue
            if any(len(digit_to_cells[digit]) == 0 for digit in triple_digits):
                continue

            triple_digit_set = set(triple_digits)
            eliminations: list[tuple[int, int]] = []
            for cell_index in sorted(positions):
                for digit in sorted(candidates[cell_index]):
                    if digit not in triple_digit_set:
                        eliminations.append((cell_index, digit))

            if eliminations:
                return Step(
                    technique=TechniqueName.HIDDEN_TRIPLE,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[unit_name],
                    rationale=(
                        f"Digits {triple_digits[0]}, {triple_digits[1]}, and {triple_digits[2]} "
                        f"form a hidden triple in {unit_name}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
