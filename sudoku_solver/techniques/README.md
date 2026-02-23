# Technique Reference

This document explains every supported technique and shows a minimal full-grid
illustration for each one. Only cells relevant to the pattern are populated; all
other cells are intentionally left blank.

Notation:

- `rXcY` means row X, column Y.
- `{...}` means candidate digits for an unsolved cell.
- Plain digits represent solved values.

## Technique Index

| Key | Name | Family | Tier | Status | Expected Cost |
| --- | --- | --- | --- | --- | --- |
| `naked_single` | Naked Single | Singles | Easy | Standard | Low |
| `hidden_single` | Hidden Single | Singles | Easy | Standard | Low |
| `locked_candidates` | Locked Candidates | Intersections | Easy | Standard | Low |
| `naked_pair` | Naked Pair | Subsets | Medium | Standard | Low |
| `hidden_pair` | Hidden Pair | Subsets | Medium | Standard | Low |
| `naked_triple` | Naked Triple | Subsets | Medium | Standard | Medium |
| `hidden_triple` | Hidden Triple | Subsets | Medium | Standard | Medium |
| `naked_quad` | Naked Quad | Subsets | Hard | Standard | Medium |
| `hidden_quad` | Hidden Quad | Subsets | Hard | Standard | Medium |
| `xy_wing` | XY-Wing | Wings | Hard | Standard | Medium |
| `xyz_wing` | XYZ-Wing | Wings | Hard | Standard | Medium |
| `x_wing` | X-Wing | Fish | Hard | Standard | Medium |
| `finned_x_wing` | Finned X-Wing | Fish | Expert | Standard | High |
| `swordfish` | Swordfish | Fish | Hard | Standard | Medium |
| `finned_swordfish` | Finned Swordfish | Fish | Expert | Standard | High |
| `jellyfish` | Jellyfish | Fish | Expert | Standard | High |
| `squirmbag` | Squirmbag | Fish | Expert | Standard | Very High |
| `simple_coloring` | Simple Coloring | Coloring/Chains | Hard | Standard | Medium |
| `three_d_medusa` | 3D Medusa | Coloring/Chains | Expert | Expanded | High |
| `aic` | AIC | Coloring/Chains | Expert | Expanded | High |
| `grouped_aic` | Grouped AIC | Coloring/Chains | Expert | Expanded | High |
| `nice_loops` | Nice Loops | Coloring/Chains | Expert | Expanded | High |
| `x_cycles` | X-Cycles | Coloring/Chains | Hard | Standard | Medium |
| `xy_chain` | XY-Chain | Coloring/Chains | Hard | Standard | Medium |
| `forcing_chains` | Forcing Chains | ALS/Forcing | Expert | Expanded | High |
| `forcing_nets` | Forcing Nets | ALS/Forcing | Expert | Expanded | High |
| `als_chains` | ALS Chains | ALS/Forcing | Expert | Expanded | High |
| `death_blossom` | Death Blossom | ALS/Forcing | Expert | Restricted | High |
| `uniqueness_expansions` | Uniqueness Expansions | Uniqueness | Expert | Restricted | Medium |
| `fireworks` | Fireworks | Structures | Expert | Restricted | High |
| `franken_mutant_fish` | Franken/Mutant Fish | Fish | Expert | Expanded | Very High |
| `wxyz_wing` | WXYZ-Wing | Wings | Expert | Expanded | High |
| `exocet` | Exocet | Structures | Expert | Restricted | Very High |
| `sue_de_coq_full` | Sue de Coq Full/Generalized | Intersections | Expert | Restricted | High |
| `kraken_fish` | Kraken Fish | Fish | Expert | Expanded | Very High |
| `sashimi_fish` | Sashimi Fish | Fish | Expert | Expanded | High |
| `als_xz` | ALS-XZ | ALS/Forcing | Expert | Expanded | High |
| `sue_de_coq` | Sue de Coq | Intersections | Expert | Restricted | High |
| `bug_plus_one` | BUG+1 | Uniqueness | Hard | Standard | Low |
| `empty_rectangle` | Empty Rectangle | Intersections | Expert | Standard | Medium |
| `remote_pairs` | Remote Pairs | Coloring/Chains | Hard | Standard | Medium |
| `unique_rectangle` | Unique Rectangle | Uniqueness | Hard | Standard | Low |
| `skyscraper` | Skyscraper | Structures | Hard | Standard | Medium |
| `two_string_kite` | Two-String Kite | Structures | Hard | Standard | Medium |
| `w_wing` | W-Wing | Wings | Hard | Standard | Medium |

