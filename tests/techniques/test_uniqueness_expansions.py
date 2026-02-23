import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.uniqueness_expansions import apply_uniqueness_expansions


class UniquenessExpansionsTechniqueTests(unittest.TestCase):
    def test_apply_uniqueness_expansions_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            3: {1, 2},
            27: {1, 2, 3},
            30: {1, 2, 3},
            28: {3, 9},
        }

        step = apply_uniqueness_expansions(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "uniqueness_expansions")
        self.assertEqual(step.eliminations, [(28, 3)])

    def test_apply_uniqueness_expansions_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            3: {1, 2},
            27: {1, 2, 3},
            30: {1, 2, 4},
            28: {3, 9},
        }

        step = apply_uniqueness_expansions(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
