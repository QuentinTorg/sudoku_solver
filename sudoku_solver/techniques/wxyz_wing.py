"""WXYZ-Wing technique (restricted implementation).

Meaning:
    Four cells with four combined digits can force elimination of a shared
    restricted candidate from cells seeing all relevant wing cells.

When used:
    On advanced stalled grids after XY/XYZ and chain methods.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import peers


def apply_wxyz_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted WXYZ-Wing elimination, else return None."""
    if not candidates:
        return None

    eligible = [
        cell_index for cell_index in sorted(candidates) if 2 <= len(candidates[cell_index]) <= 4
    ]
    for wing_cells in combinations(eligible, 4):
        union_digits = set().union(*(candidates[cell_index] for cell_index in wing_cells))
        if len(union_digits) != 4:
            continue

        for restricted_digit in sorted(union_digits):
            restricted_holders = [
                cell_index
                for cell_index in wing_cells
                if restricted_digit in candidates[cell_index]
            ]
            if len(restricted_holders) != 3:
                continue

            common_peer_set = set(peers(restricted_holders[0]))
            for holder in restricted_holders[1:]:
                common_peer_set &= peers(holder)
            eliminations = [
                (cell_index, restricted_digit)
                for cell_index in sorted(common_peer_set)
                if cell_index not in wing_cells
                and cell_index in candidates
                and restricted_digit in candidates[cell_index]
            ]
            if eliminations:
                return Step(
                    technique=TechniqueName.WXYZ_WING,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[],
                    rationale=(
                        f"WXYZ-Wing on cells {sorted(wing_cells)} "
                        f"eliminates restricted digit {restricted_digit}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
