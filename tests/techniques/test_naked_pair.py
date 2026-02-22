import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.naked_pair import apply_naked_pair
from sudoku_solver.types import TechniqueName


class NakedPairTechniqueTests(unittest.TestCase):
    def test_apply_naked_pair_returns_step_when_elimination_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 2},
            2: {1, 2, 3},
            3: {2, 4},
            4: {4, 5},
        }

        step = apply_naked_pair(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.NAKED_PAIR)
        assert step is not None
        self.assertEqual(step.eliminations, [(2, 1), (2, 2), (3, 2)])
        self.assertEqual(step.affected_units, ["row1"])


if __name__ == "__main__":
    unittest.main()
