"""Shared helpers for ALS-family techniques."""

from dataclasses import dataclass
from itertools import combinations

from sudoku_solver.units import all_units, peers


@dataclass(slots=True, frozen=True)
class Als:
    """Compact representation of an almost-locked set."""

    cells: tuple[int, ...]
    digits: frozenset[int]
    unit_name: str


@dataclass(slots=True, frozen=True)
class AlsElimination:
    """Single ALS-style elimination batch."""

    restricted_digit: int
    target_digit: int
    eliminations: tuple[tuple[int, int], ...]
    affected_units: tuple[str, ...]


@dataclass(slots=True, frozen=True)
class DeathBlossomElimination:
    """Single death-blossom elimination batch."""

    stem_cell: int
    first_petal: int
    second_petal: int
    target_digit: int
    eliminations: tuple[tuple[int, int], ...]


def find_als(candidates: dict[int, set[int]]) -> list[Als]:
    """Enumerate small ALS patterns from rows/columns/boxes."""
    results: list[Als] = []
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
                    Als(
                        cells=tuple(sorted(subset)),
                        digits=frozenset(digit_union),
                        unit_name=unit_name,
                    )
                )
    return results


def find_als_xz_elimination(candidates: dict[int, set[int]]) -> AlsElimination | None:
    """Find one restricted ALS-XZ elimination."""
    all_als = find_als(candidates)
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
                    return AlsElimination(
                        restricted_digit=restricted_digit,
                        target_digit=target_digit,
                        eliminations=tuple(sorted(eliminations)),
                        affected_units=(first_als.unit_name, second_als.unit_name),
                    )

    return None


def find_als_chain_elimination(candidates: dict[int, set[int]]) -> AlsElimination | None:
    """Find one restricted 3-ALS RCC-chain elimination."""
    all_als = find_als(candidates)
    if len(all_als) < 3:
        return None

    links: list[tuple[int, int, int]] = []
    for first_index, first_als in enumerate(all_als):
        for second_index in range(first_index + 1, len(all_als)):
            second_als = all_als[second_index]
            if set(first_als.cells) & set(second_als.cells):
                continue
            for digit in sorted(first_als.digits & second_als.digits):
                if _restricted_link_exists(candidates, first_als, second_als, digit):
                    links.append((first_index, second_index, digit))

    if not links:
        return None

    for middle_index, middle_als in enumerate(all_als):
        incoming = [
            (first_index, digit)
            for first_index, second_index, digit in links
            if second_index == middle_index
        ]
        incoming.extend(
            (second_index, digit)
            for first_index, second_index, digit in links
            if first_index == middle_index
        )
        if len(incoming) < 2:
            continue

        for first_neighbor, first_rcc in incoming:
            first_als = all_als[first_neighbor]
            for second_neighbor, second_rcc in incoming:
                if second_neighbor == first_neighbor:
                    continue
                second_als = all_als[second_neighbor]
                if set(first_als.cells) & set(second_als.cells):
                    continue
                if set(first_als.cells) & set(middle_als.cells):
                    continue
                if set(second_als.cells) & set(middle_als.cells):
                    continue

                target_digits = sorted((first_als.digits & second_als.digits) - {first_rcc, second_rcc})
                for target_digit in target_digits:
                    if target_digit in middle_als.digits:
                        continue
                    eliminations = _target_digit_eliminations(
                        candidates,
                        first_als,
                        second_als,
                        target_digit,
                    )
                    if not eliminations:
                        continue
                    return AlsElimination(
                        restricted_digit=first_rcc,
                        target_digit=target_digit,
                        eliminations=tuple(sorted(eliminations)),
                        affected_units=(
                            first_als.unit_name,
                            middle_als.unit_name,
                            second_als.unit_name,
                        ),
                    )

    return None


def _restricted_link_exists(
    candidates: dict[int, set[int]],
    first_als: Als,
    second_als: Als,
    digit: int,
) -> bool:
    first_cells = [cell_index for cell_index in first_als.cells if digit in candidates[cell_index]]
    second_cells = [cell_index for cell_index in second_als.cells if digit in candidates[cell_index]]
    if len(first_cells) != 1 or len(second_cells) != 1:
        return False
    return second_cells[0] in peers(first_cells[0])


def _target_digit_eliminations(
    candidates: dict[int, set[int]],
    first_als: Als,
    second_als: Als,
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
    return eliminations


def find_death_blossom_elimination(
    candidates: dict[int, set[int]],
) -> DeathBlossomElimination | None:
    """Find one restricted death-blossom elimination."""
    for stem_cell, stem_options in sorted(candidates.items()):
        if len(stem_options) < 2:
            continue

        petal_cells = [
            cell_index
            for cell_index in sorted(peers(stem_cell))
            if cell_index in candidates and len(candidates[cell_index]) == 2
        ]
        for first_petal, second_petal in combinations(petal_cells, 2):
            first_options = candidates[first_petal]
            second_options = candidates[second_petal]

            first_stem_digits = stem_options & first_options
            second_stem_digits = stem_options & second_options
            if len(first_stem_digits) != 1 or len(second_stem_digits) != 1:
                continue
            if first_stem_digits == second_stem_digits:
                continue

            first_external = first_options - first_stem_digits
            second_external = second_options - second_stem_digits
            if len(first_external) != 1 or len(second_external) != 1:
                continue
            if first_external != second_external:
                continue
            shared_external = next(iter(first_external))

            eliminations = [
                (cell_index, shared_external)
                for cell_index in sorted(peers(first_petal) & peers(second_petal))
                if cell_index not in {stem_cell, first_petal, second_petal}
                and cell_index in candidates
                and shared_external in candidates[cell_index]
            ]
            if eliminations:
                return DeathBlossomElimination(
                    stem_cell=stem_cell,
                    first_petal=first_petal,
                    second_petal=second_petal,
                    target_digit=shared_external,
                    eliminations=tuple(sorted(eliminations)),
                )

    return None
