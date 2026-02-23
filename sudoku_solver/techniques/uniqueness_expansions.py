"""Uniqueness expansions (restricted UR type-2 style).

Meaning:
    Additional uniqueness patterns beyond base unique rectangle. This restricted
    version targets an UR type-2 style elimination.

When used:
    On harder stalled states to avoid non-unique deadly patterns.
"""

from sudoku_solver.engines.uniqueness_engine import find_uniqueness_expansion_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_uniqueness_expansions(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted uniqueness-expansion elimination, else return None."""
    if not candidates:
        return None

    elimination = find_uniqueness_expansion_elimination(candidates)
    if elimination is None:
        return None

    extra_digit = elimination.eliminations[0][1]
    return Step(
        technique=TechniqueName.UNIQUENESS_EXPANSIONS,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=[],
        rationale=(
            "Uniqueness expansion (restricted UR type-2) "
            f"eliminates extra digit {extra_digit}."
        ),
        grid_snapshot_after=format_grid(grid),
    )
