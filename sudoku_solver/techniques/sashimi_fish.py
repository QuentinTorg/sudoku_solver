"""Sashimi Fish technique (expanded implementation).

Meaning:
    Sashimi fish variants extend finned fish logic for additional eliminations.
    The expanded implementation uses finned fish first, then scans generalized
    under-populated base-line fish shapes that are compatible with sashimi.

When used:
    On expert stalled grids after standard/finned fish passes.
"""

from sudoku_solver.engines.fish_engine import (
    FishElimination,
    find_finned_swordfish_elimination,
    find_finned_x_wing_elimination,
    find_standard_fish_elimination,
)
from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import col_cells, row_cells


def apply_sashimi_fish(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply an expanded sashimi-fish elimination, else return None."""
    for digit in range(1, 10):
        for fish in (
            find_finned_swordfish_elimination(candidates, digit),
            find_finned_x_wing_elimination(candidates, digit),
        ):
            if fish is None:
                continue
            return Step(
                technique=TechniqueName.SASHIMI_FISH,
                placements=[],
                eliminations=list(fish.eliminations),
                affected_units=list(fish.affected_units),
                rationale=("Sashimi fish (expanded) found a finned-fish-compatible elimination."),
                grid_snapshot_after=format_grid(grid),
            )
        underpopulated_x_wing = _find_underpopulated_x_wing(candidates, digit)
        if underpopulated_x_wing is not None:
            return Step(
                technique=TechniqueName.SASHIMI_FISH,
                placements=[],
                eliminations=list(underpopulated_x_wing.eliminations),
                affected_units=list(underpopulated_x_wing.affected_units),
                rationale=(
                    "Sashimi fish (expanded) found an under-populated base-line fish elimination."
                ),
                grid_snapshot_after=format_grid(grid),
            )

        for size in (3,):
            fish = find_standard_fish_elimination(
                candidates,
                digit,
                size=size,
                exact_line_size=False,
            )
            if fish is None or not _is_sashimi_like_base(candidates, digit, fish, size=size):
                continue
            return Step(
                technique=TechniqueName.SASHIMI_FISH,
                placements=[],
                eliminations=list(fish.eliminations),
                affected_units=list(fish.affected_units),
                rationale=(
                    "Sashimi fish (expanded) found an under-populated base-line fish elimination."
                ),
                grid_snapshot_after=format_grid(grid),
            )
    return None


def _is_sashimi_like_base(
    candidates: dict[int, set[int]],
    digit: int,
    fish: FishElimination,
    *,
    size: int,
) -> bool:
    """Return True when a base line has fewer than fish-size candidates."""
    for base in fish.base_units:
        if fish.orientation == "row":
            count = sum(
                1
                for cell_index in row_cells(base)
                if cell_index in candidates and digit in candidates[cell_index]
            )
        else:
            count = sum(
                1
                for cell_index in col_cells(base)
                if cell_index in candidates and digit in candidates[cell_index]
            )
        if count < size:
            return True

    return False


def _find_underpopulated_x_wing(
    candidates: dict[int, set[int]],
    digit: int,
) -> FishElimination | None:
    row_positions = {
        row: {
            cell_index % 9
            for cell_index in row_cells(row)
            if cell_index in candidates and digit in candidates[cell_index]
        }
        for row in range(9)
    }
    row_positions = {row: covers for row, covers in row_positions.items() if 1 <= len(covers) <= 2}
    for first_row in sorted(row_positions):
        for second_row in sorted(row_positions):
            if second_row <= first_row:
                continue
            cover_union = row_positions[first_row] | row_positions[second_row]
            if len(cover_union) != 2:
                continue
            counts = (len(row_positions[first_row]), len(row_positions[second_row]))
            if sorted(counts) != [1, 2]:
                continue
            eliminations = [
                (cell_index, digit)
                for cover_col in sorted(cover_union)
                for cell_index in col_cells(cover_col)
                if (cell_index // 9) not in {first_row, second_row}
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return FishElimination(
                    digit=digit,
                    eliminations=tuple(sorted(set(eliminations))),
                    affected_units=(
                        f"row{first_row + 1}",
                        f"row{second_row + 1}",
                        f"col{sorted(cover_union)[0] + 1}",
                        f"col{sorted(cover_union)[1] + 1}",
                    ),
                    orientation="row",
                    base_units=(first_row, second_row),
                )

    col_positions = {
        col: {
            cell_index // 9
            for cell_index in col_cells(col)
            if cell_index in candidates and digit in candidates[cell_index]
        }
        for col in range(9)
    }
    col_positions = {col: covers for col, covers in col_positions.items() if 1 <= len(covers) <= 2}
    for first_col in sorted(col_positions):
        for second_col in sorted(col_positions):
            if second_col <= first_col:
                continue
            cover_union = col_positions[first_col] | col_positions[second_col]
            if len(cover_union) != 2:
                continue
            counts = (len(col_positions[first_col]), len(col_positions[second_col]))
            if sorted(counts) != [1, 2]:
                continue
            eliminations = [
                (cell_index, digit)
                for cover_row in sorted(cover_union)
                for cell_index in row_cells(cover_row)
                if (cell_index % 9) not in {first_col, second_col}
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return FishElimination(
                    digit=digit,
                    eliminations=tuple(sorted(set(eliminations))),
                    affected_units=(
                        f"col{first_col + 1}",
                        f"col{second_col + 1}",
                        f"row{sorted(cover_union)[0] + 1}",
                        f"row{sorted(cover_union)[1] + 1}",
                    ),
                    orientation="col",
                    base_units=(first_col, second_col),
                )

    return None
