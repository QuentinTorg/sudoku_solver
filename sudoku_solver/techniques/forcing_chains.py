"""Forcing Chains / Nets technique (restricted implementation).

Meaning:
    Assume each candidate of a pivot cell in turn and propagate forced singles.
    If all branches agree on a placement/elimination, or one branch contradicts,
    that consequence is logically forced.

When used:
    On expert stalled grids when direct chain/fish/ALS rules make no progress.
"""

from sudoku_solver.engines.chain_engine import find_forcing_chains_consequence
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_forcing_chains(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a restricted forcing-chain/net consequence, else return None."""
    consequence = find_forcing_chains_consequence(grid, candidates)
    if consequence is None:
        return None

    return Step(
        technique=TechniqueName.FORCING_CHAINS,
        placements=list(consequence.placements),
        eliminations=list(consequence.eliminations),
        affected_units=[],
        rationale=consequence.reason,
        grid_snapshot_after=format_grid(grid),
    )
