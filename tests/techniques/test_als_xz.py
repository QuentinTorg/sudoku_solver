import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.als_xz import apply_als_xz


class AlsXzTechniqueTests(unittest.TestCase):
    def test_apply_als_xz_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {2, 7},
            1: {5, 7},  # ALS A (row 1): digits {2,5,7}
            9: {2, 8},
            10: {5, 8},  # ALS B (row 2): digits {2,5,8}
            19: {5, 9},  # sees both z-cells (1 and 10)
        }

        step = apply_als_xz(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "als_xz")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(19, 5)])

    def test_apply_als_xz_returns_none_when_no_restricted_common_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {2, 7},
            1: {2, 5, 7},  # digit 2 appears twice in ALS A
            9: {2, 8},
            10: {5, 8},
            19: {5, 9},
        }

        step = apply_als_xz(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
