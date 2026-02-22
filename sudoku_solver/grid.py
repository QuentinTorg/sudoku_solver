"""Grid parsing and formatting helpers."""

from sudoku_solver.types import Grid
from sudoku_solver.units import all_units


def parse_grid(puzzle: str) -> Grid:
    """Parse an 81-character puzzle string into a Grid."""
    if len(puzzle) != 81:
        msg = "Puzzle must contain exactly 81 characters."
        raise ValueError(msg)

    cells: list[int] = []
    for char in puzzle:
        if char in {".", "0"}:
            cells.append(0)
            continue
        if char.isdigit() and char != "0":
            cells.append(int(char))
            continue
        msg = f"Invalid puzzle character: {char!r}"
        raise ValueError(msg)

    _validate_no_conflicts(cells)
    return Grid(cells=tuple(cells))


def format_grid(grid: Grid) -> str:
    """Serialize a Grid back to normalized 81-character format."""
    if len(grid.cells) != 81:
        msg = "Grid must contain exactly 81 cells."
        raise ValueError(msg)

    chars: list[str] = []
    for value in grid.cells:
        if value == 0:
            chars.append(".")
            continue
        if 1 <= value <= 9:
            chars.append(str(value))
            continue
        msg = f"Grid contains invalid value: {value!r}"
        raise ValueError(msg)

    return "".join(chars)


def _validate_no_conflicts(cells: list[int]) -> None:
    """Raise ValueError if any row, column, or box has duplicate digits."""
    for _, unit in all_units():
        seen: set[int] = set()
        for index in unit:
            value = cells[index]
            if value == 0:
                continue
            if value in seen:
                msg = "Puzzle has conflicting givens in a unit."
                raise ValueError(msg)
            seen.add(value)