Status meaning:

- `Standard`: implemented baseline rule for normal production use.
- `Expanded`: implementation includes additional sub-pattern coverage compared to baseline.
- `Restricted`: intentionally conservative subset of broader known variants.

## Singles and Subsets

### 1. Naked Single (`naked_single`)

Definition: one cell has exactly one candidate.

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

Action: place `7` at `r4c5`.

### 2. Hidden Single (`hidden_single`)

Definition: in one unit, a digit appears in only one candidate cell.

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

Action: `1` is hidden in row 2, so place `1` at `r2c1`.

### 3. Locked Candidates (`locked_candidates`)

Definition: a candidate is locked to one row/column inside a box (or vice versa).

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

Action: eliminate `5` from row 1 outside box 1 (`r1c4`, `r1c8`).

### 4. Naked Pair (`naked_pair`)

Definition: two cells in one unit share the same two candidates.

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

Action: remove `2` from `r5c4`, remove `8` from `r5c9`.

### 5. Hidden Pair (`hidden_pair`)

Definition: two digits in a unit appear only in the same two cells.

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

Action: reduce `r6c2` and `r6c9` to `{3,7}`.

### 6. Naked Triple (`naked_triple`)

Definition: three cells in a unit contain exactly three digits in union.

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

Action: remove `4` and `9` from non-triple cells in column 4.

### 7. Hidden Triple (`hidden_triple`)

Definition: three digits can only go in three cells of a unit.

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

Action: keep only `{2,5,8}` across the three triple cells.

### 8. Naked Quad (`naked_quad`)

Definition: four cells in one unit contain exactly four digits in union.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 | `{1,2}` | `{1,5}` | `{2,3}` | 8 | `{3,4}` | `{4,9}` | 6 | 7 |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: remove quad digits `{1,2,3,4}` from other row-7 cells.

### 9. Hidden Quad (`hidden_quad`)

Definition: four digits in a unit only appear in the same four cells.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,3,5}` | `{2,4,7}` |  |  |  |  |  |  |  |
| r2 | `{1,6}` | `{2,8}` |  |  |  |  |  |  |  |
| r3 | `{3,5,9}` | `{4,7,9}` |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: in row 1-3/col1-2 area, keep only hidden-quad digits in the four target cells.

## Wings and Chains

### 10. XY-Wing (`xy_wing`)

Definition: one bivalue pivot with two bivalue pincers eliminates a shared digit.

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

Action: eliminate `3` from cells that see both pincers.

### 11. XYZ-Wing (`xyz_wing`)

Definition: a tri-value pivot and two bivalue pincers force elimination of the shared digit.

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

Action: eliminate shared digit `1` from common peers of all three wing cells.

### 12. W-Wing (`w_wing`)

Definition: two matching bivalue cells are linked by a strong link on one digit.

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

Action: eliminate `9` from cells that see both `{1,9}` wing endpoints.

### 13. WXYZ-Wing (`wxyz_wing`)

Definition: four-cell wing where restricted/non-restricted wing digits force eliminations.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  | `{1,3}` |  |  | `{2,3,4}` |  |  |  |  |
| r3 |  |  |  | `{1,2}` |  |  |  |  |  |
| r4 |  |  |  |  | `{2,4}` |  |  |  |  |
| r5 |  | `{3,4}` |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate target wing digit from cells that see the relevant wing structure.

Implementation note: code supports both type-1 and type-2 WXYZ cases.

### 14. XY-Chain (`xy_chain`)

Definition: alternating bivalue chain eliminates endpoint-shared digit from common peers.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2}` |  |  |  |  |  |  |  |  |
| r2 |  | `{2,5}` |  |  |  |  |  |  |  |
| r3 |  |  | `{5,7}` |  |  |  |  |  |  |
| r4 |  |  |  | `{1,7}` |  |  |  |  |  |
| r5 |  |  |  |  | `{1,9}` |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate endpoint digit from any cell that sees both chain endpoints.

### 15. AIC (`aic`)

Definition: alternating strong/weak candidate links create logical forcing paths.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2}` | `{2,3}` | `{1,3}` |  |  |  |  |  |  |
| r2 | `{1,6}` | `{2,4}` | `{3,5}` |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate candidates contradicted by both ends of the AIC.

Implementation note: expanded version includes same-cell discontinuous loop eliminations.

### 16. Grouped AIC (`grouped_aic`)

Definition: AIC with grouped nodes (sets of candidates treated as one node).

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2}` | `{2,3}` |  |  |  |  |  |  |  |
| r2 | `{1,4}` | `{3,4}` |  |  |  |  |  |  |  |
| r3 | `{2,5}` | `{5,6}` |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: remove candidates disproven by grouped chain logic.

