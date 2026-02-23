"""Shared helpers for chain-family techniques.

This module centralizes graph construction and chain traversals used by:
- AIC-family techniques
- Coloring/X-Cycles techniques
- XY-Chain neighborhood scans
- Forcing Chains/Nets branch consequences
"""

from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import TypeVar

from sudoku_solver.candidates import get_candidates
from sudoku_solver.types import Grid
from sudoku_solver.units import all_units, peers

Node = tuple[int, int]  # (cell_index, digit)
GraphNode = TypeVar("GraphNode", int, Node)


@dataclass(slots=True, frozen=True)
class AicElimination:
    """Single AIC-derived elimination batch."""

    digit: int
    start_cell: int
    end_cell: int
    eliminations: tuple[tuple[int, int], ...]
    pattern: str = "endpoint_peer"


@dataclass(slots=True, frozen=True)
class ForcingConsequence:
    """Consequence detected by bivalue forcing-chain branch analysis."""

    pivot_cell: int
    placements: tuple[tuple[int, int], ...]
    eliminations: tuple[tuple[int, int], ...]
    reason: str


@dataclass(slots=True)
class _ForcingBranchResult:
    valid: bool
    cells: list[int]
    candidates: dict[int, set[int]]


def add_undirected_edge(
    graph: dict[GraphNode, set[GraphNode]],
    first: GraphNode,
    second: GraphNode,
) -> None:
    """Insert an undirected edge between two nodes."""
    graph.setdefault(first, set()).add(second)
    graph.setdefault(second, set()).add(first)


def build_aic_link_graphs(
    candidates: dict[int, set[int]],
) -> tuple[dict[Node, set[Node]], dict[Node, set[Node]]]:
    """Build strong/weak candidate-node graphs for AIC-style traversals."""
    strong: dict[Node, set[Node]] = {}
    weak: dict[Node, set[Node]] = {}

    for cell_index, options in candidates.items():
        option_list = sorted(options)
        if len(option_list) < 2:
            continue
        for first_digit, second_digit in combinations(option_list, 2):
            first_node = (cell_index, first_digit)
            second_node = (cell_index, second_digit)
            add_undirected_edge(weak, first_node, second_node)
            if len(option_list) == 2:
                add_undirected_edge(strong, first_node, second_node)

    for _, unit_cells in all_units():
        for digit in range(1, 10):
            positions = [
                cell_index
                for cell_index in unit_cells
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) < 2:
                continue
            nodes = [(cell_index, digit) for cell_index in sorted(positions)]
            for first, second in combinations(nodes, 2):
                add_undirected_edge(weak, first, second)
            if len(nodes) == 2:
                add_undirected_edge(strong, nodes[0], nodes[1])

    return strong, weak


def find_aic_elimination(
    candidates: dict[int, set[int]],
    *,
    max_chain_nodes: int = 8,
    allow_same_cell_discontinuity: bool = True,
) -> AicElimination | None:
    """Find one restricted AIC elimination, if available."""
    strong_graph, weak_graph = build_aic_link_graphs(candidates)
    if not strong_graph:
        return None

    for start in sorted(strong_graph):
        for next_node in sorted(strong_graph[start]):
            elimination = _search_aic_chain(
                candidates,
                start,
                next_node,
                strong_graph,
                weak_graph,
                path=[start, next_node],
                last_edge_type="S",
                max_chain_nodes=max_chain_nodes,
                allow_same_cell_discontinuity=allow_same_cell_discontinuity,
            )
            if elimination is not None:
                return elimination

    return None


