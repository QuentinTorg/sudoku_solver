import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.aic import apply_aic


class AicTechniqueTests(unittest.TestCase):
    def test_apply_aic_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {1, 3},
            3: {1, 6},  # common peer for endpoint digit 1
            4: {2, 4},  # forces weak link on digit 2
            5: {3, 5},  # forces weak link on digit 3
        }

        step = apply_aic(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "aic")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(3, 1)])

    def test_apply_aic_returns_none_when_chain_is_broken(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {3, 4},  # endpoint digit 1 removed
            3: {1, 6},
        }

        step = apply_aic(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
