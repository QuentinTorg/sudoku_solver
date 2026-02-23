"""X-Cycles technique (restricted single-digit loops).

Meaning:
    Alternating strong-link cycles for one digit can force eliminations by
    coloring contradictions.

When used:
    On advanced stalled puzzles after fish/wing techniques.
"""

from sudoku_solver.engines.chain_engine import find_coloring_eliminations
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_x_cycles(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted X-Cycles elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        eliminations = find_coloring_eliminations(
            candidates,
            digit,
            require_loop_component=True,
        )
        if not eliminations:
            continue
        return Step(
            technique=TechniqueName.X_CYCLES,
            placements=[],
            eliminations=eliminations,
            affected_units=[],
            rationale=f"X-Cycle loop on digit {digit} produced eliminations.",
            grid_snapshot_after=format_grid(grid),
        )

    return None
