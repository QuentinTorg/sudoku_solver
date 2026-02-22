"""Technique function exports."""

from sudoku_solver.techniques.hidden_triple import apply_hidden_triple
from sudoku_solver.techniques.hidden_pair import apply_hidden_pair
from sudoku_solver.techniques.hidden_single import apply_hidden_single
from sudoku_solver.techniques.locked_candidates import apply_locked_candidates
from sudoku_solver.techniques.naked_pair import apply_naked_pair
from sudoku_solver.techniques.naked_single import apply_naked_single
from sudoku_solver.techniques.naked_triple import apply_naked_triple
from sudoku_solver.techniques.xyz_wing import apply_xyz_wing

__all__ = [
    "apply_hidden_triple",
    "apply_hidden_pair",
    "apply_hidden_single",
    "apply_locked_candidates",
    "apply_naked_pair",
    "apply_naked_single",
    "apply_naked_triple",
    "apply_xyz_wing",
]
