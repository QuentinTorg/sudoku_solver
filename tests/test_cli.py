import unittest
from io import StringIO
from tempfile import NamedTemporaryFile
from unittest.mock import patch

from sudoku_solver.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_build_parser_handles_required_and_optional_args(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["." * 81, "--show-steps", "--max-steps", "10"])
        self.assertEqual(args.puzzle, "." * 81)
        self.assertTrue(args.show_steps)
        self.assertEqual(args.max_steps, 10)

    def test_build_parser_handles_puzzle_file_mode(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--puzzle-file", "top1465.txt"])
        self.assertEqual(args.puzzle_file, "top1465.txt")
        self.assertIsNone(args.puzzle)

    def test_main_returns_success_for_valid_input(self) -> None:
        code = main(["." * 81])
        self.assertEqual(code, 0)

    def test_main_reports_failures_from_puzzle_file(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write("534678912672195348198342567859761423426853791713924856961537284287419635345286179\n")
            tmp.write("." * 81 + "\n")
            tmp.flush()

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["--puzzle-file", tmp.name])

            output = mock_stdout.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("total: 2", output)
            self.assertIn("solved: 1", output)
            self.assertIn("stalled: 1", output)
            self.assertIn("line 2: stalled", output)

    def test_main_stops_early_when_max_failures_reached(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write("534678912672195348198342567859761423426853791713924856961537284287419635345286179\n")
            tmp.write("." * 81 + "\n")
            tmp.write("." * 81 + "\n")
            tmp.flush()

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["--puzzle-file", tmp.name, "--max-failures", "1"])

            output = mock_stdout.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("total: 2", output)
            self.assertIn("stopped_early: reached max_failures=1", output)
            self.assertIn("failures: 1", output)
            self.assertNotIn("line 3:", output)

    def test_main_shows_steps_for_failed_file_entries(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write("12345678." + "." * 72 + "\n")
            tmp.flush()

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["--puzzle-file", tmp.name, "--show-steps", "--max-failures", "1"])

            output = mock_stdout.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("steps line 1:", output)
            self.assertIn("- naked_single placements=[(8, 9)] eliminations=[]", output)


if __name__ == "__main__":
    unittest.main()
