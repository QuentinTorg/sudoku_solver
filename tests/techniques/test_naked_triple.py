import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.naked_triple import apply_naked_triple


class NakedTripleTechniqueTests(unittest.TestCase):
    def test_apply_naked_triple_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            2: {2, 3},
            3: {1, 2, 4},
            4: {4, 5},
        }

        step = apply_naked_triple(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "naked_triple")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(3, 1), (3, 2)])
        self.assertEqual(step.affected_units, ["row1"])

    def test_apply_naked_triple_returns_none_when_no_triple_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            2: {2, 4},
            3: {3, 4},
        }

        step = apply_naked_triple(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
