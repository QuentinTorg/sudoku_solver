import unittest

from sudoku_solver.engines.chain_engine import (
    bivalue_cells,
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
        self.assertEqual(elimination.eliminations, ((0, 3),))

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


if __name__ == "__main__":
    unittest.main()
