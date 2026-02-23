import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.three_d_medusa import apply_three_d_medusa


class ThreeDMedusaTechniqueTests(unittest.TestCase):
    def test_apply_three_d_medusa_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            9: {1, 2},
            10: {1, 3},  # sees both colors of digit 1
            14: {1, 4},  # keeps row2 non-conjugate for digit 1
        }

        step = apply_three_d_medusa(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "three_d_medusa")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(10, 1)])

    def test_apply_three_d_medusa_returns_none_when_no_coloring_component(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            9: {2, 4, 5},
            10: {1, 3, 6},
            14: {1, 4, 7},
            15: {4, 6, 7},
            18: {2, 8, 9},
        }

        step = apply_three_d_medusa(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
