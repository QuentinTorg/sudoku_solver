import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.wxyz_wing import apply_wxyz_wing


class WxyzWingTechniqueTests(unittest.TestCase):
    def test_apply_wxyz_wing_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            9: {1, 4},
            10: {2, 3, 4},
            11: {1, 9},
        }

        step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "wxyz_wing")
        self.assertEqual(step.eliminations, [(11, 1)])

    def test_apply_wxyz_wing_returns_none_when_union_not_four_digits(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            9: {1, 4},
            10: {2, 3, 5},
            11: {1, 9},
        }

        step = apply_wxyz_wing(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
