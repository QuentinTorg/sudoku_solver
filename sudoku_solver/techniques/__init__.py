"""Technique function exports."""

from sudoku_solver.techniques.aic import apply_aic
from sudoku_solver.techniques.als_chains import apply_als_chains
from sudoku_solver.techniques.als_xz import apply_als_xz
from sudoku_solver.techniques.bug_plus_one import apply_bug_plus_one
from sudoku_solver.techniques.death_blossom import apply_death_blossom
from sudoku_solver.techniques.empty_rectangle import apply_empty_rectangle
from sudoku_solver.techniques.exocet import apply_exocet
from sudoku_solver.techniques.finned_swordfish import apply_finned_swordfish
from sudoku_solver.techniques.finned_x_wing import apply_finned_x_wing
from sudoku_solver.techniques.fireworks import apply_fireworks
from sudoku_solver.techniques.grouped_aic import apply_grouped_aic
from sudoku_solver.techniques.hidden_pair import apply_hidden_pair
from sudoku_solver.techniques.hidden_quad import apply_hidden_quad
from sudoku_solver.techniques.hidden_single import apply_hidden_single
from sudoku_solver.techniques.hidden_triple import apply_hidden_triple
from sudoku_solver.techniques.jellyfish import apply_jellyfish
from sudoku_solver.techniques.kraken_fish import apply_kraken_fish
from sudoku_solver.techniques.locked_candidates import apply_locked_candidates
from sudoku_solver.techniques.naked_pair import apply_naked_pair
from sudoku_solver.techniques.naked_quad import apply_naked_quad
from sudoku_solver.techniques.naked_single import apply_naked_single
from sudoku_solver.techniques.naked_triple import apply_naked_triple
from sudoku_solver.techniques.nice_loops import apply_nice_loops
from sudoku_solver.techniques.remote_pairs import apply_remote_pairs
from sudoku_solver.techniques.sashimi_fish import apply_sashimi_fish
from sudoku_solver.techniques.simple_coloring import apply_simple_coloring
from sudoku_solver.techniques.skyscraper import apply_skyscraper
from sudoku_solver.techniques.sue_de_coq import apply_sue_de_coq
from sudoku_solver.techniques.sue_de_coq_full import apply_sue_de_coq_full
from sudoku_solver.techniques.swordfish import apply_swordfish
from sudoku_solver.techniques.three_d_medusa import apply_three_d_medusa
from sudoku_solver.techniques.two_string_kite import apply_two_string_kite
from sudoku_solver.techniques.unique_rectangle import apply_unique_rectangle
from sudoku_solver.techniques.uniqueness_expansions import apply_uniqueness_expansions
from sudoku_solver.techniques.w_wing import apply_w_wing
from sudoku_solver.techniques.wxyz_wing import apply_wxyz_wing
from sudoku_solver.techniques.x_cycles import apply_x_cycles
from sudoku_solver.techniques.x_wing import apply_x_wing
from sudoku_solver.techniques.xy_chain import apply_xy_chain
from sudoku_solver.techniques.xy_wing import apply_xy_wing
from sudoku_solver.techniques.xyz_wing import apply_xyz_wing

__all__ = [
    "apply_als_xz",
    "apply_aic",
    "apply_als_chains",
    "apply_bug_plus_one",
    "apply_death_blossom",
    "apply_empty_rectangle",
    "apply_exocet",
    "apply_finned_swordfish",
    "apply_finned_x_wing",
    "apply_fireworks",
    "apply_grouped_aic",
    "apply_hidden_pair",
    "apply_hidden_quad",
    "apply_hidden_single",
    "apply_hidden_triple",
    "apply_jellyfish",
    "apply_kraken_fish",
    "apply_locked_candidates",
    "apply_naked_pair",
    "apply_naked_quad",
    "apply_naked_single",
    "apply_naked_triple",
    "apply_nice_loops",
    "apply_remote_pairs",
    "apply_sashimi_fish",
    "apply_skyscraper",
    "apply_simple_coloring",
    "apply_swordfish",
    "apply_sue_de_coq",
    "apply_sue_de_coq_full",
    "apply_three_d_medusa",
    "apply_two_string_kite",
    "apply_uniqueness_expansions",
    "apply_unique_rectangle",
    "apply_w_wing",
    "apply_wxyz_wing",
    "apply_x_wing",
    "apply_x_cycles",
    "apply_xy_chain",
    "apply_xy_wing",
    "apply_xyz_wing",
]
