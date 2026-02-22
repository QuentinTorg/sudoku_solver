import unittest

from sudoku_solver.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_build_parser_handles_required_and_optional_args(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["." * 81, "--show-steps", "--max-steps", "10"])
        self.assertEqual(args.puzzle, "." * 81)
        self.assertTrue(args.show_steps)
        self.assertEqual(args.max_steps, 10)

    def test_main_returns_success_for_valid_input(self) -> None:
        code = main(["." * 81])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
