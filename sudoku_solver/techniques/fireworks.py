"""Fireworks technique (restricted implementation).

Meaning:
    A pivot and two conjugate-style links can force eliminations on a shared
    digit from cells that see the two remote endpoints.

When used:
    On expert stalled grids with strong-link intersections.
"""

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import col_cells, peers, row_cells


def apply_fireworks(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply expanded-but-safe fireworks elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        for pivot, pivot_options in sorted(candidates.items()):
            if digit not in pivot_options:
                continue

            pivot_row = pivot // 9
            pivot_col = pivot % 9

            row_positions = [
                cell_index
                for cell_index in row_cells(pivot_row)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            col_positions = [
                cell_index
                for cell_index in col_cells(pivot_col)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(row_positions) != 2 or len(col_positions) != 2:
                continue
            if pivot not in row_positions or pivot not in col_positions:
                continue

            row_remote = next(cell_index for cell_index in row_positions if cell_index != pivot)
            col_remote = next(cell_index for cell_index in col_positions if cell_index != pivot)

            legacy_eliminations = [
                (cell_index, digit)
                for cell_index in sorted(peers(row_remote) & peers(col_remote))
                if cell_index not in {pivot, row_remote, col_remote}
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            conservative_eliminations = [
                (cell_index, digit)
                for cell_index, options in sorted(candidates.items())
                if cell_index not in {pivot, row_remote, col_remote}
                and digit in options
                and cell_index in peers(pivot)
                and (cell_index in peers(row_remote) or cell_index in peers(col_remote))
            ]
            eliminations = sorted(set(legacy_eliminations + conservative_eliminations))
            if eliminations:
                return Step(
                    technique=TechniqueName.FIREWORKS,
                    placements=[],
                    eliminations=eliminations,
                    affected_units=[f"row{pivot_row + 1}", f"col{pivot_col + 1}"],
                    rationale=(
                        f"Fireworks pivot {pivot} with digit {digit} "
                        f"eliminates from compatible remote-peer interactions."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
