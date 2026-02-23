import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_quad import apply_hidden_quad


class HiddenQuadTechniqueTests(unittest.TestCase):
    def test_apply_hidden_quad_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3, 4, 8},
            1: {1, 2, 3, 4, 9},
            2: {1, 2, 3, 4, 7},
            3: {1, 2, 3, 4, 6},
            4: {5, 6},
        }

        step = apply_hidden_quad(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "hidden_quad")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(0, 8), (1, 9), (2, 7), (3, 6)])
        self.assertEqual(step.affected_units, ["row1"])

    def test_apply_hidden_quad_returns_none_when_no_quad_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 8},
            1: {1, 3, 9},
            2: {2, 3, 7},
        }

        step = apply_hidden_quad(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
