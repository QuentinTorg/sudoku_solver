import unittest

from sudoku_solver.engines.uniqueness_engine import (
    find_unique_rectangle_type1_elimination,
    find_uniqueness_expansion_elimination,
    find_uniqueness_type2_elimination,
    find_uniqueness_type4_elimination,
    find_uniqueness_type5_elimination,
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
            0: {1, 2, 3},
            1: {1, 2},
            9: {1, 2},
            10: {1, 2, 3},
            11: {3, 9},
        }

        elimination = find_uniqueness_expansion_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type2_restricted")
        self.assertEqual(elimination.eliminations, ((11, 3),))

    def test_find_uniqueness_type2_elimination(self) -> None:
        candidates = {
            0: {1, 2, 3},
            1: {1, 2},
            9: {1, 2},
            10: {1, 2, 3},
            11: {3, 9},
        }

        elimination = find_uniqueness_type2_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type2_restricted")
        self.assertEqual(elimination.eliminations, ((11, 3),))

    def test_find_uniqueness_type4_elimination(self) -> None:
        candidates = {
            0: {1, 2, 4},
            3: {1, 2, 5},
            27: {1, 2},
            30: {1, 2},
        }

        elimination = find_uniqueness_type4_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type4_restricted")
        self.assertEqual(elimination.eliminations, ((0, 2), (3, 2)))

    def test_find_uniqueness_type5_elimination(self) -> None:
        candidates = {
            0: {1, 2, 4},
            3: {1, 2},
            27: {1, 2},
            30: {1, 2},
        }

        elimination = find_uniqueness_type5_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type5_restricted")
        self.assertEqual(elimination.eliminations, ((0, 2), (3, 2)))

    def test_iter_rectangle_pair_patterns_skips_when_pair_not_subset_of_all_corners(self) -> None:
        candidates = {
            0: {1, 2},
            1: {1, 2},
            9: {1, 3},
            10: {1, 2, 3},
        }
        patterns = iter_rectangle_pair_patterns(candidates)
        self.assertEqual(patterns, [])

    def test_unique_rectangle_type1_requires_single_extra_corner(self) -> None:
        candidates = {
            0: {1, 2, 3},
            3: {1, 2},
            9: {1, 2},
            12: {1, 2, 4},
        }
        self.assertIsNone(find_unique_rectangle_type1_elimination(candidates))

    def test_uniqueness_type2_requires_matching_extra_digit_and_peer_roofs(self) -> None:
        candidates_extra_mismatch = {
            0: {1, 2, 3},
            1: {1, 2},
            9: {1, 2},
            10: {1, 2, 4},
            11: {3, 4, 9},
        }
        self.assertIsNone(find_uniqueness_type2_elimination(candidates_extra_mismatch))

        candidates_not_peers = {
            0: {1, 2, 3},
            8: {1, 2},
            72: {1, 2},
            80: {1, 2, 3},
            40: {3, 9},
        }
        self.assertIsNone(find_uniqueness_type2_elimination(candidates_not_peers))

    def test_uniqueness_type2_returns_none_when_no_external_eliminations(self) -> None:
        candidates = {
            0: {1, 2, 3},
            1: {1, 2},
            9: {1, 2},
            10: {1, 2, 3},
        }
        self.assertIsNone(find_uniqueness_type2_elimination(candidates))

    def test_uniqueness_type4_requires_pure_floor_and_eliminations(self) -> None:
        candidates_floor_not_pure = {
            0: {1, 2, 4},
            3: {1, 2, 5},
            27: {1, 2, 6},
            30: {1, 2},
        }
        self.assertIsNone(find_uniqueness_type4_elimination(candidates_floor_not_pure))

        candidates_no_target_digit = {
            0: {1, 2},
            3: {1, 2},
            27: {1, 2},
            30: {1, 2},
        }
        self.assertIsNone(find_uniqueness_type4_elimination(candidates_no_target_digit))

    def test_uniqueness_type4_supports_column_shared_roof(self) -> None:
        candidates = {
            0: {1, 2, 4},
            27: {1, 2, 5},
            3: {1, 2},
            30: {1, 2},
        }
        elimination = find_uniqueness_type4_elimination(candidates)
        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type4_restricted")
        self.assertEqual(elimination.eliminations, ((0, 2), (27, 2)))

    def test_uniqueness_type5_requires_non_pair_roofs_and_eliminations(self) -> None:
        candidates_pair_roofs_only = {
            0: {1, 2},
            3: {1, 2},
            27: {1, 2},
            30: {1, 2},
        }
        self.assertIsNone(find_uniqueness_type5_elimination(candidates_pair_roofs_only))

        candidates_no_target_digit = {
            0: {1, 2, 4},
            3: {1, 2},
            27: {1, 2},
            30: {1, 2},
        }
        # remove target digit from one roof to avoid eliminations
        candidates_no_target_digit[0] = {1, 2}
        self.assertIsNone(find_uniqueness_type5_elimination(candidates_no_target_digit))

    def test_uniqueness_type5_supports_column_oriented_roofs(self) -> None:
        candidates = {
            0: {1, 2, 4},
            27: {1, 2},
            3: {1, 2},
            30: {1, 2},
        }
        elimination = find_uniqueness_type5_elimination(candidates)
        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.kind, "ur_type5_restricted")
        self.assertIn((0, 2), elimination.eliminations)
        self.assertEqual(len(elimination.eliminations), 2)


if __name__ == "__main__":
    unittest.main()
