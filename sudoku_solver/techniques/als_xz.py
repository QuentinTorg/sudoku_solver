"""ALS-XZ technique (restricted implementation).

Meaning:
    Two almost-locked sets (ALS) with a restricted common candidate can force
    eliminations of another shared candidate.

When used:
    On advanced stalled grids after chain and fish techniques.
"""

from dataclasses import dataclass
from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units, peers


@dataclass(slots=True, frozen=True)
class _Als:
    cells: tuple[int, ...]
    digits: frozenset[int]
    unit_name: str


def apply_als_xz(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted ALS-XZ elimination, else return None."""
    if not candidates:
        return None

    all_als = _find_als(candidates)
    for first_als, second_als in combinations(all_als, 2):
        if set(first_als.cells) & set(second_als.cells):
            continue

        shared_digits = sorted(first_als.digits & second_als.digits)
        if len(shared_digits) < 2:
            continue

        for restricted_digit in shared_digits:
            first_restricted_cells = [
                cell_index
                for cell_index in first_als.cells
                if restricted_digit in candidates[cell_index]
            ]
            second_restricted_cells = [
                cell_index
                for cell_index in second_als.cells
                if restricted_digit in candidates[cell_index]
            ]
            if len(first_restricted_cells) != 1 or len(second_restricted_cells) != 1:
                continue
            if second_restricted_cells[0] not in peers(first_restricted_cells[0]):
                continue

            for target_digit in shared_digits:
                if target_digit == restricted_digit:
                    continue
                eliminations = _target_digit_eliminations(
                    candidates,
                    first_als,
                    second_als,
                    target_digit,
                )
                if eliminations:
                    return Step(
                        technique=TechniqueName.ALS_XZ,
                        placements=[],
                        eliminations=eliminations,
                        affected_units=[first_als.unit_name, second_als.unit_name],
                        rationale=(
                            f"ALS-XZ with restricted digit {restricted_digit} "
                            f"eliminates digit {target_digit}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

    return None


def _find_als(candidates: dict[int, set[int]]) -> list[_Als]:
    results: list[_Als] = []
    for unit_name, unit_cells in all_units():
        unsolved = [cell_index for cell_index in unit_cells if cell_index in candidates]
        for size in (2, 3):
            if len(unsolved) < size:
                continue
            for subset in combinations(unsolved, size):
                digit_union = set().union(*(candidates[cell_index] for cell_index in subset))
                if len(digit_union) != size + 1:
                    continue
                results.append(
                    _Als(
                        cells=tuple(sorted(subset)),
                        digits=frozenset(digit_union),
                        unit_name=unit_name,
                    )
                )
    return results


def _target_digit_eliminations(
    candidates: dict[int, set[int]],
    first_als: _Als,
    second_als: _Als,
    target_digit: int,
) -> list[tuple[int, int]]:
    first_target_cells = [
        cell_index for cell_index in first_als.cells if target_digit in candidates[cell_index]
    ]
    second_target_cells = [
        cell_index for cell_index in second_als.cells if target_digit in candidates[cell_index]
    ]
    if not first_target_cells or not second_target_cells:
        return []

    eliminations: list[tuple[int, int]] = []
    blocked = set(first_als.cells) | set(second_als.cells)
    for cell_index, options in candidates.items():
        if cell_index in blocked or target_digit not in options:
            continue
        if not all(source in peers(cell_index) for source in first_target_cells):
            continue
        if not all(source in peers(cell_index) for source in second_target_cells):
            continue
        eliminations.append((cell_index, target_digit))
    return sorted(eliminations)
