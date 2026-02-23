"""3D Medusa technique (restricted implementation).

Meaning:
    Build two-color chains on candidate nodes using strong links across cells
    and units. Use color contradictions/traps to eliminate candidates.

When used:
    On advanced stalled grids after simpler coloring/fish methods.
"""

from collections import deque
from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units, peers

Node = tuple[int, int]  # (cell_index, digit)


def apply_three_d_medusa(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted 3D Medusa elimination, else return None."""
    if not candidates:
        return None

    strong_graph = _build_strong_graph(candidates)
    if not strong_graph:
        return None

    visited: set[Node] = set()
    for start in sorted(strong_graph):
        if start in visited:
            continue

        color = _color_component(start, strong_graph)
        component = set(color)
        visited.update(component)
        if len(component) < 2:
            continue

        impossible_color = _find_impossible_color(color, candidates)
        if impossible_color is not None:
            eliminations = sorted(
                {
                    (cell_index, digit)
                    for (cell_index, digit), value in color.items()
                    if value == impossible_color and digit in candidates.get(cell_index, set())
                }
            )
            if eliminations:
                return Step(
                    technique=TechniqueName.THREE_D_MEDUSA,
                    placements=[],
                    eliminations=eliminations,
                    affected_units=[],
                    rationale="3D Medusa color contradiction removes one full color set.",
                    grid_snapshot_after=format_grid(grid),
                )

        trap_eliminations = _find_color_trap_eliminations(color, component, candidates)
        if trap_eliminations:
            return Step(
                technique=TechniqueName.THREE_D_MEDUSA,
                placements=[],
                eliminations=trap_eliminations,
                affected_units=[],
                rationale="3D Medusa color trap removes candidates seeing both colors.",
                grid_snapshot_after=format_grid(grid),
            )

    return None


def _build_strong_graph(candidates: dict[int, set[int]]) -> dict[Node, set[Node]]:
    graph: dict[Node, set[Node]] = {}

    for cell_index, options in candidates.items():
        if len(options) != 2:
            continue
        first_digit, second_digit = sorted(options)
        _add_edge(graph, (cell_index, first_digit), (cell_index, second_digit))

    for _, unit_cells in all_units():
        for digit in range(1, 10):
            positions = [
                cell_index
                for cell_index in unit_cells
                if cell_index in candidates and digit in candidates[cell_index]
            ]
            if len(positions) != 2:
                continue
            _add_edge(graph, (positions[0], digit), (positions[1], digit))

    return graph


def _add_edge(graph: dict[Node, set[Node]], first: Node, second: Node) -> None:
    graph.setdefault(first, set()).add(second)
    graph.setdefault(second, set()).add(first)


def _color_component(start: Node, graph: dict[Node, set[Node]]) -> dict[Node, int]:
    color: dict[Node, int] = {start: 0}
    queue: deque[Node] = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor in color:
                continue
            color[neighbor] = 1 - color[current]
            queue.append(neighbor)
    return color


def _find_impossible_color(color: dict[Node, int], candidates: dict[int, set[int]]) -> int | None:
    by_cell: dict[int, list[Node]] = {}
    by_digit: dict[int, list[Node]] = {}
    for node in color:
        by_cell.setdefault(node[0], []).append(node)
        by_digit.setdefault(node[1], []).append(node)

    for nodes in by_cell.values():
        for first, second in combinations(nodes, 2):
            if color[first] == color[second]:
                return color[first]

    for nodes in by_digit.values():
        for first, second in combinations(nodes, 2):
            if first[0] == second[0]:
                continue
            if second[0] not in peers(first[0]):
                continue
            if color[first] == color[second]:
                return color[first]

    # Keep conservative: require contradiction within already-colored nodes.
    return None


def _find_color_trap_eliminations(
    color: dict[Node, int],
    component: set[Node],
    candidates: dict[int, set[int]],
) -> list[tuple[int, int]]:
    colored_by_digit: dict[int, dict[int, set[int]]] = {}
    for (cell_index, digit), value in color.items():
        colored_by_digit.setdefault(digit, {0: set(), 1: set()})
        colored_by_digit[digit][value].add(cell_index)

    eliminations: list[tuple[int, int]] = []
    for cell_index, options in candidates.items():
        for digit in sorted(options):
            node = (cell_index, digit)
            if node in component:
                continue
            groups = colored_by_digit.get(digit)
            if groups is None:
                continue
            sees_color0 = any(peer in groups[0] for peer in peers(cell_index))
            sees_color1 = any(peer in groups[1] for peer in peers(cell_index))
            if sees_color0 and sees_color1:
                eliminations.append((cell_index, digit))

    return sorted(set(eliminations))
