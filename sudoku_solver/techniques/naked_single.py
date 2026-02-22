"""Naked single technique.

Meaning:
    A cell has exactly one remaining candidate digit.

When used:
    During each solve pass after candidate computation or candidate elimination.

Expected behavior:
    Find the first unsolved cell (deterministic order) with a one-digit
    candidate set, place that digit, and emit a `Step`.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import cell_label


def apply_naked_single(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a naked single placement, else return None."""
    for cell_index in sorted(candidates):
        options = candidates[cell_index]
        if len(options) != 1:
            continue
        digit = next(iter(options))
        return Step(
            technique=TechniqueName.NAKED_SINGLE,
            placements=[(cell_index, digit)],
            eliminations=[],
            affected_units=[cell_label(cell_index)],
            rationale=f"Cell {cell_index} has a single candidate: {digit}.",
            grid_snapshot_after=format_grid(grid),
        )
    return None
