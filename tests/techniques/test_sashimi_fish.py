import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.sashimi_fish import apply_sashimi_fish


class SashimiFishTechniqueTests(unittest.TestCase):
    def test_apply_sashimi_fish_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 4},
            13: {2, 4},
            11: {3, 4},  # fin in row 2
            37: {5, 4},
            40: {6, 4},
            19: {4, 9},
        }

        step = apply_sashimi_fish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "sashimi_fish")
        self.assertEqual(step.eliminations, [(19, 4)])

    def test_apply_sashimi_fish_returns_none_when_no_finned_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 4},
            24: {2, 4},
            50: {3, 4},
        }

        step = apply_sashimi_fish(grid, candidates)
        self.assertIsNone(step)

    def test_apply_sashimi_fish_supports_under_populated_base_line_fish(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 7},
            9: {2, 7},
            10: {3, 7},
            27: {4, 7},
            28: {5, 7},
        }

        step = apply_sashimi_fish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "sashimi_fish")
        self.assertEqual(step.eliminations, [(27, 7), (28, 7)])


if __name__ == "__main__":
    unittest.main()