def _search_aic_chain(
    candidates: dict[int, set[int]],
    start: Node,
    current: Node,
    strong_graph: dict[Node, set[Node]],
    weak_graph: dict[Node, set[Node]],
    *,
    path: list[Node],
    last_edge_type: str,
    max_chain_nodes: int,
    allow_same_cell_discontinuity: bool,
) -> AicElimination | None:
    if len(path) > max_chain_nodes:
        return None

    if (
        len(path) >= 6
        and last_edge_type == "S"
        and start[1] == current[1]
        and start[0] != current[0]
        and current in weak_graph.get(start, set())
    ):
        digit = start[1]
        eliminations = tuple(
            (cell_index, digit)
            for cell_index in sorted(peers(start[0]) & peers(current[0]))
            if cell_index not in {start[0], current[0]}
            and cell_index in candidates
            and digit in candidates[cell_index]
        )
        if eliminations:
            return AicElimination(
                digit=digit,
                start_cell=start[0],
                end_cell=current[0],
                eliminations=eliminations,
                pattern="endpoint_peer",
            )

    if (
        allow_same_cell_discontinuity
        and len(path) >= 5
        and last_edge_type == "W"
        and start[0] == current[0]
        and start[1] != current[1]
        and current in weak_graph.get(start, set())
    ):
        extras = [
            digit
            for digit in sorted(candidates.get(start[0], set()))
            if digit not in {start[1], current[1]}
        ]
        if extras:
            return AicElimination(
                digit=start[1],
                start_cell=start[0],
                end_cell=current[0],
                eliminations=tuple((start[0], digit) for digit in extras),
                pattern="same_cell_discontinuity",
            )

    next_graph = weak_graph if last_edge_type == "S" else strong_graph
    next_edge_type = "W" if last_edge_type == "S" else "S"
    for next_node in sorted(next_graph.get(current, set())):
        if next_node in path:
            continue
        elimination = _search_aic_chain(
            candidates,
            start,
            next_node,
            strong_graph,
            weak_graph,
            path=path + [next_node],
            last_edge_type=next_edge_type,
            max_chain_nodes=max_chain_nodes,
            allow_same_cell_discontinuity=allow_same_cell_discontinuity,
        )
        if elimination is not None:
            return elimination

    return None


def build_digit_strong_link_graph(
    candidates: dict[int, set[int]],
    digit: int,
) -> dict[int, set[int]]:
    """Build strong-link graph for one digit across all units."""
    adjacency: dict[int, set[int]] = {}
    for _, unit_cells in all_units():
        positions = [
            cell_index
            for cell_index in unit_cells
            if cell_index in candidates and digit in candidates[cell_index]
        ]
        if len(positions) != 2:
            continue
        first, second = positions
        add_undirected_edge(adjacency, first, second)
    return adjacency


def color_component(start: int, adjacency: dict[int, set[int]]) -> dict[int, int]:
    """Two-color one connected component of a strong-link graph."""
    color: dict[int, int] = {start: 0}
    queue: deque[int] = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor in color:
                continue
            color[neighbor] = 1 - color[current]
            queue.append(neighbor)
    return color


def component_edge_count(adjacency: dict[int, set[int]], component: set[int]) -> int:
    """Count undirected edges inside a colored component."""
    return sum(len(adjacency[cell_index]) for cell_index in component) // 2


def wrap_eliminations(
    candidates: dict[int, set[int]],
    digit: int,
    groups: dict[int, set[int]],
) -> list[tuple[int, int]]:
    """Return color-wrap eliminations for one digit/component."""
    for group in groups.values():
        for first, second in combinations(sorted(group), 2):
            if second not in peers(first):
                continue
            return [
                (cell_index, digit)
                for cell_index in sorted(group)
                if cell_index in candidates and digit in candidates[cell_index]
            ]
    return []


def trap_eliminations(
    candidates: dict[int, set[int]],
    digit: int,
    component: set[int],
    groups: dict[int, set[int]],
) -> list[tuple[int, int]]:
    """Return color-trap eliminations for one digit/component."""
    eliminations: list[tuple[int, int]] = []
    for cell_index, options in candidates.items():
        if cell_index in component or digit not in options:
            continue
        if not any(peer in groups[0] for peer in peers(cell_index)):
            continue
        if not any(peer in groups[1] for peer in peers(cell_index)):
            continue
        eliminations.append((cell_index, digit))
    return eliminations


