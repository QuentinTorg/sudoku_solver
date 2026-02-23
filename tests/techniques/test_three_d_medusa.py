import unittest
from unittest.mock import patch

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.three_d_medusa import (
    _find_cell_bicolor_eliminations,
    _find_impossible_color,
    _find_unit_bicolor_digit_eliminations,
    apply_three_d_medusa,
)


class ThreeDMedusaTechniqueTests(unittest.TestCase):
    def test_apply_three_d_medusa_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            9: {1, 2},
            10: {1, 3},  # sees both colors of digit 1
            14: {1, 4},  # keeps row2 non-conjugate for digit 1
        }

        step = apply_three_d_medusa(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "three_d_medusa")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(10, 1)])

    def test_apply_three_d_medusa_returns_none_when_no_coloring_component(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            9: {2, 4, 5},
            10: {1, 3, 6},
            14: {1, 4, 7},
            15: {4, 6, 7},
            18: {2, 8, 9},
        }

        step = apply_three_d_medusa(grid, candidates)
        self.assertIsNone(step)

    def test_apply_three_d_medusa_handles_single_node_component(self) -> None:
        grid = parse_grid("." * 81)
        with patch(
            "sudoku_solver.techniques.three_d_medusa._build_strong_graph",
            return_value={(0, 1): set()},
        ):
            step = apply_three_d_medusa(grid, {0: {1, 2}})
        self.assertIsNone(step)

    def test_apply_three_d_medusa_prefers_impossible_color_elimination(self) -> None:
        grid = parse_grid("." * 81)
        color = {(0, 1): 0, (9, 1): 0, (1, 2): 1}
        with (
            patch(
                "sudoku_solver.techniques.three_d_medusa._build_strong_graph",
                return_value={(0, 1): {(9, 1)}, (9, 1): {(0, 1)}},
            ),
            patch("sudoku_solver.techniques.three_d_medusa._color_component", return_value=color),
            patch("sudoku_solver.techniques.three_d_medusa._find_impossible_color", return_value=0),
        ):
            step = apply_three_d_medusa(grid, {0: {1}, 9: {1}, 1: {2}})

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.eliminations, [(0, 1), (9, 1)])
        self.assertIn("color contradiction", step.rationale)

    def test_find_impossible_color_detects_cell_and_peer_conflicts(self) -> None:
        same_cell_color = {
            (0, 1): 0,
            (0, 2): 0,
        }
        self.assertEqual(_find_impossible_color(same_cell_color, {0: {1, 2}}), 0)

        peer_conflict_color = {
            (0, 1): 1,
            (1, 1): 1,
        }
        self.assertEqual(_find_impossible_color(peer_conflict_color, {0: {1}, 1: {1}}), 1)

    def test_find_cell_bicolor_eliminations_removes_non_colored_options(self) -> None:
        color = {
            (0, 1): 0,
            (0, 2): 1,
            (1, 3): 0,
        }
        component = set(color)
        candidates = {
            0: {1, 2, 4},
            1: {3, 5},
        }
        self.assertEqual(_find_cell_bicolor_eliminations(color, component, candidates), [(0, 4)])

    def test_find_unit_bicolor_digit_eliminations_removes_uncolored_unit_digit(self) -> None:
        color = {
            (0, 1): 0,
            (1, 1): 1,
            (9, 2): 0,
        }
        component = set(color)
        candidates = {
            0: {1, 3},
            1: {1, 4},
            2: {1, 5},
            9: {2, 6},
        }
        self.assertEqual(
            _find_unit_bicolor_digit_eliminations(color, component, candidates),
            [(2, 1)],
        )

    def test_apply_three_d_medusa_uses_cell_bicolor_rule_before_traps(self) -> None:
        grid = parse_grid("." * 81)
        color = {(0, 1): 0, (0, 2): 1}
        with (
            patch(
                "sudoku_solver.techniques.three_d_medusa._build_strong_graph",
                return_value={(0, 1): {(0, 2)}, (0, 2): {(0, 1)}},
            ),
            patch("sudoku_solver.techniques.three_d_medusa._color_component", return_value=color),
            patch(
                "sudoku_solver.techniques.three_d_medusa._find_impossible_color",
                return_value=None,
            ),
            patch(
                "sudoku_solver.techniques.three_d_medusa._find_color_trap_eliminations",
                return_value=[(5, 9)],
            ),
        ):
            step = apply_three_d_medusa(grid, {0: {1, 2, 3}})

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.eliminations, [(0, 3)])
        self.assertIn("bi-color cell rule", step.rationale)

    def test_apply_three_d_medusa_uses_unit_bicolor_rule(self) -> None:
        grid = parse_grid("." * 81)
        color = {(0, 1): 0, (1, 1): 1}
        with (
            patch(
                "sudoku_solver.techniques.three_d_medusa._build_strong_graph",
                return_value={(0, 1): {(1, 1)}, (1, 1): {(0, 1)}},
            ),
            patch("sudoku_solver.techniques.three_d_medusa._color_component", return_value=color),
            patch(
                "sudoku_solver.techniques.three_d_medusa._find_impossible_color",
                return_value=None,
            ),
        ):
            step = apply_three_d_medusa(
                grid,
                {
                    0: {1, 2},
                    1: {1, 3},
                    2: {1, 4},
                },
            )

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.eliminations, [(2, 1)])
        self.assertIn("bi-color unit rule", step.rationale)


if __name__ == "__main__":
    unittest.main()
