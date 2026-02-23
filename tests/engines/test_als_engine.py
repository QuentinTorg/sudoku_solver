import unittest

from sudoku_solver.engines.als_engine import (
    Als,
    DeathBlossomElimination,
    _als_cells_disjoint,
    _restricted_link_exists,
    _target_digit_eliminations,
    find_als,
    find_als_chain_elimination,
    find_als_xy_wing_elimination,
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
            any(als.cells == (0, 1) and als.digits == frozenset({2, 5, 7}) for als in all_als)
        )
        self.assertTrue(
            any(als.cells == (9, 10) and als.digits == frozenset({2, 5, 8}) for als in all_als)
        )

    def test_find_als_supports_size_four_when_requested(self) -> None:
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {3, 4},
            3: {4, 5},
        }
        all_als = find_als(candidates, sizes=(4,))
        self.assertTrue(
            any(
                als.cells == (0, 1, 2, 3) and als.digits == frozenset({1, 2, 3, 4, 5})
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

    def test_find_death_blossom_elimination_supports_multi_petal_stem(self) -> None:
        candidates = {
            40: {1, 2, 3},
            30: {1, 9},
            41: {2, 9},
            49: {3, 9},
            32: {8, 9},
        }

        elimination = find_death_blossom_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.stem_cell, 40)
        self.assertEqual(elimination.petals, (30, 41, 49))
        self.assertEqual(elimination.target_digit, 9)
        self.assertEqual(elimination.eliminations, ((32, 9),))

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

    def test_find_als_chain_elimination_supports_four_als_paths(self) -> None:
        candidates = {
            0: {1, 4},
            1: {2},
            9: {1, 5},
            10: {3},
            18: {3, 6},
            19: {5},
            27: {6},
            29: {2, 4},
            2: {4, 7},
        }

        elimination = find_als_chain_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.target_digit, 4)
        self.assertEqual(elimination.eliminations, ((2, 4),))

    def test_find_als_xy_wing_elimination_returns_expected_batch(self) -> None:
        candidates = {
            0: {1, 9},
            1: {2, 9},
            9: {1, 4},
            10: {4, 7},
            19: {2, 5},
            20: {5, 7},
            11: {7, 8},
        }

        elimination = find_als_xy_wing_elimination(candidates)

        self.assertIsNotNone(elimination)
        assert elimination is not None
        self.assertEqual(elimination.target_digit, 7)
        self.assertEqual(elimination.eliminations, ((11, 7),))

    def test_death_blossom_properties_expose_first_two_petals(self) -> None:
        elimination = DeathBlossomElimination(
            stem_cell=40,
            petals=(30, 41, 49),
            target_digit=9,
            eliminations=((32, 9),),
        )
        self.assertEqual(elimination.first_petal, 30)
        self.assertEqual(elimination.second_petal, 41)

    def test_find_als_chain_returns_none_when_no_links_exist(self) -> None:
        candidates = {
            0: {1, 2},
            10: {3, 4},
            20: {5, 6},
        }
        self.assertIsNone(find_als_chain_elimination(candidates))

    def test_als_helper_predicates_cover_false_paths(self) -> None:
        first = Als(cells=(0, 1), digits=frozenset({1, 2, 3}), unit_name="row1")
        second = Als(cells=(1, 2), digits=frozenset({1, 4, 5}), unit_name="row1")
        self.assertFalse(_als_cells_disjoint(first, second))

        candidates = {
            0: {1, 2},
            1: {1, 2, 3},
            2: {1, 3, 4},
        }
        self.assertFalse(_restricted_link_exists(candidates, first, second, 1))

    def test_target_digit_eliminations_handles_missing_target_cells(self) -> None:
        first = Als(cells=(0, 1), digits=frozenset({1, 2, 3}), unit_name="row1")
        second = Als(cells=(9, 10), digits=frozenset({1, 2, 4}), unit_name="row2")
        candidates = {
            0: {1, 2},
            1: {2, 3},
            9: {1, 2},
            10: {1, 4},
            11: {3, 4},
        }
        self.assertEqual(_target_digit_eliminations(candidates, first, second, 5), [])

    def test_find_death_blossom_skips_invalid_stem_and_external_shapes(self) -> None:
        candidates = {
            0: {1},
            1: {1, 2},
            9: {1, 2},
            10: {2, 3, 4},
        }
        self.assertIsNone(find_death_blossom_elimination(candidates))


if __name__ == "__main__":
    unittest.main()
