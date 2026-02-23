import unittest

from sudoku_solver.engines.fish_engine import (
    _find_finned_swordfish_col_based,
    _find_finned_swordfish_row_based,
    _find_finned_x_wing_col_based,
    _find_finned_x_wing_row_based,
    _franken_eliminations,
    _franken_unit_label,
    _FrankenBaseUnit,
    find_finned_swordfish_elimination,
    find_finned_x_wing_elimination,
    find_franken_mutant_fish_elimination,
    find_standard_fish_elimination,
)


class FishEngineTests(unittest.TestCase):
    def test_find_standard_fish_elimination_for_x_wing(self) -> None:
        candidates = {
            10: {1, 7},
            16: {2, 7},
            46: {3, 7},
            52: {4, 7},
            28: {7, 9},
            79: {5, 7},
        }

        fish = find_standard_fish_elimination(
            candidates,
            7,
            size=2,
            exact_line_size=True,
        )

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((28, 7), (79, 7)))

    def test_find_finned_x_wing_elimination(self) -> None:
        candidates = {
            10: {1, 4},
            13: {2, 4},
            11: {3, 4},
            37: {5, 4},
            40: {6, 4},
            19: {4, 9},
        }

        fish = find_finned_x_wing_elimination(candidates, 4)

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((19, 4),))

    def test_find_finned_swordfish_elimination(self) -> None:
        candidates = {
            1: {5, 8},
            4: {1, 5},
            2: {3, 5},
            28: {2, 5},
            34: {4, 5},
            58: {6, 5},
            61: {7, 5},
            10: {5, 9},
        }

        fish = find_finned_swordfish_elimination(candidates, 5)

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((10, 5),))

    def test_find_franken_mutant_fish_elimination(self) -> None:
        candidates = {
            3: {1, 7},
            4: {2, 7},
            12: {3, 7},
            22: {4, 7},
            57: {5, 7},
            58: {6, 7},
        }

        fish = find_franken_mutant_fish_elimination(candidates, 7)

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((57, 7), (58, 7)))

    def test_find_standard_fish_elimination_supports_column_orientation(self) -> None:
        candidates = {
            1: {2, 7},
            4: {3, 7},
            37: {4, 7},
            40: {5, 7},
            7: {1, 7},
            43: {6, 7},
        }

        fish = find_standard_fish_elimination(
            candidates,
            7,
            size=2,
            exact_line_size=True,
        )

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.orientation, "col")
        self.assertEqual(fish.eliminations, ((7, 7), (43, 7)))
        self.assertIn("row1", fish.affected_units)

    def test_finned_x_wing_helpers_cover_continue_paths(self) -> None:
        candidates = {
            0: {1},
        }
        row_positions = {
            0: {0, 1, 2},
            1: {1, 2, 3},
        }
        self.assertIsNone(_find_finned_x_wing_row_based(candidates, 1, row_positions))

        col_positions = {
            0: {0, 1, 2},
            1: {1, 2, 3},
        }
        self.assertIsNone(_find_finned_x_wing_col_based(candidates, 1, col_positions))

    def test_finned_swordfish_helpers_cover_continue_paths(self) -> None:
        candidates = {
            0: {1},
        }
        row_positions = {
            0: {0, 1, 2, 3},
            1: {0, 1, 2, 4},
            2: {0, 1, 2, 5},
        }
        self.assertIsNone(_find_finned_swordfish_row_based(candidates, 1, row_positions))

        col_positions = {
            0: {0, 1, 2, 3},
            1: {0, 1, 2, 4},
            2: {0, 1, 2, 5},
        }
        self.assertIsNone(_find_finned_swordfish_col_based(candidates, 1, col_positions))

    def test_franken_helpers_cover_column_orientation(self) -> None:
        candidates = {
            9: {7},
            18: {7},
        }
        eliminations = _franken_eliminations(
            candidates,
            7,
            orientation="col",
            cover_lines=(1, 2),
            protected_cells=set(),
        )
        self.assertEqual(eliminations, [(9, 7), (18, 7)])
        self.assertEqual(
            _franken_unit_label(
                _FrankenBaseUnit(
                    kind="col",
                    index=1,
                    covers=frozenset({0, 1}),
                    protected_cells=frozenset(),
                )
            ),
            "col2",
        )


if __name__ == "__main__":
    unittest.main()
