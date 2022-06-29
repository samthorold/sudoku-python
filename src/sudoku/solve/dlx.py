"""

https://en.wikipedia.org/wiki/Dancing_Links

- 9 columns for the cell values
- 81 columns for the cells
- 9 columns for the rows
- 9 columns for the columns
- 9 columns for the boxes

Columns as elements of a universe and rows as subsets and the problem is to
cover the universe with disjoint subsets.

0010110
1001001
0110010
1001000
0100001

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
from typing import Iterator, Iterable, TypeVar


T = TypeVar("T")


PROBLEM = (
    (0, 0, 1, 0, 1, 1, 0),
    (1, 0, 0, 1, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 1),
    (0, 0, 0, 1, 1, 0, 1),
)


@dataclass
class Node:
    """Node representing a 1 in the dancing links algorithm to solve the exact
    cover problem.

    Nodes are not necessarily adjacent in terms of row, column index.

    Attributes:
        left: Previous Node by moving along the columns
        right: Next Node by moving along the columns
        down: Previous Node by moving along the rows
        up: Next Node by moving along the rows
        col: Column header

    """

    col: Column
    left: Node | None = None
    right: Node | None = None
    up: Node | None = None
    down: Node | None = None


@dataclass
class Column:
    """

    Attributes:
        node: First Node in the column
        col: Root Column containing all active columns
        size: Number of Nodes in the column
        name: Human readable name for showing solution

    """
    name: str
    left: Column | None = None
    right: Column | None = None
    up: Node | None = None
    down: Node | None = None

    @property
    def size(self):
        n = 0
        down = self.down
        while down and not isinstance(down, Column):
            n += 1
            down = down.down
        return n


@dataclass
class Problem:
    """"""
    cols: list[Column]


def build_problem(
    matrix: Iterable[Iterable[int]],
) -> Problem:
    """Build a Problem object from an iterable of rows."""
    root = Column("root")

    cols: list[Column] = []

    for i, row in enumerate(matrix):
        left = None
        for j, elem in enumerate(row):
            if i == 0:
                cols.append(Column(str(j)))
                if j == 1:
                    cols[j].left = cols[j-1]
                    cols[j-1].right = cols[j]
            if i == 1:
                cols[-1].right = cols[0]
                cols[0].left = cols[-1]
            if elem:
                node = Node(col=cols[j])
                if not cols[j].down:
                    cols[j].down = node
                else:
                    up = node.col.down
                    while up.down and not isinstance(up, Column):
                        up = up.down
                    node.up = up
                    up.down = node
                if left:
                    node.left = left
                    left.right = node
                    left = node
                

    # point all the bottom nodes back to the top nodes and vice versa
    # and all the right nodes back the left nodes and vice versa
    for col in cols:
        bottom = col.down
        while bottom.down:
            bottom = bottom.down
        bottom.down = col.down
        col.up = bottom
        col.down.up = bottom

    return Problem(cols)


def choose_column(pr: Problem) -> Column:
    """Choose the next Column object to cover."""


def cover(col: Column) -> Problem:
    """Exclude the Column and associated rows from the search."""


def uncover(col: Column) -> Problem:
    """Include the Column and associated rows in the search."""


def solve(pr: Problem, depth: int = 0) -> Problem:
    """Recursive algorithm for exact cover problem."""
