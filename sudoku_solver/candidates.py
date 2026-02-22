"""Candidate generation and maintenance utilities."""

from sudoku_solver.types import Grid


Cell = int


def get_candidates(grid: Grid) -> dict[Cell, set[int]]:
    """Return a candidate set for each unsolved cell."""
    if len(grid.cells) != 81:
        msg = "Grid must contain exactly 81 cells."
        raise ValueError(msg)

    candidates: dict[Cell, set[int]] = {}
    for index, value in enumerate(grid.cells):
        if value != 0:
            continue
        disallowed = _peer_values(grid, index)
        candidates[index] = {digit for digit in range(1, 10) if digit not in disallowed}

    return candidates


def _peer_values(grid: Grid, index: int) -> set[int]:
    values: set[int] = set()
    for peer_index in _peer_indices(index):
        peer_value = grid.cells[peer_index]
        if peer_value != 0:
            values.add(peer_value)
    return values


def _peer_indices(index: int) -> set[int]:
    row = index // 9
    col = index % 9

    peers: set[int] = set()

    for c in range(9):
        peer = row * 9 + c
        if peer != index:
            peers.add(peer)

    for r in range(9):
        peer = r * 9 + col
        if peer != index:
            peers.add(peer)

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for dr in range(3):
        for dc in range(3):
            peer = (box_row + dr) * 9 + (box_col + dc)
            if peer != index:
                peers.add(peer)

    return peers
