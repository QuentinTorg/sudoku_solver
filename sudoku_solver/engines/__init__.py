"""Shared technique engines used by multiple rule adapters."""

from sudoku_solver.engines.als_engine import (
    Als,
    AlsElimination,
    DeathBlossomElimination,
    find_als,
    find_als_xz_elimination,
    find_death_blossom_elimination,
)
from sudoku_solver.engines.chain_engine import (
    AicElimination,
    bivalue_cells,
    build_aic_link_graphs,
    build_digit_strong_link_graph,
    color_component,
    component_edge_count,
    find_aic_elimination,
    find_coloring_eliminations,
    shared_single_candidate,
    trap_eliminations,
    wrap_eliminations,
)
from sudoku_solver.engines.fish_engine import (
    FishElimination,
    find_finned_swordfish_elimination,
    find_finned_x_wing_elimination,
    find_standard_fish_elimination,
)
from sudoku_solver.engines.uniqueness_engine import (
    RectanglePairPattern,
    UniquenessElimination,
    find_unique_rectangle_type1_elimination,
    find_uniqueness_expansion_elimination,
    iter_rectangle_pair_patterns,
)

__all__ = [
    "AicElimination",
    "Als",
    "AlsElimination",
    "bivalue_cells",
    "build_aic_link_graphs",
    "build_digit_strong_link_graph",
    "color_component",
    "component_edge_count",
    "FishElimination",
    "find_finned_swordfish_elimination",
    "find_finned_x_wing_elimination",
    "DeathBlossomElimination",
    "find_als",
    "find_als_xz_elimination",
    "find_aic_elimination",
    "find_coloring_eliminations",
    "find_death_blossom_elimination",
    "find_uniqueness_expansion_elimination",
    "find_unique_rectangle_type1_elimination",
    "find_standard_fish_elimination",
    "iter_rectangle_pair_patterns",
    "RectanglePairPattern",
    "UniquenessElimination",
    "shared_single_candidate",
    "trap_eliminations",
    "wrap_eliminations",
]
