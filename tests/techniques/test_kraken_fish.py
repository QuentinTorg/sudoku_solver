import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.kraken_fish import apply_kraken_fish


class KrakenFishTechniqueTests(unittest.TestCase):
    def test_apply_kraken_fish_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 7},
            16: {2, 7},
            46: {3, 7},
            52: {4, 7},
            28: {7, 9},
            79: {5, 7},
        }

        step = apply_kraken_fish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "kraken_fish")
        self.assertEqual(step.eliminations, [(28, 7), (79, 7)])

    def test_apply_kraken_fish_returns_none_when_no_fish_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 7},
            16: {2, 7},
            46: {3, 7},
            53: {4, 7},
            28: {7, 9},
        }

        step = apply_kraken_fish(grid, candidates)
        self.assertIsNone(step)

    def test_apply_kraken_fish_supports_finned_fish_compatibility(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 4},
            13: {2, 4},
            11: {3, 4},
            37: {5, 4},
            40: {6, 4},
            19: {4, 9},
        }

        step = apply_kraken_fish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "kraken_fish")
        self.assertEqual(step.eliminations, [(19, 4)])


if __name__ == "__main__":
    unittest.main()
