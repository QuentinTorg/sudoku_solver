"""Two-String Kite technique skeleton.

Meaning:
    One strong row link and one strong column link for a digit intersect to force
    eliminations at cells that see both opposite endpoints.

When used:
    As an advanced single-digit chain technique on stalled boards.
"""

from sudoku_solver.types import Grid, Step


def apply_two_string_kite(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a two-string-kite elimination, else return None."""
    if not candidates:
        return None
    return None
