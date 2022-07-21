from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Sequence

from sudoku.models import Board, Cell


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


@dataclass
class Problem:
    root: Column
    next_min_col: Column | None = None

    @staticmethod
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
        col = self.root.right

        min_size = 1_000_000_000
        while col.name != "__root__":
            s = col.size
            if s < min_size:
                min_col = col
                min_size = s
            col = col.right
        return min_col


def from_matrix(
    matrix: Sequence[Sequence[int]],
    column_names: Sequence[str] | None = None,
) -> Problem:
    """Build a Problem object from a sequence of rows."""

    root = Column("__root__", -1)

    cols: list[Column] = []
    if column_names is None:
        ncols = tuple(str(i) for i in range(len(matrix[0])))
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
                col = Column(name=ncols[j], col_idx=j)
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
