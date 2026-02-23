import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.forcing_nets import apply_forcing_nets


class ForcingNetsTechniqueTests(unittest.TestCase):
    def test_apply_forcing_nets_returns_forced_placement(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            1: {1},
            2: {2},
        }

        step = apply_forcing_nets(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "forcing_nets")
        self.assertEqual(step.placements, [(0, 3)])
        self.assertEqual(step.eliminations, [])

    def test_apply_forcing_nets_returns_none_when_no_forcing_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3},
            9: {4, 5},
        }

        step = apply_forcing_nets(grid, candidates)
        self.assertIsNone(step)

    def test_apply_forcing_nets_supports_four_candidate_pivot(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2, 3, 4},
            1: {1},
            2: {2},
            3: {3},
        }

        step = apply_forcing_nets(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "forcing_nets")
        self.assertEqual(step.placements, [(0, 4)])


if __name__ == "__main__":
    unittest.main()
