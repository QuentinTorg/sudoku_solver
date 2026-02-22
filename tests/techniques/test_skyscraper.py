import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.skyscraper import apply_skyscraper


class SkyscraperTechniqueTests(unittest.TestCase):
    def test_apply_skyscraper_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {5, 8},
            6: {5, 9},
            37: {1, 5},
            44: {2, 5},
            8: {5, 6},
            42: {4, 5},
        }

        step = apply_skyscraper(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "skyscraper")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(8, 5), (42, 5)])

    def test_apply_skyscraper_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {5, 8},
            6: {5, 9},
            37: {1, 5},
            43: {2, 5},  # shifted roof breaks alignment
            8: {5, 6},
        }

        step = apply_skyscraper(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
