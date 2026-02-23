import unittest
from unittest.mock import patch

from sudoku_solver.engines.fish_engine import FishElimination
from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.swordfish import apply_swordfish


class SwordfishTechniqueTests(unittest.TestCase):
    def test_apply_swordfish_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {2, 7},
            4: {1, 7},
            28: {3, 7},
            34: {4, 7},
            55: {5, 7},
            61: {6, 7},
            10: {7, 9},
            79: {1, 7},
        }

        step = apply_swordfish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "swordfish")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(10, 7), (79, 7)])

    def test_apply_swordfish_returns_none_when_no_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {2, 7},
            4: {1, 7},
            28: {3, 7},
            35: {4, 7},
            55: {5, 7},
            61: {6, 7},
            10: {7, 9},
        }

        step = apply_swordfish(grid, candidates)
        self.assertIsNone(step)

    def test_apply_swordfish_supports_column_oriented_rationale(self) -> None:
        grid = parse_grid("." * 81)
        fish = FishElimination(
            digit=7,
            eliminations=((10, 7),),
            affected_units=("col1", "col4", "col7"),
            orientation="col",
            base_units=(0, 3, 6),
        )
        with patch(
            "sudoku_solver.techniques.swordfish.find_standard_fish_elimination", return_value=fish
        ):
            step = apply_swordfish(grid, {10: {7}})

        self.assertIsNotNone(step)
        assert step is not None
        self.assertIn("columns", step.rationale)
        self.assertEqual(step.affected_units, ["col1", "col4", "col7"])


if __name__ == "__main__":
    unittest.main()
