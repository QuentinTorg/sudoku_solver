"""Forcing Nets technique (expanded implementation).

Meaning:
    Assume each candidate of a 2- to 4-candidate pivot cell in turn and
    propagate consequences. Each branch now includes forced singles plus
    lightweight candidate reductions (locked candidates and naked pairs) before
    checking branch contradictions or shared outcomes.

When used:
    On expert stalled grids after direct chain/fish/ALS techniques.
"""

from sudoku_solver.engines.chain_engine import find_forcing_nets_consequence
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName


def apply_forcing_nets(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an expanded forcing-net consequence, else return None."""
    consequence = find_forcing_nets_consequence(grid, candidates)
    if consequence is None:
        return None

    return Step(
        technique=TechniqueName.FORCING_NETS,
        placements=list(consequence.placements),
        eliminations=list(consequence.eliminations),
        affected_units=[],
        rationale=consequence.reason,
        grid_snapshot_after=format_grid(grid),
    )
