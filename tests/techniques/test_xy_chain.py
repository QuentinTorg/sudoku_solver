import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.xy_chain import apply_xy_chain


class XYChainTechniqueTests(unittest.TestCase):
    def test_apply_xy_chain_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            10: {1, 3},
            9: {1, 4},  # common peer of endpoints for digit 1 elimination
        }

        step = apply_xy_chain(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "xy_chain")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(9, 1)])

    def test_apply_xy_chain_returns_none_when_no_valid_endpoint_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            10: {2, 3},
            9: {1, 4},
        }

        step = apply_xy_chain(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
