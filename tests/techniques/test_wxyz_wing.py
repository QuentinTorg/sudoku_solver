import unittest
from unittest.mock import patch

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.wxyz_wing import (
    _eliminations_for_digit,
    _is_two_unit_pattern,
    apply_wxyz_wing,
)


class WxyzWingTechniqueTests(unittest.TestCase):
    def test_apply_wxyz_wing_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            9: {1, 4},
            10: {2, 3, 4},
            11: {1, 9},
        }

        step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "wxyz_wing")
        self.assertEqual(step.eliminations, [(11, 1)])

    def test_apply_wxyz_wing_returns_none_when_union_not_four_digits(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            9: {1, 4},
            10: {2, 3, 5},
            11: {1, 9},
        }

        step = apply_wxyz_wing(grid, candidates)
        self.assertIsNone(step)

    def test_apply_wxyz_wing_type1_supports_two_holder_non_restricted_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {2, 3},
            1: {2, 4},
            4: {1, 4},
            9: {1, 3},
            13: {1, 8},
        }

        step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "wxyz_wing")
        self.assertEqual(step.eliminations, [(13, 1)])
        self.assertIn("type 1", step.rationale)

    def test_apply_wxyz_wing_type2_eliminates_restricted_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            4: {2, 4},
            9: {1, 3},
            3: {2, 5, 6, 7, 8},
        }

        step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "wxyz_wing")
        self.assertEqual(step.eliminations, [(3, 2)])
        self.assertIn("type 2", step.rationale)

    def test_apply_wxyz_wing_legacy_three_holder_path(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            9: {1, 4},
            10: {2, 3, 4},
            11: {1, 9},
        }

        def fake_elims(
            _candidates: dict[int, set[int]],
            _wing_cells: tuple[int, int, int, int],
            holders: list[int],
            digit: int,
        ) -> list[tuple[int, int]]:
            if len(holders) == 3 and digit == 1:
                return [(11, 1)]
            return []

        with (
            patch("sudoku_solver.techniques.wxyz_wing._is_two_unit_pattern", return_value=True),
            patch(
                "sudoku_solver.techniques.wxyz_wing._all_holders_mutually_visible",
                return_value=False,
            ),
            patch(
                "sudoku_solver.techniques.wxyz_wing._eliminations_for_digit", side_effect=fake_elims
            ),
        ):
            step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.eliminations, [(11, 1)])
        self.assertIn("legacy 3-holder", step.rationale)

    def test_apply_wxyz_wing_type2_skips_single_holder_digit(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 3},
            2: {1, 4},
            9: {2, 3, 4},
            11: {3, 8},
        }

        def fake_elims(
            _candidates: dict[int, set[int]],
            _wing_cells: tuple[int, int, int, int],
            holders: list[int],
            digit: int,
        ) -> list[tuple[int, int]]:
            if digit == 3 and len(holders) >= 2:
                return [(11, 3)]
            return []

        with patch(
            "sudoku_solver.techniques.wxyz_wing._eliminations_for_digit", side_effect=fake_elims
        ):
            step = apply_wxyz_wing(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.eliminations, [(11, 3)])
        self.assertIn("type 2", step.rationale)

    def test_wxyz_helpers_cover_empty_holders_and_non_two_unit_pattern(self) -> None:
        candidates = {
            11: {1, 9},
        }
        self.assertEqual(_eliminations_for_digit(candidates, (0, 1, 9, 10), [], 1), [])
        self.assertFalse(_is_two_unit_pattern((0, 13, 26, 39)))


if __name__ == "__main__":
    unittest.main()
