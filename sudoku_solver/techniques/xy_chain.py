"""XY-Chain technique.

Meaning:
    A chain of bivalue cells with alternating shared digits can force
    eliminations of an endpoint-shared digit.

When used:
    On advanced stalled grids after XY/XYZ-Wing level techniques.
"""

from sudoku_solver.engines.chain_engine import bivalue_cells, shared_single_candidate
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import peers

MAX_CHAIN_LENGTH = 7


def apply_xy_chain(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an XY-Chain elimination, else return None."""
    if not candidates:
        return None

    for start in bivalue_cells(candidates):
        start_digits = candidates[start]
        for target_digit in sorted(start_digits):
            for next_cell in sorted(peers(start)):
                if next_cell not in candidates or len(candidates[next_cell]) != 2:
                    continue

                first_link_digit = shared_single_candidate(candidates, start, next_cell)
                if first_link_digit is None or first_link_digit == target_digit:
                    continue

                step = _search_chain(
                    grid,
                    candidates,
                    start,
                    next_cell,
                    target_digit,
                    first_link_digit,
                    path=[start, next_cell],
                )
                if step is not None:
                    return step

    return None


def _search_chain(
    grid: Grid,
    candidates: dict[int, set[int]],
    start: int,
    current: int,
    target_digit: int,
    previous_link_digit: int,
    *,
    path: list[int],
) -> Step | None:
    current_options = candidates[current]

    if (
        len(path) >= 3
        and target_digit in current_options
        and previous_link_digit != target_digit
        and current in peers(start)
    ):
        eliminations = [
            (cell_index, target_digit)
            for cell_index in sorted(peers(start) & peers(current))
            if cell_index not in path
            and cell_index in candidates
            and target_digit in candidates[cell_index]
        ]
        if eliminations:
            return Step(
                technique=TechniqueName.XY_CHAIN,
                placements=[],
                eliminations=eliminations,
                affected_units=[],
                rationale=(
                    f"XY-Chain {path} links endpoint digit {target_digit} and "
                    "eliminates from common peers."
                ),
                grid_snapshot_after=format_grid(grid),
            )

    if len(path) >= MAX_CHAIN_LENGTH:
        return None

    for next_cell in sorted(peers(current)):
        if next_cell in path:
            continue
        if next_cell not in candidates or len(candidates[next_cell]) != 2:
            continue

        link_digit = shared_single_candidate(candidates, current, next_cell)
        if link_digit is None or link_digit == previous_link_digit:
            continue

        step = _search_chain(
            grid,
            candidates,
            start,
            next_cell,
            target_digit,
            link_digit,
            path=path + [next_cell],
        )
        if step is not None:
            return step

    return None
