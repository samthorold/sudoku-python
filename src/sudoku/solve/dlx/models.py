from __future__ import annotations
from dataclasses import dataclass
import itertools
import logging
from typing import Iterable


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

    @property
    def size(self):
        n = 0
        down = self.down
        while down and not isinstance(down, Column):
            n += 1
            down = down.down
        return n

    def __repr__(self):
        return f"<Column({self.name})>"

    def __str__(self):
        s = f"{self.name}["
        node = self.down

        while node and node != self:
            s += f"{node.row_idx}"
            node = node.down

        s += "]"

        return s


@dataclass
class Problem:
    root: Column

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
                    logger.debug(f"{col=}")
                if elem:
                    node = Node(
                        row_idx=i,
                        col_idx=j,
                        col=cols[j],
                    )
                    logger.debug(f"Created {node=}")
                    up: Node | Column = node.col
                    while up.down:
                        up = up.down
                    node.up = up
                    up.down = node
                    if row_nodes:
                        node.left = row_nodes[-1]
                        row_nodes[-1].right = node
                    row_nodes.append(node)
                    logger.debug(f"{node=}")
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
        return Problem.from_matrix(matrix, iter(column_names))

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

    def choose_column(self) -> Column:
        """Choose the next Column object to cover."""
        min_size = 1_000_000_000
        col = self.root.right
        j = min_j = 0
        while col.name != "__root__":
            s = col.size
            if s < min_size:
                min_size = s
                min_j = j
            j += 1
            col = col.right
        return self.select_col(min_j)


def cell_to_idx() -> dict[str, int]:
    mapper = {}
    i = 0
    for v in range(1, 10):
        for r in range(1, 10):
            for c in range(1, 10):
                mapper[f"{v}{r}{c}"] = i
                i += 1
        for r in range(1, 10):
            mapper[f"{v}r{r}"] = i
            i += 1
        for c in range(1, 10):
            mapper[f"{v}c{c}"] = i
            i += 1
        for b in range(1, 10):
            mapper[f"{v}b{b}"] = i
            i += 1
    return mapper


def cell_to_row(
    cell: Cell, cell_to_idx_mapper: dict[str, int], row_length: int
) -> list[int]:
    row = [0] * row_length
    val_idx = cell_to_idx_mapper[f"{cell.val}{cell.row}{cell.col}"]
    row_idx = cell_to_idx_mapper[f"{cell.val}r{cell.row}"]
    col_idx = cell_to_idx_mapper[f"{cell.val}c{cell.col}"]
    box_idx = cell_to_idx_mapper[f"{cell.val}b{cell.box}"]
    row[val_idx] = 1
    row[row_idx] = 1
    row[col_idx] = 1
    row[box_idx] = 1
    return tuple(row)


def to_matrix(board: Board) -> tuple[Iterable[Iterable[int]], tuple[str]]:
    cell_to_idx_mapper = cell_to_idx()
    row_length = len(cell_to_idx_mapper)
    rows = []
    for addr, cell in board.items():
        if cell.is_set():
            rows.append(cell_to_row(cell, cell_to_idx_mapper, row_length))
        else:
            for val in board.candidates(addr):
                rows.append(
                    cell_to_row(
                        board[addr].with_val(val), cell_to_idx_mapper, row_length
                    )
                )
    return tuple(rows), tuple(cell_to_idx_mapper)


def empty_cols(matrix: Iterable[Iterable[int]]) -> list[int]:
    tr = list(map(list, zip(*matrix)))
    cols = []
    for j, col in enumerate(tr):
        if all(i == 0 for i in col):
            cols.append(j)
    return cols


def remove_empty_cols(
    matrix: Iterable[Iterable[int]], col_names: tuple[str]
) -> tuple[Iterable[Iterable[int]], tuple[str]]:
    to_remove = empty_cols(matrix)
    tr = list(map(list, zip(*matrix)))
    tr_new = []
    col_names_new = []
    for j, (col, col_name) in enumerate(zip(tr, col_names)):
        if j not in to_remove:
            tr_new.append(col)
            col_names_new.append(col_name)
    return tuple(map(list, zip(*tr_new))), tuple(col_names_new)
