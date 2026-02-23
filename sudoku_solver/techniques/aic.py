"""AIC technique (restricted alternating inference chain).

Meaning:
    Build alternating strong/weak links across candidate nodes. If a chain
    starts and ends on the same digit with weakly linked endpoints, that digit
    can be eliminated from common peers of the endpoints.

When used:
    On advanced stalled grids after XY-Chain and coloring methods.
"""

from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units, peers

Node = tuple[int, int]  # (cell_index, digit)
MAX_CHAIN_NODES = 8


def apply_aic(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted AIC elimination, else return None."""
    if not candidates:
        return None

    strong_graph, weak_graph = _build_link_graphs(candidates)
    if not strong_graph:
        return None

    for start in sorted(strong_graph):
        for next_node in sorted(strong_graph[start]):
            step = _search_chain(
                grid,
                candidates,
                start,
                next_node,
                strong_graph,
                weak_graph,
                path=[start, next_node],
                last_edge_type="S",
            )
            if step is not None:
                return step

    return None


def _build_link_graphs(
    candidates: dict[int, set[int]],
) -> tuple[dict[Node, set[Node]], dict[Node, set[Node]]]:
    strong: dict[Node, set[Node]] = {}
    weak: dict[Node, set[Node]] = {}

    for cell_index, options in candidates.items():
        option_list = sorted(options)
        if len(option_list) >= 2:
            for first_digit, second_digit in combinations(option_list, 2):
                first_node = (cell_index, first_digit)
                second_node = (cell_index, second_digit)
                _add_edge(weak, first_node, second_node)
                if len(option_list) == 2:
                    _add_edge(strong, first_node, second_node)

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
                _add_edge(weak, first, second)
            if len(nodes) == 2:
                _add_edge(strong, nodes[0], nodes[1])

    return strong, weak


def _add_edge(graph: dict[Node, set[Node]], first: Node, second: Node) -> None:
    graph.setdefault(first, set()).add(second)
    graph.setdefault(second, set()).add(first)


def _search_chain(
    grid: Grid,
    candidates: dict[int, set[int]],
    start: Node,
    current: Node,
    strong_graph: dict[Node, set[Node]],
    weak_graph: dict[Node, set[Node]],
    *,
    path: list[Node],
    last_edge_type: str,
) -> Step | None:
    if len(path) > MAX_CHAIN_NODES:
        return None

    if (
        len(path) >= 6
        and last_edge_type == "S"
        and start[1] == current[1]
        and start[0] != current[0]
        and current in weak_graph.get(start, set())
    ):
        digit = start[1]
        eliminations = [
            (cell_index, digit)
            for cell_index in sorted(peers(start[0]) & peers(current[0]))
            if cell_index not in {start[0], current[0]}
            and cell_index in candidates
            and digit in candidates[cell_index]
        ]
        if eliminations:
            return Step(
                technique=TechniqueName.AIC,
                placements=[],
                eliminations=eliminations,
                affected_units=[],
                rationale=(
                    f"AIC chain on digit {digit} between cells {start[0]} and {current[0]} "
                    "eliminates from common peers."
                ),
                grid_snapshot_after=format_grid(grid),
            )

    next_graph = weak_graph if last_edge_type == "S" else strong_graph
    next_edge_type = "W" if last_edge_type == "S" else "S"
    for next_node in sorted(next_graph.get(current, set())):
        if next_node in path:
            continue
        step = _search_chain(
            grid,
            candidates,
            start,
            next_node,
            strong_graph,
            weak_graph,
            path=path + [next_node],
            last_edge_type=next_edge_type,
        )
        if step is not None:
            return step

    return None
