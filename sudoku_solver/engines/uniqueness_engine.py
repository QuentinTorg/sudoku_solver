"""Shared helpers for uniqueness-family techniques."""

from dataclasses import dataclass
from itertools import combinations

from sudoku_solver.units import peers


@dataclass(slots=True, frozen=True)
class RectanglePairPattern:
    """Rectangle corners that all contain a shared digit pair."""

    rows: tuple[int, int]
    cols: tuple[int, int]
    corners: tuple[int, int, int, int]
    corner_sets: tuple[frozenset[int], frozenset[int], frozenset[int], frozenset[int]]
    pair_digits: tuple[int, int]


@dataclass(slots=True, frozen=True)
class UniquenessElimination:
    """Single uniqueness-derived elimination batch."""

    kind: str
    rows: tuple[int, int]
    cols: tuple[int, int]
    eliminations: tuple[tuple[int, int], ...]


def iter_rectangle_pair_patterns(candidates: dict[int, set[int]]) -> list[RectanglePairPattern]:
    """Enumerate rectangle/pair patterns shared by both uniqueness rules."""
    patterns: list[RectanglePairPattern] = []
    for first_row, second_row in combinations(range(9), 2):
        for first_col, second_col in combinations(range(9), 2):
            corners = (
                first_row * 9 + first_col,
                first_row * 9 + second_col,
                second_row * 9 + first_col,
                second_row * 9 + second_col,
            )
            if any(cell_index not in candidates for cell_index in corners):
                continue

            corner_sets: tuple[
                frozenset[int],
                frozenset[int],
                frozenset[int],
                frozenset[int],
            ] = (
                frozenset(candidates[corners[0]]),
                frozenset(candidates[corners[1]]),
                frozenset(candidates[corners[2]]),
                frozenset(candidates[corners[3]]),
            )
            common = set(corner_sets[0])
            for options in corner_sets[1:]:
                common &= set(options)
            if len(common) < 2:
                continue

            for first_digit, second_digit in combinations(sorted(common), 2):
                pair_set = {first_digit, second_digit}
                if not all(pair_set.issubset(options) for options in corner_sets):
                    continue
                patterns.append(
                    RectanglePairPattern(
                        rows=(first_row, second_row),
                        cols=(first_col, second_col),
                        corners=corners,
                        corner_sets=corner_sets,
                        pair_digits=(first_digit, second_digit),
                    )
                )
    return patterns


def find_unique_rectangle_type1_elimination(
    candidates: dict[int, set[int]],
) -> UniquenessElimination | None:
    """Find one type-1 unique rectangle elimination."""
    for pattern in iter_rectangle_pair_patterns(candidates):
        box_counts: dict[int, int] = {}
        for cell_index in pattern.corners:
            box = ((cell_index // 9) // 3) * 3 + ((cell_index % 9) // 3)
            box_counts[box] = box_counts.get(box, 0) + 1
        if len(box_counts) != 2 or sorted(box_counts.values()) != [2, 2]:
            continue

        pair_set = set(pattern.pair_digits)
        pure_pair_count = sum(1 for options in pattern.corner_sets if options == pair_set)
        if pure_pair_count != 3:
            continue

        extras = [options - pair_set for options in pattern.corner_sets]
        extra_indices = [index for index, extra in enumerate(extras) if extra]
        if len(extra_indices) != 1:
            continue

        target_corner = pattern.corners[extra_indices[0]]
        eliminations = tuple((target_corner, digit) for digit in sorted(extras[extra_indices[0]]))
        if not eliminations:
            continue

        return UniquenessElimination(
            kind="ur_type1",
            rows=pattern.rows,
            cols=pattern.cols,
            eliminations=eliminations,
        )

    return None


def find_uniqueness_expansion_elimination(
    candidates: dict[int, set[int]],
) -> UniquenessElimination | None:
    """Find one restricted UR type-2 style elimination."""
    for pattern in iter_rectangle_pair_patterns(candidates):
        pair_set = set(pattern.pair_digits)
        extras = [set(options) - pair_set for options in pattern.corner_sets]
        expanded_indices = [index for index, extra in enumerate(extras) if len(extra) == 1]
        if len(expanded_indices) != 2:
            continue
        if any(index not in expanded_indices and extras[index] for index in range(4)):
            continue

        first_expanded = pattern.corners[expanded_indices[0]]
        second_expanded = pattern.corners[expanded_indices[1]]
        if extras[expanded_indices[0]] != extras[expanded_indices[1]]:
            continue
        extra_digit = next(iter(extras[expanded_indices[0]]))

        if second_expanded not in peers(first_expanded):
            continue

        eliminations = tuple(
            (cell_index, extra_digit)
            for cell_index in sorted(peers(first_expanded) & peers(second_expanded))
            if cell_index not in pattern.corners
            and cell_index in candidates
            and extra_digit in candidates[cell_index]
        )
        if not eliminations:
            continue

        return UniquenessElimination(
            kind="ur_type2_restricted",
            rows=pattern.rows,
            cols=pattern.cols,
            eliminations=eliminations,
        )

    return None
