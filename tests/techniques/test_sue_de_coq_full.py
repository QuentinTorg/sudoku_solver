import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.sue_de_coq_full import apply_sue_de_coq_full


class SueDeCoqFullTechniqueTests(unittest.TestCase):
    def test_apply_sue_de_coq_full_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {3, 4},
            3: {1},
            4: {2},
            5: {1, 5},
            6: {2, 6},
            9: {3},
            10: {4},
            11: {3, 7},
            18: {4, 8},
        }

        step = apply_sue_de_coq_full(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "sue_de_coq_full")
        self.assertEqual(step.eliminations, [(5, 1), (6, 2), (11, 3), (18, 4)])

    def test_apply_sue_de_coq_full_returns_none_when_no_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            3: {1},
            4: {2},
            9: {3},
            10: {4},
        }

        step = apply_sue_de_coq_full(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