def find_coloring_eliminations(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    require_loop_component: bool,
) -> list[tuple[int, int]]:
    """Find first elimination set from coloring analysis for one digit."""
    adjacency = build_digit_strong_link_graph(candidates, digit)
    if not adjacency:
        return []

    visited: set[int] = set()
    for start in sorted(adjacency):
        if start in visited:
            continue

        color = color_component(start, adjacency)
        component = set(color)
        visited.update(component)
        if len(component) < 2:
            continue
        if require_loop_component and component_edge_count(adjacency, component) < len(component):
            continue

        groups = {
            0: {cell_index for cell_index, value in color.items() if value == 0},
            1: {cell_index for cell_index, value in color.items() if value == 1},
        }
        eliminations = wrap_eliminations(candidates, digit, groups)
        eliminations.extend(trap_eliminations(candidates, digit, component, groups))
        deduped = sorted(set(eliminations))
        if deduped:
            return deduped

    return []


def bivalue_cells(candidates: dict[int, set[int]]) -> list[int]:
    """Return sorted cell indices that currently have exactly two candidates."""
    return [cell_index for cell_index in sorted(candidates) if len(candidates[cell_index]) == 2]


def shared_single_candidate(
    candidates: dict[int, set[int]],
    first_cell: int,
    second_cell: int,
) -> int | None:
    """Return shared candidate when exactly one candidate is shared, else None."""
    shared = candidates[first_cell] & candidates[second_cell]
    if len(shared) != 1:
        return None
    return next(iter(shared))


def find_forcing_chains_consequence(
    grid: Grid,
    candidates: dict[int, set[int]],
) -> ForcingConsequence | None:
    """Find one forcing-chains/net consequence from a bivalue pivot."""
    if not candidates:
        return None

    allowed = {cell_index: set(options) for cell_index, options in candidates.items()}
    for pivot_cell in bivalue_cells(candidates):
        pivot_digits = sorted(candidates[pivot_cell])
        if len(pivot_digits) != 2:
            continue

        first_digit, second_digit = pivot_digits
        first_branch = _propagate_assumption(grid.cells, allowed, pivot_cell, first_digit)
        second_branch = _propagate_assumption(grid.cells, allowed, pivot_cell, second_digit)

        if first_branch.valid and not second_branch.valid:
            return ForcingConsequence(
                pivot_cell=pivot_cell,
                placements=((pivot_cell, first_digit),),
                eliminations=(),
                reason=(
                    f"Assuming {second_digit} in cell {pivot_cell} causes contradiction; "
                    f"cell {pivot_cell} must be {first_digit}."
                ),
            )
        if second_branch.valid and not first_branch.valid:
            return ForcingConsequence(
                pivot_cell=pivot_cell,
                placements=((pivot_cell, second_digit),),
                eliminations=(),
                reason=(
                    f"Assuming {first_digit} in cell {pivot_cell} causes contradiction; "
                    f"cell {pivot_cell} must be {second_digit}."
                ),
            )
        if not first_branch.valid or not second_branch.valid:
            continue

        common_placements = _common_branch_placements(
            grid.cells,
            first_branch.cells,
            second_branch.cells,
        )
        if common_placements:
            return ForcingConsequence(
                pivot_cell=pivot_cell,
                placements=tuple(common_placements),
                eliminations=(),
                reason=(
                    f"Both forcing branches from pivot cell {pivot_cell} place the same values."
                ),
            )

        common_eliminations = _common_branch_eliminations(
            candidates,
            first_branch.candidates,
            second_branch.candidates,
            pivot_cell=pivot_cell,
        )
        if common_eliminations:
            return ForcingConsequence(
                pivot_cell=pivot_cell,
                placements=(),
                eliminations=tuple(common_eliminations),
                reason=(
                    f"Both forcing branches from pivot cell {pivot_cell} "
                    "remove the same candidates."
                ),
            )

    return None


