import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.w_wing import apply_w_wing


class WWingTechniqueTests(unittest.TestCase):
    def test_apply_w_wing_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 9},
            70: {1, 9},
            13: {1, 4},
            67: {1, 7},
            16: {2, 9},
            64: {3, 9},
        }

        step = apply_w_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "w_wing")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(16, 9), (64, 9)])

    def test_apply_w_wing_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 9},
            70: {1, 9},
            13: {1, 4},
            66: {1, 7},  # moved link endpoint breaks strong link
            16: {2, 9},
        }

        step = apply_w_wing(grid, candidates)
        self.assertIsNone(step)

    def test_apply_w_wing_returns_none_when_wing_sees_both_link_endpoints(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 9},  # wing A
            12: {1, 9},  # wing B (non-peer with wing A)
            1: {1, 2},  # strong-link endpoint 1 (col 2)
            10: {1, 3},  # strong-link endpoint 2 (col 2)
            3: {4, 9},  # common peer candidate
        }

        step = apply_w_wing(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
