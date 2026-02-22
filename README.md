# sudoku_solver

Human-technique-first Sudoku solver in Python, designed to be explainable, deterministic, and fully unit tested.

## Goals

- Solve Sudoku puzzles using human-style techniques (not brute-force in v1)
- Produce structured, machine-testable explanations for each solving step
- Provide both a reusable Python library and a CLI
- Maintain **100% unit test coverage**

## Current v1 Scope

The solver applies techniques in this fixed priority order:

1. Naked Single
2. Hidden Single
3. Locked Candidates (pointing/claiming)
4. Naked Pair
5. Hidden Pair

If none of the enabled techniques can make progress, the solver returns `stalled`.

### Technique guide (v1)

1. Naked Single
   A cell has exactly one remaining candidate.
   Use when: candidate pruning leaves a cell with one possible digit.
   Action: place that digit in the cell.
   Why early: it is the most direct forced move and often unlocks many follow-up constraints.

2. Hidden Single
   A digit appears as a candidate in only one cell inside a unit (row/column/box).
   Use when: scanning a unit shows a digit can go in exactly one position.
   Action: place that digit in that lone cell.
   Why after naked singles: still a forced placement, but requires unit-level counting.

3. Locked Candidates (pointing/claiming)
   Candidate positions for a digit are locked to one row/column within a box, or one box within a row/column.
   Use when: all candidates for a digit in a unit align on an intersecting unit.
   Action: eliminate that digit from peers on the intersecting unit outside the locked segment.
   Why here: no placement is required, but it creates strong eliminations for later singles/pairs.

4. Naked Pair
   Two cells in a unit share the same two candidates (and only those two).
   Use when: a unit contains exactly two cells with an identical candidate pair.
   Action: remove those two digits from candidates of other cells in that unit.
   Why later: requires pair-pattern matching and candidate bookkeeping.

5. Hidden Pair
   Two digits in a unit appear only in the same two cells, even if those cells have extra candidates.
   Use when: frequency counting in a unit shows two digits restricted to the same two positions.
   Action: keep only those two digits in those two cells; remove other candidates from those cells.
   Why last in v1: similar value to naked pair but usually requires more expensive scanning.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Pre-commit Hooks

Install and enable local hooks:

```bash
pip install -e .[dev]
pre-commit install
pre-commit install --hook-type pre-push
```

Run hooks across the repo:

```bash
pre-commit run --all-files
```

## Usage

### Python API (planned)

```python
from sudoku_solver import solve_from_string

puzzle = "53..7....6..195....98....6.8...6...34..8..6...2...1.6....28....419..5....8..79"
result = solve_from_string(puzzle)

print(result.status)
print(result.grid_string)
print(len(result.steps))
```

### CLI (planned)

```bash
python -m sudoku_solver "<81-char-puzzle>"
python -m sudoku_solver "<81-char-puzzle>" --show-steps
python -m sudoku_solver "<81-char-puzzle>" --max-steps 200
python -m sudoku_solver --puzzle-file top1465.txt
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --max-failures 2 --show-steps
```

### Benchmark Harness

Run batch performance benchmarks over a puzzle corpus:

```bash
python scripts/benchmark.py puzzles/top1465.txt
python scripts/benchmark.py puzzles/top1465.txt --limit 200 --top-slowest 10 --progress-every 500
```

## CI

- PR/push CI runs formatter/lint, mypy, unit tests, and branch coverage with a 99% minimum.
- Nightly/manual CI runs full dataset regression checks on `puzzles/top95.txt` and `puzzles/top1465.txt`, then uploads benchmark artifacts.

## Input Format

- 81-character string
- Digits `1-9` for filled cells
- `0` or `.` for empty cells

## Non-Goals for v1

- Guessing/backtracking
- Advanced techniques (triples, X-Wing, chains, etc.)
- GUI/web interface
