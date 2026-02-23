"""Unique Rectangle technique skeleton.

Meaning:
    A near-rectangle with two digits would create multiple solutions unless extra
    candidates are removed from one corner.

When used:
    On harder stalled states to avoid deadly-pattern ambiguity.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_unique_rectangle(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a unique-rectangle elimination, else return None."""
    if not candidates:
        return None

    for first_row, second_row in combinations(range(9), 2):
        for first_col, second_col in combinations(range(9), 2):
            corners = [
                first_row * 9 + first_col,
                first_row * 9 + second_col,
                second_row * 9 + first_col,
                second_row * 9 + second_col,
            ]
            if any(cell_index not in candidates for cell_index in corners):
                continue

            corner_sets = [set(candidates[cell_index]) for cell_index in corners]
            common = set.intersection(*corner_sets)
            if len(common) < 2:
                continue

            box_counts: dict[int, int] = {}
            for cell_index in corners:
                box = ((cell_index // 9) // 3) * 3 + ((cell_index % 9) // 3)
                box_counts[box] = box_counts.get(box, 0) + 1
            # Type-1 unique rectangle logic is reliable when corners lie in two boxes.
            if len(box_counts) != 2 or sorted(box_counts.values()) != [2, 2]:
                continue

            for pair in combinations(sorted(common), 2):
                pair_set = set(pair)
                if not all(pair_set.issubset(options) for options in corner_sets):
                    continue

                # Type-1 UR: exactly three corners are the pure pair, one has extras.
                pure_pair_count = sum(1 for options in corner_sets if options == pair_set)
                if pure_pair_count != 3:
                    continue

                extras = [
                    options - pair_set if options != pair_set else set() for options in corner_sets
                ]
                extra_indices = [index for index, extra in enumerate(extras) if extra]
                if len(extra_indices) != 1:
                    continue

                target_corner = corners[extra_indices[0]]
                eliminations = [
                    (target_corner, digit) for digit in sorted(extras[extra_indices[0]])
                ]
                if not eliminations:
                    continue

                return Step(
                    technique=TechniqueName.UNIQUE_RECTANGLE,
                    placements=[],
                    eliminations=eliminations,
                    affected_units=[
                        f"row{first_row + 1}",
                        f"row{second_row + 1}",
                        f"col{first_col + 1}",
                        f"col{second_col + 1}",
                    ],
                    rationale=(
                        "Unique Rectangle pattern removes extra candidates "
                        f"from cell {target_corner}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