### 17. Nice Loops (`nice_loops`)

Definition: closed inference loops with weak/strong links force eliminations.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2}` | `{2,3}` | `{1,3}` |  |  |  |  |  |  |
| r2 | `{1,4}` | `{3,4}` |  |  |  |  |  |  |  |
| r3 | `{2,5}` | `{5,1}` |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate candidates on weak points implied false by the loop.

### 18. X-Cycles (`x_cycles`)

Definition: single-digit alternating cycles create forced eliminations.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{7,9}` |  | `{7,8}` |  |  |  |  |  |  |
| r2 |  | `{2,7}` |  | `{5,7}` |  |  |  |  |  |
| r3 | `{1,7}` |  | `{3,7}` |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate digit `7` where cycle parity forbids it.

### 19. Simple Coloring (`simple_coloring`)

Definition: two-color strong-link graph for one digit gives wrap/trap eliminations.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{5,8}` |  | `{5,9}` |  |  |  |  |  |  |
| r2 |  | `{1,5}` |  | `{2,5}` |  |  |  |  |  |
| r3 | `{3,5}` |  | `{4,5}` |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate colored digit where both colors see the same cell.

### 20. 3D Medusa (`three_d_medusa`)

Definition: extended coloring over cell and unit strong links.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,5}` | `{1,7}` |  |  |  |  |  |  |  |
| r2 | `{5,7}` | `{2,7}` |  |  |  |  |  |  |  |
| r3 | `{1,2}` | `{2,5}` |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate candidates from color contradictions, cell bi-color, or unit bi-color conflicts.

## Fish Family

### 21. X-Wing (`x_wing`)

Definition: two rows (or columns) share the same two candidate columns (or rows).

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

Action: eliminate `7` from those columns outside the two base rows.

### 22. Finned X-Wing (`finned_x_wing`)

Definition: near X-Wing with one fin; eliminations are limited by fin box geometry.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  | `{1,4}` | `{3,4}` |  | `{2,4}` |  |  |  |  |
| r3 |  | `{5,4}` |  |  | `{6,4}` |  |  |  |  |
| r4 |  | `{4,9}` |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: remove finned digit from cover-line cells in the fin box.

### 23. Swordfish (`swordfish`)

Definition: size-3 fish pattern for one digit across three rows/columns.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{5,8}` |  |  | `{1,5}` |  |  | `{2,5}` |  |  |
| r2 |  | `{3,5}` |  | `{4,5}` |  |  | `{6,5}` |  |  |
| r3 | `{7,5}` |  |  |  | `{8,5}` |  | `{9,5}` |  |  |
| r4 |  |  |  | `{2,5}` |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  | `{1,5}` |  |  |

Action: eliminate fish digit from cover columns outside base rows.

### 24. Finned Swordfish (`finned_swordfish`)

Definition: near Swordfish with a fin; elimination area is constrained by fin box.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{5,8}` |  | `{3,5}` |  | `{1,5}` |  | `{2,5}` |  |  |
| r2 |  | `{4,5}` |  |  | `{6,5}` |  | `{7,5}` |  |  |
| r3 |  | `{8,5}` |  |  | `{9,5}` |  | `{5,6}` |  |  |
| r4 |  | `{1,5}` |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: remove fish digit from fin-box cells on the fish cover lines.

### 25. Jellyfish (`jellyfish`)

Definition: size-4 fish extension of Swordfish.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{7,1}` |  |  | `{7,2}` |  |  | `{7,3}` |  |  |
| r2 |  | `{7,4}` |  | `{7,5}` |  |  | `{7,6}` |  |  |
| r3 | `{7,8}` |  |  |  | `{7,9}` |  | `{7,1}` |  |  |
| r4 | `{7,2}` |  |  | `{7,3}` |  |  | `{7,4}` |  |  |
| r5 |  |  |  | `{7,8}` |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate fish digit from cover columns outside base rows.

### 26. Squirmbag (`squirmbag`)

Definition: size-5 fish extension.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{6,1}` |  | `{6,2}` |  | `{6,3}` |  |  |  |  |
| r2 |  | `{6,4}` |  | `{6,5}` |  | `{6,7}` |  |  |  |
| r3 | `{6,8}` |  |  | `{6,9}` |  | `{6,1}` |  |  |  |
| r4 |  | `{6,2}` |  |  | `{6,3}` |  | `{6,4}` |  |  |
| r5 | `{6,5}` |  |  |  | `{6,7}` |  | `{6,8}` |  |  |
| r6 |  |  |  | `{6,9}` |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate fish digit from cover lines outside base lines.

