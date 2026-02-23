import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.simple_coloring import apply_simple_coloring


class SimpleColoringTechniqueTests(unittest.TestCase):
    def test_apply_simple_coloring_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 5},
            4: {2, 5},
            36: {3, 5},
            40: {4, 5},
            8: {5, 9},  # sees opposite colors in row 1
        }

        step = apply_simple_coloring(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "simple_coloring")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(8, 5)])

    def test_apply_simple_coloring_returns_none_when_no_chain_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 5},
            4: {2, 5},
            36: {3, 5},
            8: {5, 9},  # missing link through column 5/row 5
        }

        step = apply_simple_coloring(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
