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
            13: {2, 4},
            11: {3, 8},
            37: {5, 4},
            41: {6, 4},
            19: {4, 9},
        }

        step = apply_sashimi_fish(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
