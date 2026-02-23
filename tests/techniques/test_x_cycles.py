import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.x_cycles import apply_x_cycles


class XCyclesTechniqueTests(unittest.TestCase):
    def test_apply_x_cycles_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {2, 5},
            3: {4, 5},
            5: {5, 6},
            28: {5, 9},
            30: {5, 7},
            41: {2, 5},
        }

        step = apply_x_cycles(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "x_cycles")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(1, 5), (5, 5), (30, 5)])

    def test_apply_x_cycles_returns_none_when_no_loop_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {2, 5},
            3: {4, 5},
            5: {5, 6},
            28: {5, 9},
            41: {2, 5},  # remove one cycle cell
        }

        step = apply_x_cycles(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
