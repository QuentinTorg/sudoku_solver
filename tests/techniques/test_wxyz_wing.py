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

    def test_apply_wxyz_wing_type1_supports_two_holder_non_restricted_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {2, 3},
            1: {2, 4},
            4: {1, 4},
            9: {1, 3},
            13: {1, 8},
        }

        step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "wxyz_wing")
        self.assertEqual(step.eliminations, [(13, 1)])
        self.assertIn("type 1", step.rationale)

    def test_apply_wxyz_wing_type2_eliminates_restricted_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            4: {2, 4},
            9: {1, 3},
            3: {2, 5, 6, 7, 8},
        }

        step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "wxyz_wing")
        self.assertEqual(step.eliminations, [(3, 2)])
        self.assertIn("type 2", step.rationale)


if __name__ == "__main__":
    unittest.main()
