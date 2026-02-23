"""Uniqueness expansions (restricted UR type-2 style).

Meaning:
    Additional uniqueness patterns beyond base unique rectangle. This restricted
    version targets an UR type-2 style elimination.

When used:
    On harder stalled states to avoid non-unique deadly patterns.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import peers


def apply_uniqueness_expansions(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted uniqueness-expansion elimination, else return None."""
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

            for pair_digits in combinations(sorted(common), 2):
                pair_set = set(pair_digits)
                if not all(pair_set.issubset(options) for options in corner_sets):
                    continue

                extras = [options - pair_set for options in corner_sets]
                expanded_indices = [index for index, extra in enumerate(extras) if len(extra) == 1]
                if len(expanded_indices) != 2:
                    continue
                if any(index not in expanded_indices and extras[index] for index in range(4)):
                    continue

                first_expanded = corners[expanded_indices[0]]
                second_expanded = corners[expanded_indices[1]]
                if extras[expanded_indices[0]] != extras[expanded_indices[1]]:
                    continue
                extra_digit = next(iter(extras[expanded_indices[0]]))

                if second_expanded not in peers(first_expanded):
                    continue

                eliminations = [
                    (cell_index, extra_digit)
                    for cell_index in sorted(peers(first_expanded) & peers(second_expanded))
                    if cell_index not in corners
                    and cell_index in candidates
                    and extra_digit in candidates[cell_index]
                ]
                if eliminations:
                    return Step(
                        technique=TechniqueName.UNIQUENESS_EXPANSIONS,
                        placements=[],
                        eliminations=sorted(eliminations),
                        affected_units=[],
                        rationale=(
                            "Uniqueness expansion (restricted UR type-2) "
                            f"eliminates extra digit {extra_digit}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

    return None
