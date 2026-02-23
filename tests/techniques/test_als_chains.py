import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.als_chains import apply_als_chains


class AlsChainsTechniqueTests(unittest.TestCase):
    def test_apply_als_chains_returns_rcc_chain_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 4},
            1: {2},
            9: {1, 5},
            10: {2, 5},
            18: {3, 4},
            19: {1, 3},
            27: {4, 7},
        }

        step = apply_als_chains(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "als_chains")
        self.assertEqual(step.eliminations, [(27, 4)])
        self.assertIn("RCC-chain", step.rationale)

    def test_apply_als_chains_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {2, 7},
            1: {5, 7},
            9: {2, 8},
            10: {5, 8},
            19: {5, 9},
        }

        step = apply_als_chains(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "als_chains")
        self.assertEqual(step.eliminations, [(19, 5)])

    def test_apply_als_chains_returns_none_when_no_als_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {2, 7},
            1: {2, 5, 7},
            9: {2, 8},
            10: {5, 8},
            19: {5, 9},
        }

        step = apply_als_chains(grid, candidates)
        self.assertIsNone(step)

    def test_apply_als_chains_supports_four_als_path(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 4},
            1: {2},
            9: {1, 5},
            10: {3},
            18: {3, 6},
            19: {5},
            27: {6},
            29: {2, 4},
            2: {4, 7},
        }

        step = apply_als_chains(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "als_chains")
        self.assertEqual(step.eliminations, [(2, 4)])


if __name__ == "__main__":
    unittest.main()
