import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_single import apply_hidden_single
from sudoku_solver.types import TechniqueName


class HiddenSingleTechniqueTests(unittest.TestCase):
    def test_apply_hidden_single_returns_step_when_move_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {0: {1, 2}, 1: {2}, 2: {1, 3}}

        step = apply_hidden_single(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.HIDDEN_SINGLE)
        assert step is not None
        self.assertEqual(step.placements, [(2, 3)])
        self.assertEqual(step.eliminations, [])
        self.assertEqual(step.affected_units, ["row1", "r1c3"])


if __name__ == "__main__":
    unittest.main()
