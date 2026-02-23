# sudoku_solver

[![CI](https://img.shields.io/github/actions/workflow/status/QuentinTorg/sudoku_solver/ci.yml?branch=main&label=ci)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/ci.yml)
[![Dataset Regression](https://img.shields.io/github/actions/workflow/status/QuentinTorg/sudoku_solver/dataset.yml?branch=main&label=dataset)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/dataset.yml)
[![Coverage Gate](https://img.shields.io/badge/coverage-%E2%89%A599%25-brightgreen)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/ci.yml)

Explainable Sudoku solver in Python with human-style techniques, step-by-step reasoning, CLI and library APIs, benchmarking tools, and CI quality gates.

## What This Project Does

- Solves 9x9 Sudoku puzzles from a single puzzle string or a puzzle file.
- Applies a deterministic sequence of human-style techniques and records each applied step.
- Can optionally use a bounded uniqueness search after human techniques stall.
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
  8. XY-Wing
  9. XYZ-Wing
  10. X-Wing
  11. Naked Quad
  12. Hidden Quad
  13. W-Wing
  14. Swordfish
  15. Jellyfish
  16. Simple Coloring
  17. 3D Medusa (restricted)
  18. AIC (restricted)
  19. X-Cycles
  20. XY-Chain
  21. ALS-XZ (restricted)
  22. Sue de Coq (restricted)
  23. BUG+1
  24. Finned X-Wing / Sashimi X-Wing
  25. Finned Swordfish
  26. Empty Rectangle
  27. Remote Pairs
  28. Two-String Kite
  29. Skyscraper
  30. Unique Rectangle
  31. Grouped AIC (restricted)
  32. Nice Loops (restricted)
  33. ALS Chains (restricted)
  34. Death Blossom (restricted)
  35. Uniqueness Expansions (restricted)
  36. Fireworks (restricted)
  37. WXYZ-Wing (restricted)
  38. Exocet (very restricted)
  39. Sue de Coq Full/Generalized (restricted)
  40. Kraken Fish (restricted)
  41. Sashimi Fish (restricted)
- Default technique order:
  Fast/core techniques plus `xy_wing`, `xyz_wing`, `x_wing`, `w_wing`,
  `naked_quad`, `hidden_quad`, `swordfish`, `jellyfish`, `bug_plus_one`,
  `simple_coloring`, `three_d_medusa`, `aic`, `x_cycles`, and `xy_chain`
  run by default.
  More expensive techniques (`als_xz`, `sue_de_coq`, `grouped_aic`,
  `nice_loops`, `als_chains`, `death_blossom`, `uniqueness_expansions`,
  `fireworks`, `wxyz_wing`, `exocet`, `sue_de_coq_full`, `kraken_fish`,
  `sashimi_fish`, `finned_x_wing`, `finned_swordfish`, `empty_rectangle`,
  `remote_pairs`, `two_string_kite`, `skyscraper`, `unique_rectangle`) are
  available through API `techniques=[...]` selection.
- Advanced-technique safety:
  High-risk eliminations are conservatively validated against solution
  existence checks before they are applied, reducing false-positive
  eliminations that can otherwise produce invalid states.
- Fallback search:
  Uniqueness-aware backtracking is available when no configured technique can advance the grid.
  It is disabled by default; use `allow_fallback_search=True` (API) or
  `--allow-fallback-search` (CLI) to enable it.
- Result metadata:
  `steps`, `technique_counts`, `difficulty`, and `used_fallback_search` are returned for every solve attempt.

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

### 9. XY-Wing
Definition:
A 2-candidate pivot and two 2-candidate pincers force elimination of one shared digit.

Minimal scenario:

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  | `{3,4}` |  |  | `{2,3}` |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  | `{1,3}` |  |  | `{1,2}` |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
Pivot is `r5c5={1,2}`. Pincers `r5c2={1,3}` and `r2c5={2,3}` force digit `3`
to be false in cells that see both pincers.

Action:
Eliminate `3` from `r2c2`.

### 10. X-Wing
Definition:
For one digit, two rows share the same two candidate columns (or vice versa), so
that digit can be removed from those columns in other rows.

Minimal scenario (digit `7`):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  | `{1,7}` |  |  |  |  |  | `{2,7}` |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  | `{7,9}` |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  | `{3,7}` |  |  |  |  |  | `{4,7}` |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  | `{5,7}` |  |

Observation:
Rows 2 and 6 place digit `7` only in columns 2 and 8.

Action:
Eliminate `7` from `r4c2` and `r9c8`.

### 11. W-Wing
Definition:
Two matching bivalue cells are connected by a strong link on one digit, allowing
elimination of the other digit from their shared peers.

Minimal scenario:

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  | `{1,9}` |  |  | `{1,4}` |  |  | `{2,9}` |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  | `{3,9}` |  |  | `{1,7}` |  |  |  |  |
| r8 |  |  |  |  |  |  |  | `{1,9}` |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
`r2c2` and `r8c8` are both `{1,9}`. A strong link on digit `1` in column 5
connects peers of those cells.

Action:
Eliminate `9` from common peers (`r2c8` and `r7c2` in this example).

### 12. Two-String Kite
Definition:
A strong row link and a strong column link for the same digit combine through one
shared box endpoint to eliminate that digit at a crossing cell.

Minimal scenario (digit `5`):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  | `{3,5}` |  |  |  |  |  |  |
| r2 |  | `{1,5}` |  |  |  |  |  | `{2,5}` |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  | `{4,5}` |  |  |  |  | `{5,9}` |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
Row 2 and column 3 each give a strong link for digit `5`, and one endpoint pair
shares box 1.

Action:
Eliminate `5` from `r7c8`.

### 13. Skyscraper
Definition:
Two strong links for one digit share a base; the roof cells force eliminations
from cells that see both roofs.

Minimal scenario (digit `5`):

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  | `{5,8}` |  |  |  |  | `{5,9}` |  |  |
| r2 |  | `{1,5}` |  |  |  |  |  | `{2,5}` |  |
| r3 |  |  |  |  |  |  |  |  | `{4,5}` |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
Rows 1 and 2 have strong links on digit `5` and share base column 2.

Action:
Eliminate `5` from `r3c9` (a common peer of the roof cells).

### 14. Unique Rectangle
Definition:
If four cells form a deadly two-digit rectangle, extra candidates can be removed
to keep a unique solution.

Minimal scenario:

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2}` |  |  | `{1,2}` |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 | `{1,2}` |  |  | `{1,2,3}` |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Observation:
Three corners are pure `{1,2}`; the fourth corner has extra candidate `3`.

Action:
Eliminate `3` from `r4c4`.

### Additional Implemented Human Techniques

- Naked Quad:
  Four cells in one unit contain exactly four total digits between them.
  Those four digits are removed from all other cells in that unit.
  Use after triples when local candidate cleanup is still possible.
- Hidden Quad:
  Four digits in one unit can only appear in the same four cells.
  Those cells are then reduced to only those four digits.
  Use when unit scans show repeated multi-digit clutter that pair/triple rules miss.
- Swordfish:
  One digit forms a 3-row/3-column fish pattern (row-based or column-based).
  That digit is eliminated from matching columns/rows outside the fish rows/columns.
  Use after X-Wing for harder single-digit line interactions.
- Jellyfish:
  A larger 4-row/4-column fish version of Swordfish.
  It enables similar eliminations but has a higher scan cost.
  Use late in the pipeline on harder stalls.
- Finned X-Wing / Sashimi X-Wing:
  A near X-Wing where one extra "fin" candidate prevents a pure rectangle.
  Eliminations are limited to cells in the fin's box that also align with base lines.
  Use after standard X-Wing when almost-rectangular patterns appear.
- Finned Swordfish:
  A near Swordfish with one extra fin candidate.
  The fin's box plus base lines determines safe eliminations.
  Use after Swordfish for harder fish-style stalls.
- Empty Rectangle:
  A box-level L-shape candidate pattern combined with row/column links.
  This creates a single crossing elimination for the same digit.
  Use on advanced stalled states where direct fish/wing moves are unavailable.
- Remote Pairs:
  A chain of bivalue cells using the same pair (for example `{1,9}`).
  Cells seeing opposite chain colors can eliminate both pair digits.
  Use on advanced chain-heavy puzzles after simpler pair/wing methods.
- Simple Coloring:
  A single digit is colored across strong links with two alternating colors.
  Color-wrap and color-trap conditions produce candidate eliminations.
  Use after fish/wing techniques when single-digit chains are present.
- 3D Medusa (restricted):
  Candidate nodes are two-colored using strong links across cells and units.
  Color contradictions and color-trap interactions remove impossible candidates.
  Use on very hard stalled puzzles with dense conjugate/bivalue structure.
- AIC (restricted):
  Alternating strong/weak links form inference chains across candidates.
  When chain endpoints force a shared digit relation, common-peer eliminations
  become possible.
  Use on expert-level stalled states after simpler chain techniques.
- X-Cycles:
  Alternating inference loops for one digit create cycle-based contradictions.
  Those contradictions force eliminations for that digit.
  Use on hard puzzles with dense conjugate-link networks.
- XY-Chain:
  A chain of bivalue cells links endpoint candidates through alternating digits.
  Shared endpoint digit is removed from common peers of the chain endpoints.
  Use when XY-Wing is insufficient and longer bivalue chains exist.
- ALS-XZ (restricted):
  Two almost-locked sets share a restricted common candidate and another
  elimination candidate.
  That shared elimination candidate can be removed from cells seeing both ALSs.
  Use late on advanced stalled states.
- Sue de Coq (restricted):
  A box-line intersection is split into disjoint line-only and box-only digit
  groups.
  This allows eliminations in the line and box outside those selected subsets.
  Use on hard intersection-heavy grids.
- BUG+1:
  In a near-BUG state (all bivalue except one tri-value cell), parity reveals
  a forced digit in that exceptional cell.
  Use very late when the grid is almost solved.
- Grouped AIC (restricted):
  Extends alternating inference chains with grouped-node style links.
  The current implementation focuses on safe AIC-compatible reductions.
  Use for chain-heavy expert stalls.
- Nice Loops (restricted):
  Inference loops can force candidates true/false through contradiction logic.
  The current implementation reuses safe AIC-loop eliminations.
  Use when shorter chains no longer progress.
- ALS Chains (restricted):
  Links multiple almost-locked sets to propagate eliminations across units.
  The current implementation extends safe ALS-XZ-style reductions.
  Use in advanced ALS-rich states.
- Death Blossom (restricted):
  A stem cell plus two petals can force a shared external candidate false.
  Useful when petal pairs tie different stem digits to the same outside value.
  Use on dense bivalue neighborhoods.
- Uniqueness Expansions (restricted):
  Additional uniqueness logic beyond baseline unique rectangle.
  Current implementation includes a restricted UR type-2 style elimination.
  Use near endgame to avoid deadly non-unique patterns.
- Fireworks (restricted):
  A pivot with row/column conjugate-style links can remove a remote candidate.
  Current implementation targets a narrow but safe single-digit form.
  Use on expert stalls with strong-link intersections.
- WXYZ-Wing (restricted):
  Four-cell wing generalization of XYZ-Wing.
  A restricted shared candidate can be removed from cells seeing all holders.
  Use after XY/XYZ/chain techniques.
- Exocet (very restricted):
  Structural base/target pattern that constrains two digits to target cells.
  Current implementation detects a narrow junior-style aligned variant.
  Use as a specialized late-game pattern.
- Sue de Coq Full/Generalized (restricted):
  Generalizes Sue de Coq beyond the base intersection form.
  Current implementation adds a safe restricted 3-cell intersection mode.
  Use on intersection-heavy hard grids.
- Kraken Fish (restricted):
  Fish patterns combined with chain logic for deeper eliminations.
  Current implementation reuses safe fish-compatible eliminations.
  Use late when base fish methods partially apply.
- Sashimi Fish (restricted):
  Broader sashimi fish family extending finned fish logic.
  Current implementation reuses safe finned-fish-compatible eliminations.
  Use on advanced fish-like stalls.

Performance note:
The heaviest techniques are intentionally kept out of default order and are
available via explicit API technique selection. Enabling all advanced
techniques increases solve power but can be significantly slower.

## Result Model

`solve_from_string()` returns a `SolveResult` with:

- `status`: `solved`, `stalled`, or `invalid`
- `grid_string`: final grid string
- `steps`: ordered list of applied steps
- `technique_counts`: count per technique used
- `difficulty`: `easy`, `medium`, `hard`, `expert`, or `unsolved`
- `used_fallback_search`: `true` if non-human fallback search was used to finish
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
fallback_result = solve_from_string(puzzle, allow_fallback_search=True)
all_techniques_result = solve_from_string(
    puzzle,
    techniques=[
        "naked_single",
        "hidden_single",
        "locked_candidates",
        "naked_pair",
        "hidden_pair",
        "naked_triple",
        "hidden_triple",
        "naked_quad",
        "hidden_quad",
        "xy_wing",
        "xyz_wing",
        "x_wing",
        "w_wing",
        "swordfish",
        "jellyfish",
        "simple_coloring",
        "three_d_medusa",
        "aic",
        "x_cycles",
        "xy_chain",
        "grouped_aic",
        "nice_loops",
        "als_chains",
        "death_blossom",
        "uniqueness_expansions",
        "fireworks",
        "wxyz_wing",
        "exocet",
        "sue_de_coq_full",
        "kraken_fish",
        "sashimi_fish",
        "als_xz",
        "sue_de_coq",
        "bug_plus_one",
        "finned_x_wing",
        "finned_swordfish",
        "empty_rectangle",
        "remote_pairs",
        "two_string_kite",
        "skyscraper",
        "unique_rectangle",
    ],
)

print(result.status)
print(result.difficulty)
print(result.used_fallback_search)
print(result.grid_string)
print(result.technique_counts)
```

### CLI

Single puzzle:

```bash
python -m sudoku_solver "<81-char-puzzle>"
python -m sudoku_solver "<81-char-puzzle>" --show-steps
python -m sudoku_solver "<81-char-puzzle>" --show-telemetry
python -m sudoku_solver "<81-char-puzzle>" --allow-fallback-search
python -m sudoku_solver "<81-char-puzzle>" --max-steps 200
```

Puzzle file mode:

```bash
python -m sudoku_solver --puzzle-file puzzles/top1465.txt
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --max-failures 2
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --allow-fallback-search
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --show-steps --show-telemetry
```

Note:
CLI uses the default technique order. Custom technique subsets/supersets are currently
configured through the Python API (`techniques=[...]`).

### Benchmark Harness

```bash
python scripts/benchmark.py puzzles/top1465.txt
python scripts/benchmark.py puzzles/top1465.txt --allow-fallback-search
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
- `sudoku_solver/solver.py`: orchestration loop, step application, optional fallback search, difficulty classification.
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
6. If stalled by techniques and fallback is enabled, run uniqueness-aware fallback search.
7. Return `SolveResult` with final status, steps, telemetry, difficulty, and fallback usage flag.

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
