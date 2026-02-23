"""Shared helpers for fish-family techniques."""

from dataclasses import dataclass
from itertools import combinations

from sudoku_solver.units import box_cells, box_index, col_cells, col_index, row_cells, row_index


@dataclass(slots=True, frozen=True)
class FishElimination:
    """Single fish-derived elimination batch."""

    digit: int
    eliminations: tuple[tuple[int, int], ...]
    affected_units: tuple[str, ...]
    orientation: str
    base_units: tuple[int, ...]


@dataclass(slots=True, frozen=True)
class _FrankenBaseUnit:
    kind: str
    index: int
    covers: frozenset[int]
    protected_cells: frozenset[int]


def find_standard_fish_elimination(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    size: int,
    exact_line_size: bool,
) -> FishElimination | None:
    """Find one standard fish elimination for a digit and size."""
    row_positions = _collect_line_positions(
        candidates,
        digit,
        line_kind="row",
        size=size,
        exact_line_size=exact_line_size,
    )
    row_result = _find_standard_orientation(
        candidates,
        digit,
        size=size,
        line_kind="row",
        line_positions=row_positions,
    )
    if row_result is not None:
        return row_result

    col_positions = _collect_line_positions(
        candidates,
        digit,
        line_kind="col",
        size=size,
        exact_line_size=exact_line_size,
    )
    return _find_standard_orientation(
        candidates,
        digit,
        size=size,
        line_kind="col",
        line_positions=col_positions,
    )


def _collect_line_positions(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    line_kind: str,
    size: int,
    exact_line_size: bool,
) -> dict[int, set[int]]:
    positions: dict[int, set[int]] = {}
    for line in range(9):
        if line_kind == "row":
            cover_set = {
                col_index(cell_index)
                for cell_index in row_cells(line)
                if cell_index in candidates and digit in candidates[cell_index]
            }
        else:
            cover_set = {
                row_index(cell_index)
                for cell_index in col_cells(line)
                if cell_index in candidates and digit in candidates[cell_index]
            }

        if exact_line_size:
            if len(cover_set) == size:
                positions[line] = cover_set
        elif 2 <= len(cover_set) <= size:
            positions[line] = cover_set
    return positions


def _find_standard_orientation(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    size: int,
    line_kind: str,
    line_positions: dict[int, set[int]],
) -> FishElimination | None:
    for line_group in combinations(sorted(line_positions), size):
        cover_union = set().union(*(line_positions[line] for line in line_group))
        if len(cover_union) != size:
            continue

        eliminations = _standard_eliminations(
            candidates,
            digit,
            line_kind=line_kind,
            base_lines=line_group,
            cover_lines=tuple(sorted(cover_union)),
        )
        if not eliminations:
            continue

        if line_kind == "row":
            affected_units = tuple(
                [f"row{line + 1}" for line in line_group]
                + [f"col{line + 1}" for line in sorted(cover_union)]
            )
        else:
            affected_units = tuple(
                [f"col{line + 1}" for line in line_group]
                + [f"row{line + 1}" for line in sorted(cover_union)]
            )

        return FishElimination(
            digit=digit,
            eliminations=tuple(sorted(eliminations)),
            affected_units=affected_units,
            orientation=line_kind,
            base_units=tuple(line_group),
        )

    return None


def _standard_eliminations(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    line_kind: str,
    base_lines: tuple[int, ...],
    cover_lines: tuple[int, ...],
) -> list[tuple[int, int]]:
    eliminations: list[tuple[int, int]] = []
    if line_kind == "row":
        for cover_col in cover_lines:
            for cell_index in col_cells(cover_col):
                if row_index(cell_index) in base_lines:
                    continue
                if cell_index not in candidates or digit not in candidates[cell_index]:
                    continue
                eliminations.append((cell_index, digit))
    else:
        for cover_row in cover_lines:
            for cell_index in row_cells(cover_row):
                if col_index(cell_index) in base_lines:
                    continue
                if cell_index not in candidates or digit not in candidates[cell_index]:
                    continue
                eliminations.append((cell_index, digit))
    return eliminations


