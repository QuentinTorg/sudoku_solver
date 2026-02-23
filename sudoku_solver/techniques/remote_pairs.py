"""Remote Pairs technique.

Meaning:
    A chain of bivalue cells with the same pair can force eliminations of both
    digits from cells that see opposite chain colors.

When used:
    As an advanced chain technique after wing and fish methods.
"""

from collections import deque
from itertools import combinations

from sudoku_solver.grid import format_grid
from sudoku_solver.types import Grid, Step, TechniqueName
from sudoku_solver.units import peers


def apply_remote_pairs(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a remote-pairs elimination, else return None."""
    if not candidates:
        return None

    pair_to_cells: dict[tuple[int, int], list[int]] = {}
    for cell_index, options in candidates.items():
        if len(options) != 2:
            continue
        pair = tuple(sorted(options))
        pair_to_cells.setdefault(pair, []).append(cell_index)

    for pair, pair_cells in pair_to_cells.items():
        if len(pair_cells) < 4:
            continue

        adjacency: dict[int, set[int]] = {cell_index: set() for cell_index in pair_cells}
        for first, second in combinations(pair_cells, 2):
            if second in peers(first):
                adjacency[first].add(second)
                adjacency[second].add(first)

        visited: set[int] = set()
        for start in pair_cells:
            if start in visited or not adjacency[start]:
                continue

            queue: deque[int] = deque([start])
            color: dict[int, int] = {start: 0}
            component: set[int] = set()
            is_bipartite = True

            while queue:
                current = queue.popleft()
                component.add(current)
                visited.add(current)
                for neighbor in adjacency[current]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        is_bipartite = False

            if not is_bipartite:
                continue

            color_groups = {
                0: {cell_index for cell_index in component if color[cell_index] == 0},
                1: {cell_index for cell_index in component if color[cell_index] == 1},
            }
            if not color_groups[0] or not color_groups[1]:
                continue

            eliminations: list[tuple[int, int]] = []
            for cell_index, options in candidates.items():
                if cell_index in component:
                    continue
                if not (
                    any(peer in color_groups[0] for peer in peers(cell_index))
                    and any(peer in color_groups[1] for peer in peers(cell_index))
                ):
                    continue
                for digit in pair:
                    if digit in options:
                        eliminations.append((cell_index, digit))

            if eliminations:
                return Step(
                    technique=TechniqueName.REMOTE_PAIRS,
                    placements=[],
                    eliminations=sorted(eliminations),
                    affected_units=[],
                    rationale=(
                        f"Remote pairs chain on digits {pair[0]} and {pair[1]} "
                        f"eliminates from common peers."
                    ),
                    grid_snapshot_after=format_grid(grid),
                )

    return None
