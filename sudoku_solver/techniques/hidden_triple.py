"""Hidden triple technique skeleton.

Meaning:
    Three digits in a unit can only appear in the same three cells, so those
    cells can drop any other candidate digits.

When used:
    After naked triples if additional unit-level pruning is needed.
"""

from sudoku_solver.types import Grid, Step


def apply_hidden_triple(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    """Apply a hidden-triple elimination, else return None."""
    _ = (grid, candidates)
    raise NotImplementedError("apply_hidden_triple is not implemented yet")
