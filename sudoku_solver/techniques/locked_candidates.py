"""Locked candidates (pointing/claiming) technique.

Meaning:
    Candidate positions for a digit are confined to an intersection between
    units (box+row or box+column).

When used:
    After direct placements (naked/hidden single) stop producing moves.

Expected behavior:
    Detect locked patterns and eliminate the locked digit from intersecting peer
    cells outside the locked segment, then emit a `Step`.
"""

from sudoku_solver.types import Grid, Step
from sudoku_solver.grid import format_grid
from sudoku_solver.types import TechniqueName


def apply_locked_candidates(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a locked-candidates elimination, else return None."""
    if not candidates:
        return None

    cell_index = min(candidates)
    options = sorted(candidates[cell_index])
    if not options:
        return None

    digit = options[0]
    return Step(
        technique=TechniqueName.LOCKED_CANDIDATES,
        placements=[],
        eliminations=[(cell_index, digit)],
        affected_units=[_unit_label(cell_index)],
        rationale="Locked-candidates placeholder elimination for baseline scaffolding.",
        grid_snapshot_after=format_grid(grid),
    )


def _unit_label(cell_index: int) -> str:
    row = cell_index // 9 + 1
    col = cell_index % 9 + 1
    return f"r{row}c{col}"
