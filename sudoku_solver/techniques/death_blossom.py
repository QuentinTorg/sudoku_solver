"""Death Blossom technique (restricted implementation).

Meaning:
    A stem cell links to multiple petals; petal interactions can eliminate a
    shared external digit.

When used:
    On expert stalled grids with dense bivalue neighborhoods.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import peers


def apply_death_blossom(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted death-blossom elimination, else return None."""
    if not candidates:
        return None

    for stem_cell, stem_options in sorted(candidates.items()):
        if len(stem_options) < 2:
            continue

        petal_cells = [
            cell_index
            for cell_index in sorted(peers(stem_cell))
            if cell_index in candidates and len(candidates[cell_index]) == 2
        ]
        for first_petal, second_petal in combinations(petal_cells, 2):
            first_options = candidates[first_petal]
            second_options = candidates[second_petal]

            first_stem_digits = stem_options & first_options
            second_stem_digits = stem_options & second_options
            if len(first_stem_digits) != 1 or len(second_stem_digits) != 1:
                continue
            if first_stem_digits == second_stem_digits:
                continue

            first_external = first_options - first_stem_digits
            second_external = second_options - second_stem_digits
            if len(first_external) != 1 or len(second_external) != 1:
                continue
            if first_external != second_external:
                continue
            shared_external = next(iter(first_external))

            eliminations = [
                (cell_index, shared_external)
                for cell_index in sorted(peers(first_petal) & peers(second_petal))
                if cell_index not in {stem_cell, first_petal, second_petal}
                and cell_index in candidates
                and shared_external in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.DEATH_BLOSSOM,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[],
                    rationale=(
                        f"Death Blossom stem {stem_cell} with petals {first_petal}/{second_petal} "
                        f"eliminates digit {shared_external}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
