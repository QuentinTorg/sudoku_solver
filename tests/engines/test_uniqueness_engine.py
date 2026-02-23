import unittest

from sudoku_solver.engines.uniqueness_engine import (
    find_unique_rectangle_type1_elimination,
    find_uniqueness_expansion_elimination,
    iter_rectangle_pair_patterns,
)


class UniquenessEngineTests(unittest.TestCase):
    def test_iter_rectangle_pair_patterns_finds_expected_pair(self) -> None:
        candidates = {
            0: {1, 2},
            3: {1, 2},
            9: {1, 2},
            12: {1, 2, 3},
        }

        patterns = iter_rectangle_pair_patterns(candidates)

        self.assertTrue(any(pattern.pair_digits == (1, 2) for pattern in patterns))

    def test_find_unique_rectangle_type1_elimination(self) -> None:
        candidates = {
            0: {1, 2},
            3: {1, 2},
            9: {1, 2},
            12: {1, 2, 3},
        }

        elimination = find_unique_rectangle_type1_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type1")
        self.assertEqual(elimination.eliminations, ((12, 3),))

    def test_find_uniqueness_expansion_elimination(self) -> None:
        candidates = {
            0: {1, 2},
            3: {1, 2},
            27: {1, 2, 3},
            30: {1, 2, 3},
            28: {3, 9},
        }

        elimination = find_uniqueness_expansion_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type2_restricted")
        self.assertEqual(elimination.eliminations, ((28, 3),))


if __name__ == "__main__":
    unittest.main()
