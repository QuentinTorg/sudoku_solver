"""Death Blossom technique (restricted implementation).

Meaning:
    A stem cell links to multiple petals; petal interactions can eliminate a
    shared external digit.

When used:
    On expert stalled grids with dense bivalue neighborhoods.
"""

from sudoku_solver.engines.als_engine import find_death_blossom_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_death_blossom(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted death-blossom elimination, else return None."""
    if not candidates:
        return None

    elimination = find_death_blossom_elimination(candidates)
    if elimination is None:
        return None

    return Step(
        technique=TechniqueName.DEATH_BLOSSOM,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=[],
        rationale=(
            f"Death Blossom stem {elimination.stem_cell} with petals "
            f"{elimination.first_petal}/{elimination.second_petal} eliminates "
            f"digit {elimination.target_digit}."
        ),
        grid_snapshot_after=format_grid(grid),
    )
