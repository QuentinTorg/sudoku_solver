import unittest

from sudoku_solver.candidates import get_candidates
from sudoku_solver.grid import parse_grid
from sudoku_solver.types import Grid


class CandidateTests(unittest.TestCase):
    def test_get_candidates_returns_candidates_for_empty_cells(self) -> None:
        grid = parse_grid("." * 81)
        candidates = get_candidates(grid)

        self.assertEqual(len(candidates), 81)
        self.assertEqual(candidates[0], {1, 2, 3, 4, 5, 6, 7, 8, 9})

    def test_get_candidates_excludes_fixed_cells(self) -> None:
        grid = parse_grid("1" + "." * 80)
        candidates = get_candidates(grid)

        self.assertNotIn(0, candidates)

    def test_get_candidates_rejects_invalid_grid_length(self) -> None:
        with self.assertRaises(ValueError) as exc:
            get_candidates(Grid(cells=(0,) * 80))
        self.assertIn("81", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
