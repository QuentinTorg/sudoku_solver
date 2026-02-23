import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.skyscraper import apply_skyscraper


class SkyscraperTechniqueTests(unittest.TestCase):
    def test_apply_skyscraper_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {5, 8},
            6: {5, 9},
            10: {1, 5},
            16: {2, 5},
            26: {4, 5},
        }

        step = apply_skyscraper(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "skyscraper")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(26, 5)])

    def test_apply_skyscraper_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {5, 8},
            6: {5, 9},
            11: {1, 5},
            17: {2, 5},  # shifted roof breaks shared-base structure
            26: {4, 5},
        }

        step = apply_skyscraper(grid, candidates)
        self.assertIsNone(step)

    def test_apply_skyscraper_supports_column_oriented_pattern(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            19: {1, 5},
            28: {2, 5},
            20: {3, 5},
            38: {4, 5},
            36: {5, 9},
            21: {5, 7},
            39: {5, 8},
        }

        step = apply_skyscraper(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "skyscraper")
        self.assertTrue(all(digit == 5 for _, digit in step.eliminations))
        self.assertGreaterEqual(len(step.eliminations), 1)
        self.assertIn("columns", step.rationale)

    def test_apply_skyscraper_skips_when_roofs_collapse_to_same_cell(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {5, 8},
            4: {5, 9},
            10: {1, 5},
            13: {2, 5},
        }
        step = apply_skyscraper(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
