import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.naked_pair import apply_naked_pair
from sudoku_solver.types import TechniqueName


class NakedPairTechniqueTests(unittest.TestCase):
    def test_apply_naked_pair_returns_step_when_elimination_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {idx: {1, 2, 3} for idx in range(81)}

        step = apply_naked_pair(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.NAKED_PAIR)


if __name__ == "__main__":
    unittest.main()
