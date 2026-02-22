import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.x_wing import apply_x_wing


class XWingTechniqueTests(unittest.TestCase):
    def test_apply_x_wing_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 7},
            16: {2, 7},
            46: {3, 7},
            52: {4, 7},
            28: {7, 9},
            79: {5, 7},
        }

        step = apply_x_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "x_wing")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(28, 7), (79, 7)])

    def test_apply_x_wing_returns_none_when_no_x_wing_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 7},
            16: {2, 7},
            46: {3, 7},
            53: {4, 7},  # shifted column breaks rectangle
            28: {7, 9},
        }

        step = apply_x_wing(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
