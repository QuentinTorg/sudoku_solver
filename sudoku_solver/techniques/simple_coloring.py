"""Simple Coloring technique.

Meaning:
    For one digit, conjugate (strong) links form colored chains. Eliminations
    follow from color-trap/wrap contradictions.

When used:
    On harder stalled grids after wing/fish techniques.
"""

from sudoku_solver.engines.chain_engine import find_coloring_eliminations
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_simple_coloring(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply simple-coloring elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        eliminations = find_coloring_eliminations(
            candidates,
            digit,
            require_loop_component=False,
        )
        if not eliminations:
            continue
        return Step(
            technique=TechniqueName.SIMPLE_COLORING,
            placements=[],
            eliminations=eliminations,
            affected_units=[],
            rationale=f"Simple coloring on digit {digit} produced eliminations.",
            grid_snapshot_after=format_grid(grid),
        )

    return None
