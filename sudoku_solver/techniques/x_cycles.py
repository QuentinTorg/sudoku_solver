"""X-Cycles technique (restricted single-digit loops).

Meaning:
    Alternating strong-link cycles for one digit can force eliminations by
    coloring contradictions.

When used:
    On advanced stalled puzzles after fish/wing techniques.
"""

from collections import deque
from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import all_units, peers


def apply_x_cycles(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply restricted X-Cycles elimination, else return None."""
    if not candidates:
        return None

    for digit in range(1, 10):
        adjacency = _build_strong_link_graph(candidates, digit)
        if not adjacency:
            continue

        visited: set[int] = set()
        for start in sorted(adjacency):
            if start in visited:
                continue

            color, edge_count = _color_component(start, adjacency)
            component = set(color)
            visited.update(component)
            # Restrict to loop-like components.
            if edge_count < len(component):
                continue

            groups = {
                0: {cell_index for cell_index, value in color.items() if value == 0},
                1: {cell_index for cell_index, value in color.items() if value == 1},
            }

            eliminations = _wrap_eliminations(candidates, digit, groups)
            eliminations.extend(_trap_eliminations(candidates, digit, component, groups))
            eliminations = sorted(set(eliminations))
            if eliminations:
                return Step(
                    technique=TechniqueName.X_CYCLES,
                    placements=[],
                    eliminations=eliminations,
                    affected_units=[],
                    rationale=f"X-Cycle loop on digit {digit} produced eliminations.",
                    grid_snapshot_after=format_grid(grid),
                )

    return None


def _build_strong_link_graph(candidates: dict[int, set[int]], digit: int) -> dict[int, set[int]]:
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
        adjacency.setdefault(first, set()).add(second)
        adjacency.setdefault(second, set()).add(first)
    return adjacency


def _color_component(start: int, adjacency: dict[int, set[int]]) -> tuple[dict[int, int], int]:
    color: dict[int, int] = {start: 0}
    queue: deque[int] = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor in color:
                continue
            color[neighbor] = 1 - color[current]
            queue.append(neighbor)
    edge_count = sum(len(adjacency[cell_index]) for cell_index in color) // 2
    return color, edge_count


def _wrap_eliminations(
    candidates: dict[int, set[int]],
    digit: int,
    groups: dict[int, set[int]],
) -> list[tuple[int, int]]:
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


def _trap_eliminations(
    candidates: dict[int, set[int]],
    digit: int,
    component: set[int],
    groups: dict[int, set[int]],
) -> list[tuple[int, int]]:
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
