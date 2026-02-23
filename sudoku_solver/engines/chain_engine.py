"""Shared helpers for chain-family techniques.

This module centralizes graph construction and chain traversals used by:
- AIC-family techniques
- Coloring/X-Cycles techniques
- XY-Chain neighborhood scans
"""

from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import TypeVar

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
