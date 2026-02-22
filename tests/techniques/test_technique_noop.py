import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_pair import apply_hidden_pair
from sudoku_solver.techniques.hidden_single import apply_hidden_single
from sudoku_solver.techniques.hidden_triple import apply_hidden_triple
from sudoku_solver.techniques.locked_candidates import apply_locked_candidates
from sudoku_solver.techniques.naked_pair import apply_naked_pair
from sudoku_solver.techniques.naked_single import apply_naked_single
from sudoku_solver.techniques.naked_triple import apply_naked_triple
from sudoku_solver.techniques.skyscraper import apply_skyscraper
from sudoku_solver.techniques.two_string_kite import apply_two_string_kite
from sudoku_solver.techniques.unique_rectangle import apply_unique_rectangle
from sudoku_solver.techniques.w_wing import apply_w_wing
from sudoku_solver.techniques.x_wing import apply_x_wing
from sudoku_solver.techniques.xy_wing import apply_xy_wing
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
        self.assertIsNone(apply_xy_wing(grid, {}))
        self.assertIsNone(apply_xyz_wing(grid, {}))
        self.assertIsNone(apply_x_wing(grid, {}))
        self.assertIsNone(apply_w_wing(grid, {}))
        self.assertIsNone(apply_two_string_kite(grid, {}))
        self.assertIsNone(apply_skyscraper(grid, {}))
        self.assertIsNone(apply_unique_rectangle(grid, {}))


if __name__ == "__main__":
    unittest.main()
