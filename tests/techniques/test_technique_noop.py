import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_pair import apply_hidden_pair
from sudoku_solver.techniques.hidden_single import apply_hidden_single
from sudoku_solver.techniques.hidden_triple import apply_hidden_triple
from sudoku_solver.techniques.locked_candidates import apply_locked_candidates
from sudoku_solver.techniques.naked_pair import apply_naked_pair
from sudoku_solver.techniques.naked_single import apply_naked_single
from sudoku_solver.techniques.naked_triple import apply_naked_triple
from sudoku_solver.techniques.xyz_wing import apply_xyz_wing


class TechniqueNoOpTests(unittest.TestCase):
    def test_all_techniques_return_none_with_empty_candidates(self) -> None:
        grid = parse_grid("." * 81)
        self.assertIsNone(apply_naked_single(grid, {}))
        self.assertIsNone(apply_hidden_single(grid, {}))
        self.assertIsNone(apply_locked_candidates(grid, {}))
        self.assertIsNone(apply_naked_pair(grid, {}))
        self.assertIsNone(apply_hidden_pair(grid, {}))
        self.assertIsNone(apply_naked_triple(grid, {}))
        self.assertIsNone(apply_hidden_triple(grid, {}))
        self.assertIsNone(apply_xyz_wing(grid, {}))


if __name__ == "__main__":
    unittest.main()