### 27. Sashimi Fish (`sashimi_fish`)

Definition: fish variants where one base line is under-populated, often fin-like.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{4,1}` |  |  | `{4,2}` |  |  |  |  |  |
| r2 |  | `{4,3}` |  | `{4,5}` |  |  |  |  |  |
| r3 | `{4,6}` |  |  |  | `{4,7}` |  |  |  |  |
| r4 |  | `{4,8}` |  |  |  |  |  |  |  |
| r5 |  |  |  | `{4,9}` |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate sashimi digit from cells constrained by the under-populated base lines.

Implementation note: code covers finned fish compatibility plus under-populated base-line scans.

### 28. Kraken Fish (`kraken_fish`)

Definition: fish eliminations strengthened by chain-compatible forcing.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{7,1}` |  |  | `{7,2}` |  |  |  |  |  |
| r2 |  | `{7,3}` |  |  | `{7,4}` |  |  |  |  |
| r3 | `{7,5}` |  |  |  | `{7,6}` |  |  |  |  |
| r4 |  | `{7,8}` |  |  |  |  |  |  |  |
| r5 |  |  |  | `{7,9}` |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: remove fish digit where fish+forcing intersections prove it false.

Implementation note: current implementation scans classic and finned-fish-compatible structures.

### 29. Franken/Mutant Fish (`franken_mutant_fish`)

Definition: fish with mixed base units (rows/columns combined with boxes).

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  | `{7,1}` | `{7,2}` |  |  |  |  |
| r2 |  |  |  | `{7,3}` |  | `{7,4}` |  |  |  |
| r3 |  |  |  |  | `{7,5}` | `{7,6}` |  |  |  |
| r4 |  |  |  |  |  |  | `{7,8}` | `{7,9}` |  |
| r5 |  |  |  |  |  |  | `{7,1}` | `{7,2}` |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate mixed-fish digit from cover lines outside protected base cells.

Implementation note: expanded version supports size-2 and size-3 mixed-base structures.

## Uniqueness and Pattern Rules

### 30. Unique Rectangle (`unique_rectangle`)

Definition: avoid non-unique deadly rectangles by eliminating extras.

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

Action: eliminate extra candidate (`3`) from the expanded corner.

### 31. Uniqueness Expansions (`uniqueness_expansions`)

Definition: additional UR variants (type-2/type-4/type-5 style logic).

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{3,8}` |  |  | `{3,8,9}` |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 | `{3,8}` |  |  | `{3,8}` |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate extra candidate(s) that would permit a deadly non-unique rectangle.

### 32. BUG+1 (`bug_plus_one`)

Definition: in a near-BUG grid, the single tri-value cell gets a forced value.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2}` | `{3,4}` | `{5,6}` | `{7,8}` | `{2,9}` | `{1,5}` | `{3,6}` | `{4,7}` | `{8,9}` |
| r2 | `{2,3}` | `{1,4}` | `{6,7}` | `{5,8}` | `{1,2,9}` | `{3,5}` | `{4,6}` | `{7,9}` | `{2,8}` |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: place the parity-forced candidate in the unique tri-value cell.

## ALS and Forcing Families

### 33. ALS-XZ (`als_xz`)

Definition: two ALSs with a restricted common candidate force elimination of another shared candidate.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{2,7}` | `{5,7}` |  |  |  |  |  |  |  |
| r2 | `{2,8}` | `{5,8}` |  |  |  |  |  |  |  |
| r3 |  | `{5,9}` |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate shared target digit from cells seeing both ALS target positions.

Implementation note: expanded scan includes larger ALS sizes.

### 34. ALS Chains (`als_chains`)

Definition: ALS nodes linked by RCCs form chain eliminations.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,4}` | `{2}` |  |  |  |  |  |  |  |
| r2 | `{1,5}` | `{2,5}` |  |  |  |  |  |  |  |
| r3 | `{3,4}` | `{1,3}` |  |  |  |  |  |  |  |
| r4 | `{4,7}` |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate a target digit where start/end ALS constraints overlap.

Implementation note: includes RCC chains and ALS XY-Wing fallback paths.

### 35. Death Blossom (`death_blossom`)

