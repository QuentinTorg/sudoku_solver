"""AIC technique (restricted alternating inference chain).

Meaning:
    Build alternating strong/weak links across candidate nodes. If a chain
    starts and ends on the same digit with weakly linked endpoints, that digit
    can be eliminated from common peers of the endpoints.

When used:
    On advanced stalled grids after XY-Chain and coloring methods.
"""

from sudoku_solver.engines.chain_engine import find_aic_elimination
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName

MAX_CHAIN_NODES = 8


def apply_aic(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted AIC elimination, else return None."""
    if not candidates:
        return None

    elimination = find_aic_elimination(candidates, max_chain_nodes=MAX_CHAIN_NODES)
    if elimination is None:
        return None

    return Step(
        technique=TechniqueName.AIC,
        placements=[],
        eliminations=list(elimination.eliminations),
        affected_units=[],
        rationale=(
            f"AIC chain on digit {elimination.digit} between cells "
            f"{elimination.start_cell} and {elimination.end_cell} eliminates "
            "from common peers."
        ),
        grid_snapshot_after=format_grid(grid),
    )
