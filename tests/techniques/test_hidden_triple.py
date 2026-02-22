import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_triple import apply_hidden_triple


class HiddenTripleTechniqueTests(unittest.TestCase):
    def test_apply_hidden_triple_raises_not_implemented(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {idx: {1, 2, 3} for idx in range(9)}

        with self.assertRaises(NotImplementedError):
            apply_hidden_triple(grid, candidates)


if __name__ == "__main__":
    unittest.main()
