import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.empty_rectangle import apply_empty_rectangle


class EmptyRectangleTechniqueTests(unittest.TestCase):
    def test_apply_empty_rectangle_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            31: {2, 9},
            32: {3, 9},
            39: {1, 9},
            48: {4, 9},
            28: {5, 9},
            35: {6, 9},
            12: {7, 9},
            66: {8, 9},
            71: {1, 9},
        }

        step = apply_empty_rectangle(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "empty_rectangle")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(71, 9)])

    def test_apply_empty_rectangle_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            31: {2, 9},
            32: {3, 9},
            39: {1, 9},
            48: {4, 9},
            28: {5, 9},
            35: {6, 9},
            12: {7, 9},
            67: {8, 9},  # shifted column breaks strong link setup
            71: {1, 9},
        }

        step = apply_empty_rectangle(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
