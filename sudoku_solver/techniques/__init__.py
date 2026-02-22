"""Technique function exports."""

from sudoku_solver.techniques.hidden_pair import apply_hidden_pair
from sudoku_solver.techniques.hidden_single import apply_hidden_single
from sudoku_solver.techniques.hidden_triple import apply_hidden_triple
from sudoku_solver.techniques.locked_candidates import apply_locked_candidates
from sudoku_solver.techniques.naked_pair import apply_naked_pair
from sudoku_solver.techniques.naked_single import apply_naked_single
from sudoku_solver.techniques.naked_triple import apply_naked_triple
from sudoku_solver.techniques.skyscraper import apply_skyscraper
from sudoku_solver.techniques.two_string_kite import apply_two_string_kite
from sudoku_solver.techniques.unique_rectangle import apply_unique_rectangle
from sudoku_solver.techniques.w_wing import apply_w_wing
from sudoku_solver.techniques.x_wing import apply_x_wing
from sudoku_solver.techniques.xy_wing import apply_xy_wing
from sudoku_solver.techniques.xyz_wing import apply_xyz_wing

__all__ = [
    "apply_hidden_triple",
    "apply_hidden_pair",
    "apply_hidden_single",
    "apply_locked_candidates",
    "apply_naked_pair",
    "apply_naked_single",
    "apply_naked_triple",
    "apply_skyscraper",
    "apply_two_string_kite",
    "apply_unique_rectangle",
    "apply_w_wing",
    "apply_x_wing",
    "apply_xy_wing",
    "apply_xyz_wing",
]
