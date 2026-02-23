import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.nice_loops import apply_nice_loops


class NiceLoopsTechniqueTests(unittest.TestCase):
    def test_apply_nice_loops_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {1, 3},
            3: {1, 6},
            4: {2, 4},
            5: {3, 5},
        }

        step = apply_nice_loops(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "nice_loops")
        self.assertEqual(step.eliminations, [(3, 1)])

    def test_apply_nice_loops_returns_none_when_no_loop_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 4},
            2: {3, 4},
        }

        step = apply_nice_loops(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
