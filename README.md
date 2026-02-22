# sudoku_solver

[![CI](https://img.shields.io/github/actions/workflow/status/QuentinTorg/sudoku_solver/ci.yml?branch=main&label=ci)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/ci.yml)
[![Dataset Regression](https://img.shields.io/github/actions/workflow/status/QuentinTorg/sudoku_solver/dataset.yml?branch=main&label=dataset)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/dataset.yml)
[![Coverage Gate](https://img.shields.io/badge/coverage-%E2%89%A599%25-brightgreen)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/ci.yml)

Explainable Sudoku solver in Python with human-style techniques, step-by-step reasoning, CLI and library APIs, benchmarking tools, and CI quality gates.

## What This Project Does

- Solves 9x9 Sudoku puzzles from a single puzzle string or a puzzle file.
- Applies a deterministic sequence of human-style techniques and records each applied step.
- Falls back to a bounded uniqueness search when technique progress stops.
- Reports structured outcomes (`solved`, `stalled`, `invalid`), difficulty rating, and optional telemetry.
- Includes unit tests, property tests (when `hypothesis` is installed), linting, typing checks, and coverage reporting.

## Feature Summary

- Techniques implemented:
  1. Naked Single
  2. Hidden Single
  3. Locked Candidates (pointing/claiming)
  4. Naked Pair
  5. Hidden Pair
  6. Naked Triple
  7. Hidden Triple
  8. XYZ-Wing
- Fallback search:
  Uniqueness-aware backtracking is used only when no configured technique can advance the grid.
- Result metadata:
  `steps`, `technique_counts`, and `difficulty` are returned for every solve attempt.

## Sudoku Terms (Quick Glossary)

- `Cell`: one square in the 9x9 grid.
- `Row`: horizontal set of 9 cells.
- `Column`: vertical set of 9 cells.
- `Box`: one 3x3 subgrid.
- `Unit`: any row, column, or box.
- `Candidate`: a digit that is still legal for an empty cell.
- `Peer`: a cell sharing a row, column, or box with another cell.
- `Placement`: writing a final digit into a cell.
- `Elimination`: removing a candidate from a cell.

## Technique Guide

Technique order is fixed by default and affects which step is chosen first.
In the example grids below, blank cells are intentionally left empty because they are not relevant to the pattern.

### 1. Naked Single
Definition:
A cell has exactly one remaining candidate, so that digit must be placed.

Minimal scenario (r4c5 is forced):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  | 4 |  |  |  |  |
| r2 |  |  |  |  | 6 |  |  |  |  |
| r3 |  |  |  |  | 2 |  |  |  |  |
| r4 | 8 | 5 | 9 | 1 | `{7}` | 4 | 3 | 2 | 6 |
| r5 |  |  |  |  | 3 |  |  |  |  |
| r6 |  |  |  |  | 5 |  |  |  |  |
| r7 |  |  |  |  | 1 |  |  |  |  |
| r8 |  |  |  |  | 8 |  |  |  |  |
| r9 |  |  |  |  | 9 |  |  |  |  |

Action:
Place `7` at `r4c5`.

### 2. Hidden Single
Definition:
In one unit, a digit appears as a candidate in exactly one cell.

Minimal scenario (row 2):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | 5 |  |  |  |  |  |  |  |  |
| r2 | `{1,4}` | 8 | `{2,4}` | 6 | 9 | 5 | `{3,4}` | 7 | 2 |
| r3 | 7 |  |  |  |  |  |  |  |  |
| r4 | 9 |  |  |  |  |  |  |  |  |
| r5 | 3 |  |  |  |  |  |  |  |  |
| r6 | 6 |  |  |  |  |  |  |  |  |
| r7 | 2 |  |  |  |  |  |  |  |  |
| r8 | 8 |  |  |  |  |  |  |  |  |
| r9 | 4 |  |  |  |  |  |  |  |  |

Observation:
Digit `1` appears only in `r2c1` in this row.

Action:
Place `1` at `r2c1`.

### 3. Locked Candidates (Pointing/Claiming)
Definition:
A digit's candidates are confined to an intersection of units, allowing eliminations in the overlapping unit.

Minimal scenario (pointing from box 1 to row 1):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{2,5}` | `{5,8}` | 1 | `{5,7}` | 6 | 4 | 2 | `{5,9}` | 3 |
| r2 | `{2,7}` | 9 | 3 |  |  |  |  |  |  |
| r3 | 4 | `{6,7}` | 8 |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
In box 1, candidate `5` appears only on row 1.

Action:
Eliminate `5` from `r1c4` and `r1c8`.

### 4. Naked Pair
Definition:
Two cells in the same unit contain the same two candidates and no others.

Minimal scenario (row 5):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 | 4 | `{2,8}` | 6 | `{1,2,9}` | 5 | 7 | `{2,8}` | 1 | `{3,8}` |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action:
Eliminate `2` from `r5c4` and eliminate `8` from `r5c9`.

### 5. Hidden Pair
Definition:
Two digits in a unit can appear only in the same two cells, so those two cells must contain those two digits.

Minimal scenario (row 6):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 | 9 | `{1,3,7}` | `{2,4}` | 5 | `{1,8}` | 6 | `{2,8}` | 4 | `{3,6,7}` |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
Digits `3` and `7` are restricted to `r6c2` and `r6c9`.

Action:
Reduce `r6c2` and `r6c9` to `{3,7}`.

### 6. Naked Triple
Definition:
Three cells in one unit contain candidates that together are exactly three digits.

Minimal scenario (column 4):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  | `{1,4}` |  |  |  |  |  |
| r2 |  |  |  | 6 |  |  |  |  |  |
| r3 |  |  |  | `{2,4,9}` |  |  |  |  |  |
| r4 |  |  |  | 3 |  |  |  |  |  |
| r5 |  |  |  | 8 |  |  |  |  |  |
| r6 |  |  |  | `{1,9}` |  |  |  |  |  |
| r7 |  |  |  | 5 |  |  |  |  |  |
| r8 |  |  |  | `{4,9}` |  |  |  |  |  |
| r9 |  |  |  | 7 |  |  |  |  |  |

Observation:
The triple cells must take digits `1`, `4`, and `9` in some order.

Action:
Eliminate `4` and `9` from `r3c4`.

### 7. Hidden Triple
Definition:
Three digits in a unit appear only in the same three cells (even if those cells have extra candidates).

Minimal scenario (box 5):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  | `{1,2,5,8}` | 6 | `{1,4}` |  |  |  |
| r5 |  |  |  | 9 | `{2,5,7,8}` | 3 |  |  |  |
| r6 |  |  |  | `{1,7}` | 4 | `{2,3,5,8}` |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action:
Reduce the three cells to subsets of `{2,5,8}` only.

### 8. XYZ-Wing
Definition:
A 3-candidate pivot and two 2-candidate pincers force a shared digit that can be eliminated from common peers.

Minimal scenario:

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  | `{1,6}` | `{1,3}` | 8 |  |  |  |
| r5 |  |  |  | `{1,2}` | `{1,2,3}` | 7 |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
Pivot is `r5c5={1,2,3}`, pincers are `r5c4={1,2}` and `r4c5={1,3}`.
Digit `1` is shared by both pincers, so any cell that sees all three (for example `r4c4`) cannot keep `1`.

Action:
Eliminate `1` from common peers of pivot + both pincers (for example from `r4c4`).

## Result Model

`solve_from_string()` returns a `SolveResult` with:

- `status`: `solved`, `stalled`, or `invalid`
- `grid_string`: final grid string
- `steps`: ordered list of applied steps
- `technique_counts`: count per technique used
- `difficulty`: `easy`, `medium`, `hard`, `expert`, or `unsolved`
- `message`: contextual message

Difficulty is derived from the hardest technique used (or fallback search usage).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Install developer tooling:

```bash
pip install -e .[dev]
```

## Running

### Python API

```python
from sudoku_solver import solve_from_string

puzzle = "53..7....6..195....98....6.8...6...34..8..6...2...1.6....28....419..5....8..79"
result = solve_from_string(puzzle)

print(result.status)
print(result.difficulty)
print(result.grid_string)
print(result.technique_counts)
```

### CLI

Single puzzle:

```bash
python -m sudoku_solver "<81-char-puzzle>"
python -m sudoku_solver "<81-char-puzzle>" --show-steps
python -m sudoku_solver "<81-char-puzzle>" --show-telemetry
python -m sudoku_solver "<81-char-puzzle>" --max-steps 200
```

Puzzle file mode:

```bash
python -m sudoku_solver --puzzle-file puzzles/top1465.txt
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --max-failures 2
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --show-steps --show-telemetry
```

### Benchmark Harness

```bash
python scripts/benchmark.py puzzles/top1465.txt
python scripts/benchmark.py puzzles/top1465.txt --limit 200 --top-slowest 10 --progress-every 500
```

## Input Format

- Exactly 81 characters.
- `1-9` for filled cells.
- `.` or `0` for empty cells.

## Repository Structure

- `sudoku_solver/grid.py`: parsing, formatting, and givens validation.
- `sudoku_solver/candidates.py`: candidate generation for empty cells.
- `sudoku_solver/units.py`: row/column/box helpers and peer calculation.
- `sudoku_solver/techniques/`: individual technique implementations.
- `sudoku_solver/solver.py`: orchestration loop, step application, fallback search, difficulty classification.
- `sudoku_solver/cli.py`: CLI parser, single/file runners, progress and reporting output.
- `sudoku_solver/types.py`: core dataclasses/enums (`Grid`, `Step`, `SolveResult`, etc.).
- `scripts/benchmark.py`: dataset timing and throughput reporting.
- `tests/`: unit, internal, regression, technique, and property tests.
- `puzzles/`: bundled puzzle corpora.

## Code Data Flow

1. Parse input (`parse_grid`) and validate puzzle consistency.
2. Build candidate sets for empty cells (`get_candidates`).
3. Iterate technique functions in fixed order and request one `Step` at a time.
4. Apply step placements/eliminations (`_apply_step`) and update state.
5. Repeat until solved or no technique can progress.
6. If stalled by techniques, run uniqueness-aware fallback search.
7. Return `SolveResult` with final status, steps, telemetry, and difficulty.

## Quality Checks

### Pre-commit hooks

```bash
pre-commit install
pre-commit install --hook-type pre-push
pre-commit run --all-files
```

### Local checks

```bash
ruff format --check .
ruff check .
mypy
python -m unittest discover -s tests -t . -v
python -m coverage run --branch --source=sudoku_solver -m unittest discover -s tests -t .
python -m coverage report -m
```

## CI

- `CI` workflow (`.github/workflows/ci.yml`) runs on pull requests and pushes to `main`:
  - Ruff format check
  - Ruff lint
  - Mypy type checking
  - Unit tests
  - Branch coverage gate (minimum 99%)
- `Dataset Regression` workflow (`.github/workflows/dataset.yml`) runs on pushes to `main` and manual dispatch:
  - Dataset regression on `puzzles/top95.txt` and `puzzles/top1465.txt`
  - Benchmark artifact generation

## Contributing

1. Create a branch for your change.
2. Install dev dependencies: `pip install -e .[dev]`.
3. Enable hooks: `pre-commit install` and `pre-commit install --hook-type pre-push`.
4. Add or update tests with any code changes.
5. Run local checks before opening a PR.
6. Open a PR with a clear description of behavior changes and test evidence.

Recommended contribution pattern:

- Keep technique changes isolated per PR when possible.
- Include at least one regression test for each bug fix.
- If adding a technique, document it in this README and add focused tests under `tests/techniques/`.
