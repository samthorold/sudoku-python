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


@dataclass
class Node:
    val: int
    left: Node | None = None
    right: Node | None = None


def insert_before(node: Node, new: Node) -> Node:
    if node.left:
        node.left.right = new
        new.left = node.left
    new.right = node
    node.left = new
    return new


def insert_after(node: Node, new: Node) -> Node:
    if node.right:
        new.right = node.right
        new.right.left = new
    new.left = node
    node.right = new
    return new


def pairs(nodes: Iterable[T]) -> Iterator[tuple[T, T]]:
    pair = []
    for node in nodes:
        pair.append(node)
        if len(pair) > 1:
            yield tuple(pair)
        if len(pair) >= 2:
            pair = pair[-1:]


def create_list(nodes: Iterable[Node]):
    for left, right in pairs(nodes):
        yield insert_after(left, right)


def forwards(node: Node) -> Iterator[Node]:
    yield node
    while node := node.right:
        yield node
