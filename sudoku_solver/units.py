"""Sudoku board geometry helpers."""


def row_index(cell_index: int) -> int:
    """Return the zero-based row index for a cell."""
    return cell_index // 9


def col_index(cell_index: int) -> int:
    """Return the zero-based column index for a cell."""
    return cell_index % 9


def box_index(cell_index: int) -> int:
    """Return the zero-based 3x3 box index for a cell."""
    row = row_index(cell_index)
    col = col_index(cell_index)
    return (row // 3) * 3 + (col // 3)


def row_cells(row: int) -> list[int]:
    """Return cell indices for a zero-based row."""
    return [row * 9 + col for col in range(9)]


def col_cells(col: int) -> list[int]:
    """Return cell indices for a zero-based column."""
    return [row * 9 + col for row in range(9)]


def box_cells(box: int) -> list[int]:
    """Return cell indices for a zero-based box."""
    base_row = (box // 3) * 3
    base_col = (box % 3) * 3
    cells: list[int] = []
    for dr in range(3):
        for dc in range(3):
            cells.append((base_row + dr) * 9 + (base_col + dc))
    return cells


def all_units() -> list[tuple[str, list[int]]]:
    """Return all row/column/box units in deterministic order."""
    units: list[tuple[str, list[int]]] = []

    for row in range(9):
        units.append((f"row{row + 1}", row_cells(row)))
    for col in range(9):
        units.append((f"col{col + 1}", col_cells(col)))
    for box in range(9):
        units.append((f"box{box + 1}", box_cells(box)))

    return units


def peers(cell_index: int) -> set[int]:
    """Return all peer indices for a cell."""
    peer_cells: set[int] = set()
    peer_cells.update(row_cells(row_index(cell_index)))
    peer_cells.update(col_cells(col_index(cell_index)))
    peer_cells.update(box_cells(box_index(cell_index)))
    peer_cells.discard(cell_index)
    return peer_cells


def cell_label(cell_index: int) -> str:
    """Return a human-readable row/column label."""
    row = row_index(cell_index) + 1
    col = col_index(cell_index) + 1
    return f"r{row}c{col}"