def find_forcing_nets_consequence(
    grid: Grid,
    candidates: dict[int, set[int]],
) -> ForcingConsequence | None:
    """Find one forcing-net consequence from a 2-4 candidate pivot."""
    if not candidates:
        return None

    allowed = {cell_index: set(options) for cell_index, options in candidates.items()}
    pivot_cells = [
        cell_index for cell_index in sorted(candidates) if 2 <= len(candidates[cell_index]) <= 4
    ]
    for pivot_cell in pivot_cells:
        pivot_digits = sorted(candidates[pivot_cell])
        branch_results: dict[int, _ForcingBranchResult] = {}
        for digit in pivot_digits:
            branch_results[digit] = _propagate_assumption(
                grid.cells,
                allowed,
                pivot_cell,
                digit,
            )

        valid_digits = [digit for digit in pivot_digits if branch_results[digit].valid]
        invalid_digits = [digit for digit in pivot_digits if not branch_results[digit].valid]
        if not valid_digits:
            continue

        if len(valid_digits) == 1 and invalid_digits:
            forced_digit = valid_digits[0]
            return ForcingConsequence(
                pivot_cell=pivot_cell,
                placements=((pivot_cell, forced_digit),),
                eliminations=(),
                reason=(
                    f"Forcing net branches {invalid_digits} at cell {pivot_cell} "
                    "contradict; remaining digit is forced."
                ),
            )

        valid_branches = [branch_results[digit] for digit in valid_digits]
        common_placements = _common_placements_for_branches(grid.cells, valid_branches)
        if common_placements:
            return ForcingConsequence(
                pivot_cell=pivot_cell,
                placements=tuple(common_placements),
                eliminations=(),
                reason=(f"Forcing net branches from cell {pivot_cell} agree on placements."),
            )

        common_eliminations = _common_eliminations_for_branches(
            candidates,
            valid_branches,
            pivot_cell=pivot_cell,
        )
        if common_eliminations:
            return ForcingConsequence(
                pivot_cell=pivot_cell,
                placements=(),
                eliminations=tuple(common_eliminations),
                reason=(f"Forcing net branches from cell {pivot_cell} agree on eliminations."),
            )

    return None


def _propagate_assumption(
    base_cells: tuple[int, ...],
    allowed_candidates: dict[int, set[int]],
    assumed_cell: int,
    assumed_digit: int,
) -> _ForcingBranchResult:
    cells = list(base_cells)
    current = cells[assumed_cell]
    if current not in (0, assumed_digit):
        return _ForcingBranchResult(valid=False, cells=cells, candidates={})
    cells[assumed_cell] = assumed_digit

    while True:
        if _has_duplicate_values(cells):
            return _ForcingBranchResult(valid=False, cells=cells, candidates={})

        branch_candidates = _state_candidates(cells, allowed_candidates)
        if branch_candidates is None:
            return _ForcingBranchResult(valid=False, cells=cells, candidates={})
        if _has_unit_digit_contradiction(cells, branch_candidates):
            return _ForcingBranchResult(valid=False, cells=cells, candidates={})

        forced = _forced_single_placements(cells, branch_candidates)
        if not forced:
            return _ForcingBranchResult(valid=True, cells=cells, candidates=branch_candidates)

        changed = False
        for cell_index, digit in sorted(forced.items()):
            current_value = cells[cell_index]
            if current_value == digit:
                continue
            if current_value not in (0, digit):
                return _ForcingBranchResult(valid=False, cells=cells, candidates={})
            cells[cell_index] = digit
            changed = True
        if not changed:
            return _ForcingBranchResult(valid=True, cells=cells, candidates=branch_candidates)


def _has_duplicate_values(cells: list[int]) -> bool:
    for _, unit_cells in all_units():
        seen: set[int] = set()
        for cell_index in unit_cells:
            value = cells[cell_index]
            if value == 0:
                continue
            if value in seen:
                return True
            seen.add(value)
    return False


