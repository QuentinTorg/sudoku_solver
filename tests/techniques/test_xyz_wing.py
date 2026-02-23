import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.xyz_wing import apply_xyz_wing


class XyzWingTechniqueTests(unittest.TestCase):
    def test_apply_xyz_wing_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 2, 3},  # pivot
            11: {1, 3},  # pincer A
            19: {2, 3},  # pincer B
            9: {3, 5},  # common peer
            20: {3, 4},  # common peer
        }

        step = apply_xyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "xyz_wing")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(9, 3), (20, 3)])

    def test_apply_xyz_wing_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 2, 3},
            11: {1, 3},
            19: {2, 4},  # shared z is missing
            9: {3, 5},
            20: {3, 4},
        }

        step = apply_xyz_wing(grid, candidates)
        self.assertIsNone(step)

    def test_apply_xyz_wing_skips_when_pincers_share_multiple_digits(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            1: {1, 2},
            9: {1, 2},
            10: {1, 2, 7},
        }
        step = apply_xyz_wing(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
