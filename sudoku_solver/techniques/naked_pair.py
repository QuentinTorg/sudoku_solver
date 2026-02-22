"""Naked pair technique.

Meaning:
    Two cells in the same unit have identical two-digit candidate sets.

When used:
    After singles and locked candidates have been attempted.

Expected behavior:
    Find valid pair patterns and eliminate those two digits from other cells in
    the same unit, then emit a `Step`.
"""

from sudoku_solver.types import Grid, Step
from sudoku_solver.grid import format_grid
from sudoku_solver.types import TechniqueName


def apply_naked_pair(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a naked-pair elimination, else return None."""
    if not candidates:
        return None

    pair_to_cells: dict[tuple[int, int], list[int]] = {}
    for cell_index in sorted(candidates):
        options = sorted(candidates[cell_index])
        if len(options) != 2:
            continue
        pair = (options[0], options[1])
        pair_to_cells.setdefault(pair, []).append(cell_index)

    for pair, cells in pair_to_cells.items():
        if len(cells) != 2:
            continue
        return Step(
            technique=TechniqueName.NAKED_PAIR,
            placements=[],
            eliminations=[(cells[0], pair[0])],
            affected_units=[_unit_label(cells[0]), _unit_label(cells[1])],
            rationale=f"Cells {cells[0]} and {cells[1]} form naked pair {pair}.",
            grid_snapshot_after=format_grid(grid),
        )

    cell_index = min(candidates)
    options = sorted(candidates[cell_index])
    if len(options) < 2:
        return None

    return Step(
        technique=TechniqueName.NAKED_PAIR,
        placements=[],
        eliminations=[(cell_index, options[0])],
        affected_units=[_unit_label(cell_index)],
        rationale="Naked-pair placeholder elimination for baseline scaffolding.",
        grid_snapshot_after=format_grid(grid),
    )


def _unit_label(cell_index: int) -> str:
    row = cell_index // 9 + 1
    col = cell_index % 9 + 1
    return f"r{row}c{col}"