Definition: stem cell plus petals can force an external candidate false.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  | `{1,2,3}` |  |  |  |  |
| r4 |  |  |  | `{1,9}` |  | `{2,9}` |  |  |  |
| r5 |  |  |  |  |  | `{8,9}` |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate shared external petal digit from common peer cells.

### 36. Forcing Chains (`forcing_chains`)

Definition: assume each candidate of a bivalue pivot; use branch consequences.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2}` | `{1}` |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: if one branch contradicts (or both branches agree), apply the forced consequence.

Implementation note: expanded version also applies lightweight branch reductions (locked candidates and naked pairs).

### 37. Forcing Nets (`forcing_nets`)

Definition: forcing-chain generalization to pivots with 2-4 candidates.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,2,3,4}` | `{1}` | `{2}` | `{3}` |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: apply candidate placement/elimination agreed by all valid net branches.

Implementation note: expanded version shares the same branch-reduction improvements as forcing chains.

## Intersection and Specialty Rules

### 38. Sue de Coq (`sue_de_coq`)

Definition: box-line intersection splits into disjoint line-only and box-only digit sets.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  | `{1,2,5}` | `{1,2,7}` | `{5,7}` |  |  |  |
| r5 |  |  |  | `{3,5}` | `{4,7}` | `{3,4}` |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate digits from row/box cells outside the chosen split subsets.

### 39. Sue de Coq Full (`sue_de_coq_full`)

Definition: generalized Sue de Coq beyond the base intersection form.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  |  |  |  |  |  |
| r2 |  |  |  |  |  |  |  |  |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  | `{1,2,5}` | `{2,5,8}` | `{1,8}` |  |  |  |
| r5 |  |  |  | `{3,5,9}` | `{4,8,9}` | `{3,4}` |  |  |  |
| r6 |  |  |  | `{1,2,8}` |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: perform generalized line/box eliminations using the chosen intersection decomposition.

Implementation note: current solver includes restricted generalized modes, including 3-cell intersections.

### 40. Empty Rectangle (`empty_rectangle`)

Definition: box-internal candidate geometry combines with a row/column strong link.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  | `{6,9}` |  |  |  |  |  |  |  |
| r2 | `{6,3}` |  | `{6,5}` |  |  |  |  |  |  |
| r3 |  | `{6,7}` |  |  |  |  |  |  |  |
| r4 |  |  |  |  | `{6,8}` |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate the target digit from the intersection cell implied by the ER + strong link.

### 41. Remote Pairs (`remote_pairs`)

Definition: chain of identical bivalue pairs eliminates both digits from joint peers.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | `{1,9}` |  |  |  |  |  |  |  |  |
| r2 |  | `{1,9}` |  |  |  |  |  |  |  |
| r3 |  |  | `{1,9}` |  |  |  |  |  |  |
| r4 |  |  |  | `{1,9}` |  |  |  |  |  |
| r5 |  |  |  |  | `{1,9}` |  |  |  |  |
| r6 |  |  |  |  |  | `{1,9}` |  |  |  |
| r7 |  |  |  |  |  |  | `{1,9}` |  |  |
| r8 |  |  |  |  |  |  |  | `{1,9}` |  |
| r9 |  |  |  |  |  |  |  |  | `{1,9}` |

Action: eliminate `1` and `9` from cells seeing opposite-colored chain endpoints.

### 42. Two-String Kite (`two_string_kite`)

Definition: one row strong link plus one column strong link share a box endpoint.

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

Action: eliminate digit `5` from the kite target cell.

### 43. Skyscraper (`skyscraper`)

Definition: two strong links share one base line, creating two roof endpoints.

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

Action: eliminate roof digit from cells seeing both roof endpoints.

### 44. Fireworks (`fireworks`)

Definition: pivot and conjugate-style links remove a remote candidate.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  |  |  |  | `{6,8}` |  |  |  |  |
| r2 |  |  |  | `{6,2}` | `{6,3}` | `{6,4}` |  |  |  |
| r3 |  |  |  |  | `{6,7}` |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: remove pivot digit from the remote target seeing both implied branches.

Implementation note: the solver includes compatibility and peer-remote variants.

### 45. Exocet (`exocet`)

Definition: base and target cells constrain two digits as a structural pattern.

|   | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |  | `{2,8}` |  |  |  |  | `{2,8}` |  |  |
| r2 |  |  | `{2,8}` |  |  |  |  | `{2,8}` |  |
| r3 |  |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Action: eliminate target digits from cells incompatible with the base-target constraints.

Implementation note: current implementation focuses on restricted aligned exocet variants.
