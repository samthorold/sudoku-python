from __future__ import annotations
from dataclasses import dataclass, field
import itertools
import logging
from typing import Iterable

from sudoku.models import Board


logger = logging.getLogger(__name__)


@dataclass
class Node:

    row_idx: int
    col_idx: int
    col: Column
    left: Node | None = None
    right: Node | None = None
    up: Node | Column | None = None
    down: Node | Column | None = None

    def __repr__(self):
        left = f"({self.left.row_idx}, {self.left.col_idx})" if self.left else None
        right = f"({self.right.row_idx}, {self.right.col_idx})" if self.right else None
        if isinstance(self.up, Column):
            up = self.up
        else:
            up = f"({self.up.row_idx}, {self.up.col_idx})" if self.up else None
        if isinstance(self.down, Column):
            down = self.down
        else:
            down = f"({self.down.row_idx}, {self.down.col_idx})" if self.down else None
        return (
            f"<Node({self.row_idx}, {self.col_idx}, "
            f"left={left}, right={right}, up={up}, down={down})>"
        )


@dataclass
class Column:

    name: str
    col_idx: int
    left: Column | None = None
    right: Column | None = None
    up: Node | Column | None = None
    down: Node | Column | None = None
    size: int = 0

    def __repr__(self):
        return f"<Column({self.name})>"

    def __str__(self):
        s = f"{self.name}["
        node = self.down

        while node and node != self:
            s += f"{node.row_idx},"
            node = node.down

        s = s[:-1] + "]"

        return s


@dataclass
class Problem:
    root: Column
    next_min_col: Column | None = None

    @staticmethod
    def from_matrix(
        matrix: Iterable[Iterable[int]],
        column_names: Iterable[str] | None = None,
    ) -> Problem:
        """Build a Problem object from a sequence of rows."""

        root = Column("__root__", -1)

        cols: list[Column] = []
        if column_names is None:
            ncols = (str(i) for i in itertools.count(0))
        else:
            ncols = column_names

        for i, row in enumerate(matrix):
            if i == 1:
                cols[0].left = root
                cols[-1].right = root
                root.left = cols[-1]
                root.right = cols[0]
            row_nodes: list[Node] = []
            for j, elem in enumerate(row):
                if i == 0:
                    col = Column(name=next(ncols), col_idx=j)
                    if cols:
                        col.left = cols[-1]
                        cols[-1].right = col
                    cols.append(col)
                if elem:
                    node = Node(
                        row_idx=i,
                        col_idx=j,
                        col=cols[j],
                    )
                    cols[j].size += 1
                    up: Node | Column = node.col
                    while up.down:
                        up = up.down
                    node.up = up
                    up.down = node
                    if row_nodes:
                        node.left = row_nodes[-1]
                        row_nodes[-1].right = node
                    row_nodes.append(node)
            row_nodes[0].left = row_nodes[-1]
            row_nodes[-1].right = row_nodes[0]

        # point all the bottom nodes back to the top nodes and vice versa
        for col in cols:
            bottom = col.down
            while bottom.down:
                bottom = bottom.down
            bottom.down = col
            col.up = bottom

        return Problem(root)

    @staticmethod
    def from_board(board: Board) -> Problem:
        matrix, column_names = remove_empty_cols(*to_matrix(board))
        return Problem.from_matrix(matrix, iter(column_names)), matrix, column_names

    @property
    def active_cols(self) -> list[Column]:
        cols = []
        col = self.root.right
        while col.name != "__root__":
            cols.append(col)
            col = col.right
        return cols

    def __repr__(self):
        return "<Problem()>"

    def select_col(self, col_idx):
        j = 0
        col = self.root.right
        while col.name != "__root__":
            if j == col_idx:
                return col
            j += 1
            col = col.right

    def choose_column(self, naive: bool = False) -> Column:
        """Choose the next Column object to cover."""
        col = self.root.right

        if naive:
            return col

        min_size = 1_000_000_000
        while col.name != "__root__":
            s = col.size
            if s < min_size:
                min_col = col
                min_size = s
            col = col.right
        return min_col


def cell_to_idx() -> dict[str, int]:
    mapper = {}
    i = 0
    for c in "PRCB":
        for x in range(1, 10):
            for y in range(1, 10):
                mapper[f"{c}{x}{y}"] = i
                i += 1
    return mapper


def cell_to_row(
    cell: Cell, cell_to_idx_mapper: dict[str, int], row_len: int
) -> list[int]:
    row = [0] * row_len
    row[cell_to_idx_mapper[f"P{cell.row}{cell.col}"]] = 1
    row[cell_to_idx_mapper[f"R{cell.val}{cell.row}"]] = 1
    row[cell_to_idx_mapper[f"C{cell.val}{cell.col}"]] = 1
    row[cell_to_idx_mapper[f"B{cell.val}{cell.box}"]] = 1
    return tuple(row)


def to_matrix(board: Board) -> tuple[Iterable[Iterable[int]], tuple[str]]:
    cell_to_idx_mapper = cell_to_idx()
    row_len = len(cell_to_idx_mapper)
    rows = []
    for addr, cell in board.items():
        if cell.is_set():
            rows.append(cell_to_row(cell, cell_to_idx_mapper, row_len))
        else:
            for val in board.candidates(addr):
                rows.append(
                    cell_to_row(
                        board[addr].with_val(val), cell_to_idx_mapper, row_len
                    )
                )
    return tuple(rows), tuple(cell_to_idx_mapper)


def remove_empty_cols(
    matrix: Iterable[Iterable[int]], col_names: tuple[str]
) -> tuple[Iterable[Iterable[int]], tuple[str]]:
    tr = list(map(list, zip(*matrix)))
    tr_new = []
    col_names_new = []
    for col, col_name in zip(tr, col_names):
        if any(col):
            tr_new.append(col)
            col_names_new.append(col_name)
    return tuple(map(list, zip(*tr_new))), tuple(col_names_new)


def populate_board(board: Board, matrix: Iterable[Iterable[int]], col_names: tuple[str]) -> Board:

    for row in matrix:
        addr_found = False
        for col, name in zip(row, col_names):
            if col:
                if not addr_found:
                    r, c = name[1:]  # Remove P
                    addr = f"{c}{r}"  # board addresses are col, row
                    addr_found = True
                else:
                    val = name[1]  # {R,C,B}<val><row,col,box idx>
        board.set(addr, val)
    return board
