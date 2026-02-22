import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_pair import apply_hidden_pair
from sudoku_solver.types import TechniqueName


class HiddenPairTechniqueTests(unittest.TestCase):
    def test_apply_hidden_pair_returns_step_when_elimination_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {idx: {1, 2, 3} for idx in range(81)}

        step = apply_hidden_pair(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.HIDDEN_PAIR)


if __name__ == "__main__":
    unittest.main()
