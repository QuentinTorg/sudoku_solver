import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.unique_rectangle import apply_unique_rectangle


class UniqueRectangleTechniqueTests(unittest.TestCase):
    def test_apply_unique_rectangle_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            3: {1, 2},
            27: {1, 2},
            30: {1, 2, 3},
        }

        step = apply_unique_rectangle(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "unique_rectangle")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(30, 3)])

    def test_apply_unique_rectangle_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            3: {1, 3},
            27: {1, 2},
            30: {1, 2, 3},
        }

        step = apply_unique_rectangle(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
