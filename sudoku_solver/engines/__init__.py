"""Shared technique engines used by multiple rule adapters."""

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

__all__ = [
    "AicElimination",
    "bivalue_cells",
    "build_aic_link_graphs",
    "build_digit_strong_link_graph",
    "color_component",
    "component_edge_count",
    "FishElimination",
    "find_finned_swordfish_elimination",
    "find_finned_x_wing_elimination",
    "find_aic_elimination",
    "find_coloring_eliminations",
    "find_standard_fish_elimination",
    "shared_single_candidate",
    "trap_eliminations",
    "wrap_eliminations",
]
