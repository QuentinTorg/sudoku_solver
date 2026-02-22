import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.hidden_triple import apply_hidden_triple


class HiddenTripleTechniqueTests(unittest.TestCase):
    def test_apply_hidden_triple_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 4},
            1: {1, 3, 5},
            2: {2, 3, 6},
            3: {4, 5},
        }

        step = apply_hidden_triple(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "hidden_triple")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(0, 4), (1, 5), (2, 6)])
        self.assertEqual(step.affected_units, ["row1"])

    def test_apply_hidden_triple_returns_none_when_no_triple_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
        }

        step = apply_hidden_triple(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
