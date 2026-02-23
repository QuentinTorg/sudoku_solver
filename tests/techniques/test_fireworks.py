import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.fireworks import apply_fireworks


class FireworksTechniqueTests(unittest.TestCase):
    def test_apply_fireworks_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {2, 5},  # pivot r5c5
            41: {5, 7},  # row remote
            4: {5, 8},  # column remote
            5: {5, 9},  # common peer of remotes
            6: {5, 6},  # keep row 1 non-conjugate for pivot 4
            8: {5, 4},  # keep row 1 non-conjugate for pivot 4
        }

        step = apply_fireworks(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "fireworks")
        self.assertEqual(step.eliminations, [(5, 5)])

    def test_apply_fireworks_returns_none_when_row_col_links_not_conjugate(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            40: {2, 5},
            41: {5, 7},
            4: {5, 8},
            42: {5, 6},  # extra row-5 candidate breaks row conjugate
            5: {5, 9},
            6: {5, 6},
            8: {5, 4},
        }

        step = apply_fireworks(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
