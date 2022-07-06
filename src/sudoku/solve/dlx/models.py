"""

https://en.wikipedia.org/wiki/Dancing_Links

- 9 columns for the cell values
- 81 columns for the cells
- 9 columns for the rows
- 9 columns for the columns
- 9 columns for the boxes

Columns as elements of a universe and rows as subsets and the problem is to
cover the universe with disjoint subsets.

(
    (0, 0, 1, 0, 1, 1, 0),
    (1, 0, 0, 1, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 1),
    (0, 0, 0, 1, 1, 0, 1),
)

If A is empty, the problem is solved; terminate successfully.
Otherwise choose a column, c (deterministically).
Choose a row, r, such that A[r, c] = 1 (nondeterministically).
Include r in the partial solution.
For each j such that A[r, j] = 1,
    delete column j from matrix A;
    for each i such that A[i, j] = 1,
        delete row i from matrix A.
Repeat this algorithm recursively on the reduced matrix A.

Choose at each stage a column with fewest 1s in the current matrix A.

---

One good way to implement algorithm X is to represent each 1 in the matrix A as
a data object x with five fields L[x], R[x], U[x], D[x], C[x].

Rows and columns are doubly linked as circular lists.

Each column list also includes a special data object called its list header.

The list headers are part of a larger object called a column object.
Each column object y contains the fields L[y], R[y], U[y], D[y], and C[y] of
a data object and two additional fields, S[y] ("size") and N[y] ("name");
the size is the number of 1s in the column, and the name is a symbolic
identifier for printing the answers.

"""

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
        ncols = itertools.count(0) if column_names is None else column_names

        for i, row in enumerate(matrix):
            if i == 1:
                cols[0].left = root
                cols[-1].right = root
                root.left = cols[-1]
                root.right = cols[0]
            row_nodes = []
            for j, elem in enumerate(row):
                if i == 0:
                    col = Column(name=str(next(ncols)), col_idx=j)
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
