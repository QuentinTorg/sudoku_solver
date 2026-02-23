import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.death_blossom import apply_death_blossom


class DeathBlossomTechniqueTests(unittest.TestCase):
    def test_apply_death_blossom_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {1, 2, 3},  # stem
            37: {1, 9},  # petal A
            49: {2, 9},  # petal B
            46: {8, 9},  # common peer of petals
        }

        step = apply_death_blossom(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "death_blossom")
        self.assertEqual(step.eliminations, [(46, 9)])

    def test_apply_death_blossom_returns_none_when_petals_do_not_share_external(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {1, 2, 3},
            37: {1, 9},
            49: {2, 8},
            46: {8, 9},
        }

        step = apply_death_blossom(grid, candidates)
        self.assertIsNone(step)

    def test_apply_death_blossom_supports_multi_petal_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {1, 2, 3},
            30: {1, 9},
            41: {2, 9},
            49: {3, 9},
            32: {8, 9},
        }

        step = apply_death_blossom(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "death_blossom")
        self.assertEqual(step.eliminations, [(32, 9)])


if __name__ == "__main__":
    unittest.main()
