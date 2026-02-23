import unittest
from unittest.mock import patch

from sudoku_solver.engines.chain_engine import AicElimination
from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.grouped_aic import apply_grouped_aic


class GroupedAicTechniqueTests(unittest.TestCase):
    def test_apply_grouped_aic_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {1, 3},
            3: {1, 6},
            4: {2, 4},
            5: {3, 5},
        }

        step = apply_grouped_aic(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "grouped_aic")
        self.assertEqual(step.eliminations, [(3, 1)])

    def test_apply_grouped_aic_returns_none_when_no_chain_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 4},
            2: {3, 4},
        }

        step = apply_grouped_aic(grid, candidates)
        self.assertIsNone(step)

    def test_apply_grouped_aic_uses_same_cell_discontinuity_rationale(self) -> None:
        grid = parse_grid("." * 81)
        elimination = AicElimination(
            digit=1,
            start_cell=0,
            end_cell=0,
            eliminations=((0, 3),),
            pattern="same_cell_discontinuity",
        )

        with patch(
            "sudoku_solver.techniques.grouped_aic.find_aic_elimination",
            return_value=elimination,
        ):
            step = apply_grouped_aic(grid, {0: {1, 2, 3}})

        self.assertIsNotNone(step)
        assert step is not None
        self.assertIn("discontinuous same-cell loop", step.rationale)


if __name__ == "__main__":
    unittest.main()
