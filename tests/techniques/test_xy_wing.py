import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.xy_wing import apply_xy_wing


class XyWingTechniqueTests(unittest.TestCase):
    def test_apply_xy_wing_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {1, 2},  # pivot
            37: {1, 3},  # pincer A
            13: {2, 3},  # pincer B
            10: {3, 4},  # common peer
        }

        step = apply_xy_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "xy_wing")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(10, 3)])

    def test_apply_xy_wing_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {1, 2},
            37: {1, 4},
            13: {2, 3},
            10: {3, 4},
        }

        step = apply_xy_wing(grid, candidates)
        self.assertIsNone(step)

    def test_apply_xy_wing_returns_none_when_pincers_see_each_other(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {1, 2},  # pivot
            37: {1, 3},  # pincer A
            39: {2, 3},  # pincer B (peer with pincer A)
            38: {3, 4},
        }

        step = apply_xy_wing(grid, candidates)
        self.assertIsNone(step)

    def test_apply_xy_wing_returns_none_when_no_elimination_targets(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            9: {2, 3},
        }
        step = apply_xy_wing(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
