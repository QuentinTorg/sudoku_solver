import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.als_chains import apply_als_chains


class AlsChainsTechniqueTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
