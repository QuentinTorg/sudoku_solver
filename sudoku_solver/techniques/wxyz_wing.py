"""WXYZ-Wing technique (expanded implementation).

Meaning:
    Four cells with four combined digits can force elimination of a shared
    candidate from cells seeing all relevant wing cells.
    This implementation supports both:
    - Type 1: exactly one non-restricted digit in the wing
    - Type 2: all wing digits are restricted

When used:
    On advanced stalled grids after XY/XYZ and chain methods.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units, peers


def apply_wxyz_wing(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply expanded WXYZ-Wing elimination, else return None."""
    if not candidates:
        return None

    eligible = [
        cell_index for cell_index in sorted(candidates) if 2 <= len(candidates[cell_index]) <= 4
    ]
    for wing_cells in combinations(eligible, 4):
        union_digits = set().union(*(candidates[cell_index] for cell_index in wing_cells))
        if len(union_digits) != 4:
            continue
        if not _is_two_unit_pattern(wing_cells):
            continue

        holders_by_digit = {
            digit: [cell_index for cell_index in wing_cells if digit in candidates[cell_index]]
            for digit in sorted(union_digits)
        }
        non_restricted_digits = [
            digit
            for digit, holders in holders_by_digit.items()
            if len(holders) >= 2 and not _all_holders_mutually_visible(holders)
        ]

        # Type 1: exactly one non-restricted wing digit.
        if len(non_restricted_digits) == 1:
            target_digit = non_restricted_digits[0]
            holders = holders_by_digit[target_digit]
            eliminations = _eliminations_for_digit(
                candidates,
                wing_cells,
                holders,
                target_digit,
            )
            if eliminations:
                return Step(
                    technique=TechniqueName.WXYZ_WING,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[],
                    rationale=(
                        f"WXYZ-Wing type 1 on cells {sorted(wing_cells)} "
                        f"eliminates non-restricted digit {target_digit}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

        # Type 2: all wing digits are restricted.
        if len(non_restricted_digits) == 0:
            for target_digit in sorted(union_digits):
                holders = holders_by_digit[target_digit]
                if len(holders) < 2:
                    continue
                eliminations = _eliminations_for_digit(
                    candidates,
                    wing_cells,
                    holders,
                    target_digit,
                )
                if eliminations:
                    return Step(
                        technique=TechniqueName.WXYZ_WING,
                        placements=[],
                        eliminations=sorted(eliminations),
                        affected_units=[],
                        rationale=(
                            f"WXYZ-Wing type 2 on cells {sorted(wing_cells)} "
                            f"eliminates restricted digit {target_digit}."
                        ),
                        grid_snapshot_after=format_grid(grid),
                    )

        # Legacy compatibility: retain the previous restricted implementation's
        # 3-holder elimination behavior when generalized forms do not trigger.
        for target_digit in sorted(union_digits):
            holders = holders_by_digit[target_digit]
            if len(holders) != 3:
                continue
            eliminations = _eliminations_for_digit(
                candidates,
                wing_cells,
                holders,
                target_digit,
            )
            if eliminations:
                return Step(
                    technique=TechniqueName.WXYZ_WING,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[],
                    rationale=(
                        f"WXYZ-Wing legacy 3-holder pattern on cells {sorted(wing_cells)} "
                        f"eliminates digit {target_digit}."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None


def _all_holders_mutually_visible(holders: list[int]) -> bool:
    for first, second in combinations(holders, 2):
        if second not in peers(first):
            return False
    return True


def _eliminations_for_digit(
    candidates: dict[int, set[int]],
    wing_cells: tuple[int, int, int, int],
    holders: list[int],
    digit: int,
) -> list[tuple[int, int]]:
    if not holders:
        return []

    common_peer_set = set(peers(holders[0]))
    for holder in holders[1:]:
        common_peer_set &= peers(holder)
    return [
        (cell_index, digit)
        for cell_index in sorted(common_peer_set)
        if cell_index not in wing_cells
        and cell_index in candidates
        and digit in candidates[cell_index]
    ]


def _is_two_unit_pattern(wing_cells: tuple[int, int, int, int]) -> bool:
    wing_set = set(wing_cells)
    unit_map = {name: set(unit_cells) for name, unit_cells in all_units()}
    relevant_units = [name for name, unit_cells in unit_map.items() if wing_set & unit_cells]
    for first_name, second_name in combinations(relevant_units, 2):
        coverage = unit_map[first_name] | unit_map[second_name]
        if wing_set.issubset(coverage):
            return True
    return False
