import unittest

from sudoku_solver.grid import format_grid, parse_grid


class GridTests(unittest.TestCase):
    def test_parse_grid_accepts_valid_81_char_input(self) -> None:
        puzzle = "." * 81
        grid = parse_grid(puzzle)
        self.assertEqual(len(grid.cells), 81)
        self.assertTrue(all(cell == 0 for cell in grid.cells))

    def test_parse_grid_rejects_invalid_length(self) -> None:
        with self.assertRaises(ValueError) as exc:
            parse_grid("." * 80)
        self.assertIn("81", str(exc.exception))

    def test_format_grid_round_trips(self) -> None:
        puzzle = ".....6....59.....82....8....45........3........6..3.54...325..6.................."
        grid = parse_grid(puzzle)
        self.assertEqual(format_grid(grid), puzzle)


if __name__ == "__main__":
    unittest.main()
