import unittest

from sudoku_solver.engines.als_engine import (
    find_als,
    find_als_chain_elimination,
    find_als_xz_elimination,
    find_death_blossom_elimination,
)


class AlsEngineTests(unittest.TestCase):
    def test_find_als_returns_expected_unit_based_sets(self) -> None:
        candidates = {
            0: {2, 7},
            1: {5, 7},
            9: {2, 8},
            10: {5, 8},
            19: {5, 9},
        }

        all_als = find_als(candidates)

        self.assertTrue(
            any(
                als.cells == (0, 1) and als.digits == frozenset({2, 5, 7})
                for als in all_als
            )
        )
        self.assertTrue(
            any(
                als.cells == (9, 10) and als.digits == frozenset({2, 5, 8})
                for als in all_als
            )
        )

    def test_find_als_xz_elimination_returns_expected_batch(self) -> None:
        candidates = {
            0: {2, 7},
            1: {5, 7},
            9: {2, 8},
            10: {5, 8},
            19: {5, 9},
        }

        elimination = find_als_xz_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.restricted_digit, 2)
        self.assertEqual(elimination.target_digit, 5)
        self.assertEqual(elimination.eliminations, ((19, 5),))

    def test_find_death_blossom_elimination_returns_expected_batch(self) -> None:
        candidates = {
            40: {1, 2, 3},
            37: {1, 9},
            49: {2, 9},
            46: {8, 9},
        }

        elimination = find_death_blossom_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.stem_cell, 40)
        self.assertEqual(elimination.first_petal, 37)
        self.assertEqual(elimination.second_petal, 49)
        self.assertEqual(elimination.target_digit, 9)
        self.assertEqual(elimination.eliminations, ((46, 9),))

    def test_find_als_chain_elimination_returns_expected_batch(self) -> None:
        candidates = {
            0: {1, 4},
            1: {2},
            9: {1, 5},
            10: {2, 5},
            18: {3, 4},
            19: {1, 3},
            27: {4, 7},
        }

        elimination = find_als_chain_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.target_digit, 4)
        self.assertEqual(elimination.eliminations, ((27, 4),))

    def test_find_als_chain_elimination_returns_none_when_no_rcc_chain_exists(self) -> None:
        candidates = {
            0: {1, 4},
            1: {2},
            9: {1, 5},
            10: {2, 5},
            18: {3, 4},
            19: {3, 6},
            27: {4, 7},
        }

        elimination = find_als_chain_elimination(candidates)
        self.assertIsNone(elimination)


if __name__ == "__main__":
    unittest.main()
