import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.exocet import _col_oriented_exocet, apply_exocet


class ExocetTechniqueTests(unittest.TestCase):
    def test_apply_exocet_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 2},  # base pair in row 1 box 1
            18: {1, 2, 3},
            19: {1, 2, 4},  # target row pair
            27: {1, 5},
            28: {2, 7},
            36: {2, 6},
            46: {1, 8},
        }

        step = apply_exocet(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "exocet")
        self.assertEqual(step.eliminations, [(27, 1), (28, 2), (36, 2), (46, 1)])

    def test_apply_exocet_returns_none_when_no_target_pair_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 2},
            18: {1, 3},  # missing digit 2
            19: {1, 2, 4},
            27: {1, 5},
        }

        step = apply_exocet(grid, candidates)
        self.assertIsNone(step)

    def test_apply_exocet_supports_column_oriented_pattern(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            9: {1, 2},  # base pair in column 1 box 1
            1: {1, 2, 3},
            10: {1, 2, 4},  # target column pair
            2: {1, 5},
            11: {2, 6},
            3: {2, 7},
            12: {1, 8},
        }

        step = apply_exocet(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "exocet")
        self.assertEqual(step.eliminations, [(2, 1), (3, 2), (11, 2), (12, 1)])

    def test_apply_exocet_skips_base_pairs_from_different_boxes(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            3: {1, 2},
            9: {1, 2},
            12: {1, 2},
        }
        self.assertIsNone(apply_exocet(grid, candidates))

    def test_col_oriented_exocet_returns_none_when_no_eliminations_exist(self) -> None:
        candidates = {
            0: {1, 2},
            9: {1, 2},
            1: {1, 2},
            10: {1, 2},
        }
        result = _col_oriented_exocet(candidates, 0, 9, {1, 2})
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
