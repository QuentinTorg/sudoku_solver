import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.naked_quad import apply_naked_quad


class NakedQuadTechniqueTests(unittest.TestCase):
    def test_apply_naked_quad_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            2: {2, 4},
            3: {3, 4},
            4: {1, 5},
            5: {4, 6},
        }

        step = apply_naked_quad(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "naked_quad")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(4, 1), (5, 4)])
        self.assertEqual(step.affected_units, ["row1"])

    def test_apply_naked_quad_returns_none_when_no_quad_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            2: {2, 4},
            3: {3, 5},
            4: {6, 7},
        }

        step = apply_naked_quad(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
