import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.bug_plus_one import apply_bug_plus_one


class BugPlusOneTechniqueTests(unittest.TestCase):
    def test_apply_bug_plus_one_returns_expected_placement(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},  # target
            1: {3, 4},
            2: {3, 5},
            3: {1, 4},
            4: {2, 5},
            9: {3, 4},
            18: {3, 5},
            27: {1, 4},
            36: {2, 5},
        }

        step = apply_bug_plus_one(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "bug_plus_one")
        self.assertEqual(step.placements, [(0, 3)])
        self.assertEqual(step.eliminations, [])

    def test_apply_bug_plus_one_returns_none_when_no_unique_odd_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},  # target
            1: {3, 4},
            2: {5, 6},  # row parity for digit 3 is now even
            3: {1, 4},
            4: {2, 5},
            9: {3, 4},
            18: {3, 5},
            27: {1, 4},
            36: {2, 5},
        }

        step = apply_bug_plus_one(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
