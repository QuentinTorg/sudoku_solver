import unittest

import sudoku_solver.engines.chain_engine as chain_engine
from sudoku_solver.engines.chain_engine import (
    _apply_branch_candidate_reductions,
    _best_forcing_consequence,
    _branch_locked_candidates_eliminations,
    _branch_naked_pair_eliminations,
    _common_branch_eliminations,
    _common_branch_placements,
    _common_eliminations_for_branches,
    _common_placements_for_branches,
    _has_unit_digit_contradiction,
    _propagate_assumption,
    _search_aic_chain,
    _state_candidates,
    bivalue_cells,
    build_aic_link_graphs,
    build_digit_strong_link_graph,
    color_component,
    component_edge_count,
    find_aic_elimination,
    find_coloring_eliminations,
    find_forcing_chains_consequence,
    find_forcing_nets_consequence,
    shared_single_candidate,
)
from sudoku_solver.grid import parse_grid


class ChainEngineTests(unittest.TestCase):
    def test_find_aic_elimination_returns_expected_batch(self) -> None:
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {1, 3},
            3: {1, 6},
            4: {2, 4},
            5: {3, 5},
        }

        elimination = find_aic_elimination(candidates, max_chain_nodes=8)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.digit, 1)
        self.assertEqual(elimination.start_cell, 0)
        self.assertEqual(elimination.end_cell, 2)
        self.assertEqual(elimination.eliminations, ((3, 1),))

    def test_find_coloring_eliminations_returns_expected_batch(self) -> None:
        candidates = {
            1: {2, 5},
            3: {4, 5},
            5: {5, 6},
            28: {5, 9},
            30: {5, 7},
            41: {2, 5},
        }

        eliminations = find_coloring_eliminations(
            candidates,
            5,
            require_loop_component=True,
        )

        self.assertEqual(eliminations, [(1, 5), (5, 5), (30, 5)])

    def test_find_aic_elimination_handles_same_cell_discontinuity(self) -> None:
        candidates = {
            0: {1, 2, 3},
            1: {1, 2},
            10: {2, 4},
        }

        elimination = find_aic_elimination(candidates, max_chain_nodes=8)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.pattern, "same_cell_discontinuity")
        self.assertEqual(len(elimination.eliminations), 1)
        self.assertEqual(elimination.eliminations[0][0], 0)
        self.assertIn(elimination.eliminations[0][1], {2, 3})

    def test_component_edge_count_and_coloring_helpers(self) -> None:
        adjacency = {
            1: {3},
            3: {1, 5},
            5: {3},
        }

        colors = color_component(1, adjacency)
        self.assertEqual(colors, {1: 0, 3: 1, 5: 0})
        self.assertEqual(component_edge_count(adjacency, set(colors)), 2)

    def test_bivalue_and_shared_single_candidate_helpers(self) -> None:
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {1, 2, 3},
        }

        self.assertEqual(bivalue_cells(candidates), [0, 1])
        self.assertEqual(shared_single_candidate(candidates, 0, 1), 2)
        self.assertIsNone(shared_single_candidate(candidates, 0, 2))

    def test_find_forcing_chains_consequence_detects_contradiction_branch(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1},
        }

        consequence = find_forcing_chains_consequence(grid, candidates)

        self.assertIsNotNone(consequence)
        assert consequence is not None
        self.assertEqual(consequence.pivot_cell, 0)
        self.assertEqual(consequence.placements, ((0, 2),))
        self.assertEqual(consequence.eliminations, ())

    def test_find_forcing_chains_consequence_returns_none_without_forcing(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 2, 3},
        }

        consequence = find_forcing_chains_consequence(grid, candidates)
        self.assertIsNone(consequence)

    def test_find_forcing_nets_consequence_forces_digit_from_tri_pivot(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            1: {1},
            2: {2},
        }

        consequence = find_forcing_nets_consequence(grid, candidates)

        self.assertIsNotNone(consequence)
        assert consequence is not None
        self.assertEqual(consequence.pivot_cell, 0)
        self.assertEqual(consequence.placements, ((0, 3),))
        self.assertEqual(consequence.eliminations, ())

    def test_find_forcing_nets_consequence_returns_common_placement(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            10: {5},
        }

        consequence = find_forcing_nets_consequence(grid, candidates)

        self.assertIsNotNone(consequence)
        assert consequence is not None
        self.assertEqual(consequence.pivot_cell, 0)
        self.assertEqual(consequence.placements, ((10, 5),))
        self.assertEqual(consequence.eliminations, ())

    def test_find_forcing_nets_consequence_returns_none_without_forcing(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            9: {4, 5},
        }

        consequence = find_forcing_nets_consequence(grid, candidates)
        self.assertIsNone(consequence)

    def test_find_forcing_nets_consequence_supports_four_candidate_pivot(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3, 4},
            1: {1},
            2: {2},
            3: {3},
        }

        consequence = find_forcing_nets_consequence(grid, candidates)

        self.assertIsNotNone(consequence)
        assert consequence is not None
        self.assertEqual(consequence.pivot_cell, 0)
        self.assertEqual(consequence.placements, ((0, 4),))

    def test_build_aic_link_graphs_skips_single_candidate_cells(self) -> None:
        strong, weak = build_aic_link_graphs({0: {1}})
        self.assertNotIn((0, 1), weak)
        self.assertEqual(strong, {})

    def test_search_aic_chain_same_cell_discontinuity_handles_empty_extras(self) -> None:
        candidates = {
            0: {1, 2},
            1: {1, 2},
        }
        start = (0, 1)
        current = (0, 2)
        strong = {start: {current}, current: {start}}
        weak = {start: {current}, current: {start}}

        elimination = _search_aic_chain(
            candidates,
            start,
            current,
            strong,
            weak,
            path=[start, (1, 1), (1, 2), current, start],
            last_edge_type="W",
            max_chain_nodes=8,
            allow_same_cell_discontinuity=True,
        )
        self.assertIsNone(elimination)

    def test_find_coloring_eliminations_skips_non_loop_components(self) -> None:
        candidates = {
            0: {1, 5},
            1: {2, 5},
            9: {3, 5},
        }
        eliminations = find_coloring_eliminations(candidates, 5, require_loop_component=True)
        self.assertEqual(eliminations, [])

    def test_find_forcing_chains_skips_non_bivalue_pivot_candidates(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 2, 3},
            2: {3, 4},
        }
        consequence = find_forcing_chains_consequence(grid, candidates)
        self.assertIsNone(consequence)

    def test_find_forcing_chains_returns_first_branch_forced_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2},
        }
        consequence = find_forcing_chains_consequence(grid, candidates)
        self.assertIsNotNone(consequence)
        assert consequence is not None
        self.assertEqual(consequence.placements, ((0, 1),))

    def test_find_forcing_chains_handles_double_invalid_branches(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1},
            9: {2},
        }
        consequence = find_forcing_chains_consequence(grid, candidates)
        self.assertIsNone(consequence)

    def test_find_forcing_chains_returns_common_placements_branch(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            10: {5},
        }
        consequence = find_forcing_chains_consequence(grid, candidates)
        self.assertIsNotNone(consequence)
        assert consequence is not None
        self.assertEqual(consequence.placements, ((10, 5),))

    def test_find_forcing_nets_skips_pivots_with_no_valid_branch(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            1: {1},
            9: {2},
            10: {3},
        }
        consequence = find_forcing_nets_consequence(grid, candidates)
        self.assertIsNone(consequence)

    def test_find_forcing_nets_returns_common_placement_branch(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3, 4},
            10: {6},
        }
        consequence = find_forcing_nets_consequence(grid, candidates)
        self.assertIsNotNone(consequence)
        assert consequence is not None
        self.assertEqual(consequence.placements, ((10, 6),))

    def test_propagate_assumption_handles_conflicting_given_cell(self) -> None:
        cells = [0] * 81
        cells[0] = 9
        result = _propagate_assumption(tuple(cells), {}, 0, 1)
        self.assertFalse(result.valid)

    def test_state_candidates_returns_none_when_allowed_restricts_all_options(self) -> None:
        cells = [0] * 81
        restricted = _state_candidates(cells, {0: set()})
        self.assertIsNone(restricted)

    def test_has_unit_digit_contradiction_detects_missing_digit_in_unit(self) -> None:
        cells = [0] * 81
        for index in range(8):
            cells[index] = index + 1
        candidates = {8: {9}}
        self.assertTrue(_has_unit_digit_contradiction(cells, candidates))
        self.assertTrue(_has_unit_digit_contradiction(cells, {}))

    def test_common_branch_helpers_cover_append_and_short_circuit_paths(self) -> None:
        base_cells = tuple([0] * 81)
        first_cells = [0] * 81
        second_cells = [0] * 81
        first_cells[4] = 7
        second_cells[4] = 7
        placements = _common_branch_placements(base_cells, first_cells, second_cells)
        self.assertEqual(placements, [(4, 7)])

        branch_a = chain_engine._ForcingBranchResult(
            valid=True, cells=first_cells, candidates={4: {7}}
        )
        one_branch = _common_placements_for_branches(base_cells, [branch_a])
        self.assertEqual(one_branch, [])
        two_branches = _common_placements_for_branches(base_cells, [branch_a, branch_a])
        self.assertEqual(two_branches, [(4, 7)])

        base_candidates = {4: {7, 8}}
        elim_single = _common_eliminations_for_branches(base_candidates, [branch_a], pivot_cell=0)
        self.assertEqual(elim_single, [])

    def test_common_branch_eliminations_detects_removed_candidate(self) -> None:
        base = {4: {7, 8}, 5: {1}}
        first = {4: {7}}
        second = {4: {7}}
        self.assertEqual(
            _common_branch_eliminations(base, first, second, pivot_cell=0),
            [(4, 8), (5, 1)],
        )

    def test_build_digit_strong_link_graph_handles_empty_digit_positions(self) -> None:
        graph = build_digit_strong_link_graph({0: {1}, 1: {2}}, 9)
        self.assertEqual(graph, {})

    def test_branch_locked_candidates_eliminations_detects_pointing(self) -> None:
        candidates = {
            0: {1, 5},
            1: {2, 5},
            3: {5, 6},
        }
        eliminations = _branch_locked_candidates_eliminations(candidates)
        self.assertEqual(eliminations, [(3, 5)])

    def test_branch_naked_pair_eliminations_detects_pair_cleanup(self) -> None:
        candidates = {
            0: {1, 2},
            1: {1, 2},
            2: {1, 2, 3},
        }
        eliminations = _branch_naked_pair_eliminations(candidates)
        self.assertEqual(eliminations, [(2, 1), (2, 2)])

    def test_apply_branch_candidate_reductions_updates_allowed_state(self) -> None:
        candidates = {
            0: {1, 2},
            1: {1, 2},
            2: {1, 2, 3},
        }
        allowed = {cell_index: set(options) for cell_index, options in candidates.items()}

        changed, invalid = _apply_branch_candidate_reductions(candidates, allowed)

        self.assertTrue(changed)
        self.assertFalse(invalid)
        self.assertEqual(candidates[2], {3})
        self.assertEqual(allowed[2], {3})

    def test_best_forcing_consequence_prefers_rank_then_scope(self) -> None:
        elimination_only = chain_engine.ForcingConsequence(
            pivot_cell=0,
            placements=(),
            eliminations=((10, 4),),
            reason="elim",
        )
        placement = chain_engine.ForcingConsequence(
            pivot_cell=1,
            placements=((1, 7),),
            eliminations=(),
            reason="place",
        )
        best = _best_forcing_consequence(None, elimination_only, rank=1)
        best = _best_forcing_consequence(best, placement, rank=2)
        self.assertIsNotNone(best)
        assert best is not None
        self.assertEqual(best[1].pivot_cell, 1)


if __name__ == "__main__":
    unittest.main()
