"""Skyscraper technique skeleton.

Meaning:
    Two strong links for one digit share a base, and roof cells force eliminations
    from cells that see both roofs.

When used:
    For advanced single-digit chain eliminations after wings/fish.
"""

from sudoku_solver.types import Grid, Step


def apply_skyscraper(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a skyscraper elimination, else return None."""
    if not candidates:
        return None
    return None
