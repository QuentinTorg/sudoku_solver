import unittest
from io import StringIO
from tempfile import NamedTemporaryFile
from unittest.mock import patch

from sudoku_solver.cli import build_parser, main
from sudoku_solver.types import Grid, SolveResult, SolveStatus, Step, TechniqueName


class CliTests(unittest.TestCase):
    def test_build_parser_handles_required_and_optional_args(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            ["." * 81, "--show-steps", "--show-telemetry", "--max-steps", "10"]
        )
        self.assertEqual(args.puzzle, "." * 81)
        self.assertTrue(args.show_steps)
        self.assertTrue(args.show_telemetry)
        self.assertEqual(args.max_steps, 10)

    def test_build_parser_handles_puzzle_file_mode(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--puzzle-file", "top1465.txt"])
        self.assertEqual(args.puzzle_file, "top1465.txt")
        self.assertIsNone(args.puzzle)

    def test_main_returns_success_for_valid_input(self) -> None:
        code = main(["." * 81])
        self.assertEqual(code, 0)

    def test_main_rejects_negative_max_failures(self) -> None:
        with self.assertRaises(SystemExit):
            main(["--max-failures", "-1", "." * 81])

    def test_main_rejects_missing_input(self) -> None:
        with self.assertRaises(SystemExit):
            main([])

    def test_main_rejects_both_puzzle_and_file(self) -> None:
        with self.assertRaises(SystemExit):
            main(["." * 81, "--puzzle-file", "top1465.txt"])

    def test_main_returns_error_when_file_is_unreadable(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            code = main(["--puzzle-file", "/definitely/missing.txt"])

        self.assertEqual(code, 2)
        self.assertIn("error: unable to read puzzle file", mock_stdout.getvalue())

    def test_main_reports_failures_from_puzzle_file(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write(
                "534678912672195348198342567859761423426853791713924856961537284287419635345286179\n"
            )
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
            self.assertIn(f"ending_grid: {'.' * 81}", output)

    def test_main_reports_invalid_lines_from_puzzle_file(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write("bad-puzzle\n")
            tmp.flush()

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["--puzzle-file", tmp.name, "--max-failures", "1"])

            output = mock_stdout.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("invalid: 1", output)
            self.assertIn("- line 1: invalid", output)
            self.assertNotIn("ending_grid:", output)

    def test_main_reports_invalid_solver_result_in_file_mode(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write("." * 81 + "\n")
            tmp.flush()

            fake = SolveResult(
                status=SolveStatus.INVALID,
                grid=Grid(cells=(0,) * 81),
                grid_string="." * 81,
                steps=[],
                message="forced invalid",
            )
            with patch("sudoku_solver.cli.solve_from_string", return_value=fake):
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    code = main(["--puzzle-file", tmp.name, "--max-failures", "1"])

            output = mock_stdout.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("invalid: 1", output)
            self.assertIn("forced invalid", output)
            self.assertNotIn("ending_grid:", output)

    def test_main_stops_early_when_max_failures_reached(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write(
                "534678912672195348198342567859761423426853791713924856961537284287419635345286179\n"
            )
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

    def test_main_returns_error_code_for_single_invalid_result(self) -> None:
        fake = SolveResult(
            status=SolveStatus.INVALID,
            grid=Grid(cells=(0,) * 81),
            grid_string="." * 81,
            steps=[],
            message="invalid result",
        )
        with patch("sudoku_solver.cli.solve_from_string", return_value=fake):
            code = main(["." * 81])
        self.assertEqual(code, 2)

    def test_main_omits_message_line_when_message_is_empty(self) -> None:
        fake = SolveResult(
            status=SolveStatus.SOLVED,
            grid=Grid(cells=(0,) * 81),
            grid_string="." * 81,
            steps=[
                Step(
                    technique=TechniqueName.NAKED_SINGLE,
                    placements=[(0, 1)],
                    eliminations=[],
                )
            ],
            message="",
        )
        with patch("sudoku_solver.cli.solve_from_string", return_value=fake):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["." * 81, "--show-steps", "--max-steps", "0"])

        output = mock_stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("status: solved", output)
        self.assertIn("grid: " + "." * 81, output)
        self.assertNotIn("message:", output)

    def test_main_prints_single_puzzle_steps(self) -> None:
        fake = SolveResult(
            status=SolveStatus.SOLVED,
            grid=Grid(cells=(0,) * 81),
            grid_string="." * 81,
            steps=[
                Step(
                    technique=TechniqueName.NAKED_SINGLE,
                    placements=[(0, 1)],
                    eliminations=[],
                )
            ],
            message="",
        )
        with patch("sudoku_solver.cli.solve_from_string", return_value=fake):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["." * 81, "--show-steps"])

        output = mock_stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("- naked_single placements=[(0, 1)] eliminations=[]", output)

    def test_main_prints_single_puzzle_telemetry(self) -> None:
        fake = SolveResult(
            status=SolveStatus.SOLVED,
            grid=Grid(cells=(0,) * 81),
            grid_string="." * 81,
            steps=[],
            message="",
            technique_counts={
                TechniqueName.NAKED_SINGLE: 2,
                TechniqueName.HIDDEN_SINGLE: 1,
            },
        )
        with patch("sudoku_solver.cli.solve_from_string", return_value=fake):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["." * 81, "--show-telemetry"])

        output = mock_stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("techniques:", output)
        self.assertIn("- hidden_single: 1", output)
        self.assertIn("- naked_single: 2", output)

    def test_main_ignores_comments_and_blank_lines(self) -> None:
        solved = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write("# comment line\n")
            tmp.write("\n")
            tmp.write(solved + "\n")
            tmp.flush()

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["--puzzle-file", tmp.name])

        output = mock_stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("total: 1", output)
        self.assertIn("solved: 1", output)

    def test_main_shows_steps_for_invalid_file_entries_when_requested(self) -> None:
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write("." * 81 + "\n")
            tmp.write("." * 81 + "\n")
            tmp.flush()

            fake_invalid = SolveResult(
                status=SolveStatus.INVALID,
                grid=Grid(cells=(0,) * 81),
                grid_string="." * 81,
                steps=[
                    Step(
                        technique=TechniqueName.NAKED_PAIR,
                        placements=[],
                        eliminations=[(1, 2)],
                    )
                ],
                message="forced invalid",
            )
            with patch("sudoku_solver.cli.solve_from_string", return_value=fake_invalid):
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    code = main(["--puzzle-file", tmp.name, "--show-steps"])

        output = mock_stdout.getvalue()
        self.assertEqual(code, 1)
        self.assertIn("steps line 1:", output)
        self.assertIn("steps line 2:", output)

    def test_main_prints_progress_every_1000_processed(self) -> None:
        solved = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write((solved + "\n") * 1000)
            tmp.flush()

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                code = main(["--puzzle-file", tmp.name])

            output = mock_stdout.getvalue()
            self.assertEqual(code, 0)
            self.assertIn("progress: processed=1000 solved=1000 stalled=0 invalid=0", output)
            self.assertIn("total: 1000", output)

    def test_main_prints_file_telemetry(self) -> None:
        solved = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        with NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
            tmp.write(solved + "\n")
            tmp.write(solved + "\n")
            tmp.flush()

            fake_solved = SolveResult(
                status=SolveStatus.SOLVED,
                grid=Grid(cells=tuple(int(value) for value in solved)),
                grid_string=solved,
                steps=[],
                message="",
                technique_counts={TechniqueName.NAKED_SINGLE: 1},
            )
            fake_stalled = SolveResult(
                status=SolveStatus.STALLED,
                grid=Grid(cells=(0,) * 81),
                grid_string="." * 81,
                steps=[],
                message="stalled",
                technique_counts={TechniqueName.NAKED_SINGLE: 2},
            )

            with patch(
                "sudoku_solver.cli.solve_from_string",
                side_effect=[fake_solved, fake_stalled],
            ):
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    code = main(["--puzzle-file", tmp.name, "--show-telemetry"])

        output = mock_stdout.getvalue()
        self.assertEqual(code, 1)
        self.assertIn("techniques:", output)
        self.assertIn("- naked_single: 3", output)


if __name__ == "__main__":
    unittest.main()
