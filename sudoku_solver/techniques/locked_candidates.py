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
from sudoku_solver.units import (
    box_cells,
    box_index,
    col_cells,
    col_index,
    row_cells,
    row_index,
)


def apply_locked_candidates(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a locked-candidates elimination, else return None."""
    if not candidates:
        return None

    # Pointing: candidates in a box align to a single row/column.
    for box in range(9):
        box_unit = box_cells(box)
        for digit in range(1, 10):
            positions = [
                cell_index
                for cell_index in box_unit
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) < 2:
                continue

            rows = {row_index(cell_index) for cell_index in positions}
            if len(rows) == 1:
                row = next(iter(rows))
                eliminations = [
                    (cell_index, digit)
                    for cell_index in row_cells(row)
                    if cell_index not in box_unit
                    and cell_index in candidates
                    and digit in candidates[cell_index]
                ]
                if eliminations:
                    return Step(
                        technique=TechniqueName.LOCKED_CANDIDATES,
                        placements=[],
                        eliminations=sorted(eliminations),
                        affected_units=[f"box{box + 1}", f"row{row + 1}"],
                        rationale=(
                            f"Digit {digit} is locked to row {row + 1} within box {box + 1}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

            cols = {col_index(cell_index) for cell_index in positions}
            if len(cols) == 1:
                col = next(iter(cols))
                eliminations = [
                    (cell_index, digit)
                    for cell_index in col_cells(col)
                    if cell_index not in box_unit
                    and cell_index in candidates
                    and digit in candidates[cell_index]
                ]
                if eliminations:
                    return Step(
                        technique=TechniqueName.LOCKED_CANDIDATES,
                        placements=[],
                        eliminations=sorted(eliminations),
                        affected_units=[f"box{box + 1}", f"col{col + 1}"],
                        rationale=(
                            f"Digit {digit} is locked to column {col + 1} within box {box + 1}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

    # Claiming: candidates in row/column align to a single box.
    for row in range(9):
        row_unit = row_cells(row)
        for digit in range(1, 10):
            positions = [
                cell_index
                for cell_index in row_unit
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) < 2:
                continue

            boxes = {box_index(cell_index) for cell_index in positions}
            if len(boxes) == 1:
                box = next(iter(boxes))
                eliminations = [
                    (cell_index, digit)
                    for cell_index in box_cells(box)
                    if cell_index not in row_unit
                    and cell_index in candidates
                    and digit in candidates[cell_index]
                ]
                if eliminations:
                    return Step(
                        technique=TechniqueName.LOCKED_CANDIDATES,
                        placements=[],
                        eliminations=sorted(eliminations),
                        affected_units=[f"row{row + 1}", f"box{box + 1}"],
                        rationale=(
                            f"Digit {digit} in row {row + 1} is confined to box {box + 1}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

    for col in range(9):
        col_unit = col_cells(col)
        for digit in range(1, 10):
            positions = [
                cell_index
                for cell_index in col_unit
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) < 2:
                continue

            boxes = {box_index(cell_index) for cell_index in positions}
            if len(boxes) == 1:
                box = next(iter(boxes))
                eliminations = [
                    (cell_index, digit)
                    for cell_index in box_cells(box)
                    if cell_index not in col_unit
                    and cell_index in candidates
                    and digit in candidates[cell_index]
                ]
                if eliminations:
                    return Step(
                        technique=TechniqueName.LOCKED_CANDIDATES,
                        placements=[],
                        eliminations=sorted(eliminations),
                        affected_units=[f"col{col + 1}", f"box{box + 1}"],
                        rationale=(
                            f"Digit {digit} in column {col + 1} is confined to box {box + 1}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

    return None
