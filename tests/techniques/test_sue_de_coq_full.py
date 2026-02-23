import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.sue_de_coq_full import _find_cover, apply_sue_de_coq_full


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

    def test_apply_sue_de_coq_full_supports_three_cell_generalized_intersection(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {3},
            2: {4, 5},
            3: {1},
            4: {2},
            5: {1, 6},
            6: {2, 7},
            9: {3},
            10: {4},
            11: {5},
            18: {3, 8},
            19: {4, 9},
            20: {5, 9},
        }

        step = apply_sue_de_coq_full(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "sue_de_coq_full")
        self.assertEqual(
            step.eliminations,
            [(5, 1), (6, 2), (18, 3), (19, 4), (20, 5)],
        )
        self.assertIn("Generalized Sue de Coq", step.rationale)

    def test_apply_sue_de_coq_full_generalized_requires_line_and_box_cells(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {3},
            2: {4, 5},
            3: {1},
            4: {2},
        }

        step = apply_sue_de_coq_full(grid, candidates)
        self.assertIsNone(step)

    def test_find_cover_returns_none_when_required_digits_not_coverable(self) -> None:
        candidates = {
            3: {1},
            4: {2},
            5: {1, 6},
        }

        cover = _find_cover([3, 4, 5], candidates, {1, 2, 3}, max_size=2)
        self.assertIsNone(cover)


if __name__ == "__main__":
    unittest.main()
