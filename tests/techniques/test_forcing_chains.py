import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.forcing_chains import apply_forcing_chains


class ForcingChainsTechniqueTests(unittest.TestCase):
    def test_apply_forcing_chains_returns_forced_placement(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1},
        }

        step = apply_forcing_chains(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "forcing_chains")
        self.assertEqual(step.placements, [(0, 2)])
        self.assertEqual(step.eliminations, [])

    def test_apply_forcing_chains_returns_none_when_no_forcing_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {1, 2, 3},
        }

        step = apply_forcing_chains(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