def _state_candidates(
    cells: list[int],
    allowed_candidates: dict[int, set[int]],
) -> dict[int, set[int]] | None:
    base_candidates = get_candidates(Grid(cells=tuple(cells)))
    normalized: dict[int, set[int]] = {}
    for cell_index, base_options in base_candidates.items():
        retained = allowed_candidates.get(cell_index, set(base_options))
        options = set(base_options) & set(retained)
        if not options:
            return None
        normalized[cell_index] = options
    return normalized


def _has_unit_digit_contradiction(
    cells: list[int],
    candidates: dict[int, set[int]],
) -> bool:
    for _, unit_cells in all_units():
        placed = {cells[cell_index] for cell_index in unit_cells if cells[cell_index] != 0}
        for digit in range(1, 10):
            if digit in placed:
                continue
            if any(
                cells[cell_index] == 0 and digit in candidates.get(cell_index, set())
                for cell_index in unit_cells
            ):
                continue
            return True
    return False


def _forced_single_placements(
    cells: list[int],
    candidates: dict[int, set[int]],
) -> dict[int, int]:
    forced: dict[int, int] = {}
    for cell_index, options in candidates.items():
        if len(options) == 1:
            forced[cell_index] = next(iter(options))

    for _, unit_cells in all_units():
        for digit in range(1, 10):
            positions = [
                cell_index
                for cell_index in unit_cells
                if cells[cell_index] == 0
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if len(positions) != 1:
                continue
            target = positions[0]
            existing = forced.get(target)
            if existing is not None and existing != digit:
                forced[target] = -1
                continue
            forced[target] = digit

    return {cell_index: digit for cell_index, digit in forced.items() if digit > 0}


def _common_branch_placements(
    base_cells: tuple[int, ...],
    first_cells: list[int],
    second_cells: list[int],
) -> list[tuple[int, int]]:
    placements: list[tuple[int, int]] = []
    for index, original in enumerate(base_cells):
        if original != 0:
            continue
        first_value = first_cells[index]
        second_value = second_cells[index]
        if first_value == 0 or first_value != second_value:
            continue
        placements.append((index, first_value))
    return placements


def _common_placements_for_branches(
    base_cells: tuple[int, ...],
    branches: list[_ForcingBranchResult],
) -> list[tuple[int, int]]:
    if len(branches) < 2:
        return []

    placements: list[tuple[int, int]] = []
    for index, original in enumerate(base_cells):
        if original != 0:
            continue
        branch_values = [branch.cells[index] for branch in branches]
        if any(value == 0 for value in branch_values):
            continue
        if len(set(branch_values)) != 1:
            continue
        placements.append((index, branch_values[0]))
    return placements


def _common_branch_eliminations(
    base_candidates: dict[int, set[int]],
    first_candidates: dict[int, set[int]],
    second_candidates: dict[int, set[int]],
    *,
    pivot_cell: int,
) -> list[tuple[int, int]]:
    eliminations: list[tuple[int, int]] = []
    for cell_index, options in base_candidates.items():
        if cell_index == pivot_cell:
            continue
        first_options = first_candidates.get(cell_index, set())
        second_options = second_candidates.get(cell_index, set())
        for digit in sorted(options):
            if digit in first_options or digit in second_options:
                continue
            eliminations.append((cell_index, digit))
    return eliminations


def _common_eliminations_for_branches(
    base_candidates: dict[int, set[int]],
    branches: list[_ForcingBranchResult],
    *,
    pivot_cell: int,
) -> list[tuple[int, int]]:
    if len(branches) < 2:
        return []

    eliminations: list[tuple[int, int]] = []
    for cell_index, options in base_candidates.items():
        if cell_index == pivot_cell:
            continue
        for digit in sorted(options):
            if all(digit not in branch.candidates.get(cell_index, set()) for branch in branches):
                eliminations.append((cell_index, digit))
    return eliminations
