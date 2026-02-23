import unittest
from unittest.mock import patch

from sudoku_solver.engines.fish_engine import FishElimination
from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.squirmbag import apply_squirmbag


class SquirmbagTechniqueTests(unittest.TestCase):
    def test_apply_squirmbag_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates: dict[int, set[int]] = {}
        for row in range(5):
            for col in range(5):
                candidates[row * 9 + col] = {7}
        candidates[45] = {7, 9}

        step = apply_squirmbag(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "squirmbag")
        self.assertEqual(step.eliminations, [(45, 7)])

    def test_apply_squirmbag_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates: dict[int, set[int]] = {}
        for row in range(4):
            for col in range(5):
                candidates[row * 9 + col] = {7}
        candidates[45] = {7, 9}

        step = apply_squirmbag(grid, candidates)
        self.assertIsNone(step)

    def test_apply_squirmbag_supports_column_oriented_rationale(self) -> None:
        grid = parse_grid("." * 81)
        fish = FishElimination(
            digit=7,
            eliminations=((45, 7),),
            affected_units=("col1", "col2", "col3", "col4", "col5"),
            orientation="col",
            base_units=(0, 1, 2, 3, 4),
        )
        with patch(
            "sudoku_solver.techniques.squirmbag.find_standard_fish_elimination", return_value=fish
        ):
            step = apply_squirmbag(grid, {45: {7, 9}})

        self.assertIsNotNone(step)
        assert step is not None
        self.assertIn("columns", step.rationale)
        self.assertEqual(step.affected_units, ["col1", "col2", "col3", "col4", "col5"])


if __name__ == "__main__":
    unittest.main()
