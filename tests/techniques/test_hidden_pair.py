import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_pair import apply_hidden_pair
from sudoku_solver.types import TechniqueName


class HiddenPairTechniqueTests(unittest.TestCase):
    def test_apply_hidden_pair_returns_step_when_elimination_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 7},
            1: {1, 2, 8},
            2: {3, 4},
            3: {3, 4, 5},
            4: {5, 6},
        }

        step = apply_hidden_pair(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.HIDDEN_PAIR)
        assert step is not None
        self.assertEqual(step.eliminations, [(0, 7), (1, 8)])
        self.assertEqual(step.affected_units, ["row1"])


if __name__ == "__main__":
    unittest.main()