def find_finned_x_wing_elimination(
    candidates: dict[int, set[int]],
    digit: int,
) -> FishElimination | None:
    """Find one finned/sashimi X-Wing elimination for a digit."""
    row_positions = _collect_line_positions(
        candidates,
        digit,
        line_kind="row",
        size=3,
        exact_line_size=False,
    )
    row_positions = {row: covers for row, covers in row_positions.items() if 1 <= len(covers) <= 3}
    row_result = _find_finned_x_wing_row_based(candidates, digit, row_positions)
    if row_result is not None:
        return row_result

    col_positions = _collect_line_positions(
        candidates,
        digit,
        line_kind="col",
        size=3,
        exact_line_size=False,
    )
    col_positions = {col: covers for col, covers in col_positions.items() if 1 <= len(covers) <= 3}
    return _find_finned_x_wing_col_based(candidates, digit, col_positions)


def _find_finned_x_wing_row_based(
    candidates: dict[int, set[int]],
    digit: int,
    row_positions: dict[int, set[int]],
) -> FishElimination | None:
    for rows in combinations(sorted(row_positions), 2):
        cols_union = row_positions[rows[0]] | row_positions[rows[1]]
        if len(cols_union) != 3:
            continue

        for base_cols in combinations(sorted(cols_union), 2):
            base_col_set = set(base_cols)
            base_counts = [len(row_positions[row] & base_col_set) for row in rows]
            if min(base_counts) < 1 or max(base_counts) > 2:
                continue
            if not any(count == 2 for count in base_counts):
                continue

            fin_rows = [row for row in rows if len(row_positions[row] - base_col_set) > 0]
            if len(fin_rows) != 1:
                continue

            fin_row = fin_rows[0]
            fin_cols = row_positions[fin_row] - base_col_set
            fin_cells = [fin_row * 9 + col for col in sorted(fin_cols)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if col_index(cell_index) in base_col_set
                and row_index(cell_index) not in rows
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return FishElimination(
                    digit=digit,
                    eliminations=tuple(sorted(eliminations)),
                    affected_units=(
                        f"row{rows[0] + 1}",
                        f"row{rows[1] + 1}",
                        f"box{fin_box + 1}",
                    ),
                    orientation="row",
                    base_units=tuple(rows),
                )
    return None


def _find_finned_x_wing_col_based(
    candidates: dict[int, set[int]],
    digit: int,
    col_positions: dict[int, set[int]],
) -> FishElimination | None:
    for cols in combinations(sorted(col_positions), 2):
        rows_union = col_positions[cols[0]] | col_positions[cols[1]]
        if len(rows_union) != 3:
            continue

        for base_rows in combinations(sorted(rows_union), 2):
            base_row_set = set(base_rows)
            base_counts = [len(col_positions[col] & base_row_set) for col in cols]
            if min(base_counts) < 1 or max(base_counts) > 2:
                continue
            if not any(count == 2 for count in base_counts):
                continue

            fin_cols = [col for col in cols if len(col_positions[col] - base_row_set) > 0]
            if len(fin_cols) != 1:
                continue

            fin_col = fin_cols[0]
            fin_rows = col_positions[fin_col] - base_row_set
            fin_cells = [row * 9 + fin_col for row in sorted(fin_rows)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if row_index(cell_index) in base_row_set
                and col_index(cell_index) not in cols
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return FishElimination(
                    digit=digit,
                    eliminations=tuple(sorted(eliminations)),
                    affected_units=(
                        f"col{cols[0] + 1}",
                        f"col{cols[1] + 1}",
                        f"box{fin_box + 1}",
                    ),
                    orientation="col",
                    base_units=tuple(cols),
                )
    return None


def find_finned_swordfish_elimination(
    candidates: dict[int, set[int]],
    digit: int,
) -> FishElimination | None:
    """Find one finned swordfish elimination for a digit."""
    row_positions = _collect_line_positions(
        candidates,
        digit,
        line_kind="row",
        size=4,
        exact_line_size=False,
    )
    row_positions = {row: covers for row, covers in row_positions.items() if 2 <= len(covers) <= 4}
    row_result = _find_finned_swordfish_row_based(candidates, digit, row_positions)
    if row_result is not None:
        return row_result

    col_positions = _collect_line_positions(
        candidates,
        digit,
        line_kind="col",
        size=4,
        exact_line_size=False,
    )
    col_positions = {col: covers for col, covers in col_positions.items() if 2 <= len(covers) <= 4}
    return _find_finned_swordfish_col_based(candidates, digit, col_positions)


def _find_finned_swordfish_row_based(
    candidates: dict[int, set[int]],
    digit: int,
    row_positions: dict[int, set[int]],
) -> FishElimination | None:
    for rows in combinations(sorted(row_positions), 3):
        union_cols = set().union(*(row_positions[row] for row in rows))
        if len(union_cols) != 4:
            continue

        for base_cols in combinations(sorted(union_cols), 3):
            base_col_set = set(base_cols)
            if any(sum(1 for row in rows if col in row_positions[row]) < 2 for col in base_col_set):
                continue

            fin_rows = [row for row in rows if not row_positions[row].issubset(base_col_set)]
            if len(fin_rows) != 1:
                continue

            fin_row = fin_rows[0]
            fin_cols = row_positions[fin_row] - base_col_set
            if len(fin_cols) != 1:
                continue
            if len(row_positions[fin_row] & base_col_set) < 2:
                continue

            fin_cells = [fin_row * 9 + col for col in sorted(fin_cols)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if col_index(cell_index) in base_col_set
                and row_index(cell_index) != fin_row
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return FishElimination(
                    digit=digit,
                    eliminations=tuple(sorted(eliminations)),
                    affected_units=(
                        f"row{rows[0] + 1}",
                        f"row{rows[1] + 1}",
                        f"row{rows[2] + 1}",
                        f"box{fin_box + 1}",
                    ),
                    orientation="row",
                    base_units=tuple(rows),
                )
    return None


def _find_finned_swordfish_col_based(
    candidates: dict[int, set[int]],
    digit: int,
    col_positions: dict[int, set[int]],
) -> FishElimination | None:
    for cols in combinations(sorted(col_positions), 3):
        union_rows = set().union(*(col_positions[col] for col in cols))
        if len(union_rows) != 4:
            continue

        for base_rows in combinations(sorted(union_rows), 3):
            base_row_set = set(base_rows)
            if any(sum(1 for col in cols if row in col_positions[col]) < 2 for row in base_row_set):
                continue

            fin_cols = [col for col in cols if not col_positions[col].issubset(base_row_set)]
            if len(fin_cols) != 1:
                continue

            fin_col = fin_cols[0]
            fin_rows = col_positions[fin_col] - base_row_set
            if len(fin_rows) != 1:
                continue
            if len(col_positions[fin_col] & base_row_set) < 2:
                continue

            fin_cells = [row * 9 + fin_col for row in sorted(fin_rows)]
            fin_boxes = {box_index(cell_index) for cell_index in fin_cells}
            if len(fin_boxes) != 1:
                continue
            fin_box = next(iter(fin_boxes))

            eliminations = [
                (cell_index, digit)
                for cell_index in box_cells(fin_box)
                if row_index(cell_index) in base_row_set
                and col_index(cell_index) != fin_col
                and cell_index in candidates
                and digit in candidates[cell_index]
            ]
            if eliminations:
                return FishElimination(
                    digit=digit,
                    eliminations=tuple(sorted(eliminations)),
                    affected_units=(
                        f"col{cols[0] + 1}",
                        f"col{cols[1] + 1}",
                        f"col{cols[2] + 1}",
                        f"box{fin_box + 1}",
                    ),
                    orientation="col",
                    base_units=tuple(cols),
                )
    return None


def find_franken_mutant_fish_elimination(
    candidates: dict[int, set[int]],
    digit: int,
) -> FishElimination | None:
    """Find an expanded franken/mutant fish elimination for one digit."""
    for size in (3, 2):
        row_oriented = _find_franken_orientation(
            candidates,
            digit,
            orientation="row",
            size=size,
        )
        if row_oriented is not None:
            return row_oriented
        col_oriented = _find_franken_orientation(
            candidates,
            digit,
            orientation="col",
            size=size,
        )
        if col_oriented is not None:
            return col_oriented
    return None


def _find_franken_orientation(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    orientation: str,
    size: int,
) -> FishElimination | None:
    bases = _collect_franken_bases(
        candidates,
        digit,
        orientation=orientation,
        max_cover_size=size,
    )
    for base_group in combinations(bases, size):
        kinds = {base.kind for base in base_group}
        if "box" not in kinds:
            continue
        if orientation == "row" and "row" not in kinds:
            continue
        if orientation == "col" and "col" not in kinds:
            continue

        cover_union = set().union(*(base.covers for base in base_group))
        if len(cover_union) != size:
            continue
        cover_lines = tuple(sorted(cover_union))

        protected = set().union(*(set(base.protected_cells) for base in base_group))
        eliminations = _franken_eliminations(
            candidates,
            digit,
            orientation=orientation,
            cover_lines=cover_lines,
            protected_cells=protected,
        )
        if not eliminations:
            continue

        line_prefix = "col" if orientation == "row" else "row"
        affected_units = tuple(
            [_franken_unit_label(base) for base in base_group]
            + [f"{line_prefix}{line + 1}" for line in cover_lines]
        )
        return FishElimination(
            digit=digit,
            eliminations=tuple(sorted(eliminations)),
            affected_units=affected_units,
            orientation=f"franken_{orientation}",
            base_units=tuple(base.index for base in base_group),
        )

    return None


def _collect_franken_bases(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    orientation: str,
    max_cover_size: int,
) -> list[_FrankenBaseUnit]:
    bases: list[_FrankenBaseUnit] = []
    if orientation == "row":
        for row in range(9):
            covers = {
                col_index(cell_index)
                for cell_index in row_cells(row)
                if cell_index in candidates and digit in candidates[cell_index]
            }
            if 1 <= len(covers) <= max_cover_size:
                bases.append(
                    _FrankenBaseUnit(
                        kind="row",
                        index=row,
                        covers=frozenset(covers),
                        protected_cells=frozenset(row_cells(row)),
                    )
                )
        for box in range(9):
            covers = {
                col_index(cell_index)
                for cell_index in box_cells(box)
                if cell_index in candidates and digit in candidates[cell_index]
            }
            if 1 <= len(covers) <= max_cover_size:
                bases.append(
                    _FrankenBaseUnit(
                        kind="box",
                        index=box,
                        covers=frozenset(covers),
                        protected_cells=frozenset(box_cells(box)),
                    )
                )
        return bases

    for col in range(9):
        covers = {
            row_index(cell_index)
            for cell_index in col_cells(col)
            if cell_index in candidates and digit in candidates[cell_index]
        }
        if 1 <= len(covers) <= max_cover_size:
            bases.append(
                _FrankenBaseUnit(
                    kind="col",
                    index=col,
                    covers=frozenset(covers),
                    protected_cells=frozenset(col_cells(col)),
                )
            )
    for box in range(9):
        covers = {
            row_index(cell_index)
            for cell_index in box_cells(box)
            if cell_index in candidates and digit in candidates[cell_index]
        }
        if 1 <= len(covers) <= max_cover_size:
            bases.append(
                _FrankenBaseUnit(
                    kind="box",
                    index=box,
                    covers=frozenset(covers),
                    protected_cells=frozenset(box_cells(box)),
                )
            )
    return bases


def _franken_eliminations(
    candidates: dict[int, set[int]],
    digit: int,
    *,
    orientation: str,
    cover_lines: tuple[int, ...],
    protected_cells: set[int],
) -> list[tuple[int, int]]:
    eliminations: list[tuple[int, int]] = []
    if orientation == "row":
        for cover_col in cover_lines:
            for cell_index in col_cells(cover_col):
                if cell_index in protected_cells:
                    continue
                if cell_index not in candidates or digit not in candidates[cell_index]:
                    continue
                eliminations.append((cell_index, digit))
        return eliminations

    for cover_row in cover_lines:
        for cell_index in row_cells(cover_row):
            if cell_index in protected_cells:
                continue
            if cell_index not in candidates or digit not in candidates[cell_index]:
                continue
            eliminations.append((cell_index, digit))
    return eliminations


def _franken_unit_label(base: _FrankenBaseUnit) -> str:
    if base.kind == "row":
        return f"row{base.index + 1}"
    if base.kind == "col":
        return f"col{base.index + 1}"
    return f"box{base.index + 1}"
