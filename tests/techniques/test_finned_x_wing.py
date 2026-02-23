import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.finned_x_wing import apply_finned_x_wing


class FinnedXWingTechniqueTests(unittest.TestCase):
    def test_apply_finned_x_wing_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 4},
            13: {2, 4},
            11: {3, 4},  # fin in row 2
            37: {5, 4},
            40: {6, 4},
            19: {4, 9},  # elimination target in fin box / base column
        }

        step = apply_finned_x_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "finned_x_wing")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(19, 4)])

    def test_apply_finned_x_wing_returns_none_when_no_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 4},
            13: {2, 4},
            11: {3, 8},
            37: {5, 4},
            41: {6, 4},  # base columns no longer align
            19: {4, 9},
        }

        step = apply_finned_x_wing(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
