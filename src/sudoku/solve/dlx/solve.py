import logging

from sudoku.models import Board
from sudoku.solve.dlx.models import Column, Node, Problem, to_board


logger = logging.getLogger(__name__)


PROBLEM = (
    (0, 0, 1, 0, 1, 1, 0),
    (1, 0, 0, 1, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 1),
    (0, 0, 0, 1, 1, 0, 1),
)
PROBLEM_COLUMN_NAMES = "ABCDEFG"


def inner_cover(node: Node) -> None:
    node.up.down = node.down
    node.down.up = node.up
    node.col.size -= 1


def cover(col: Column):
    """Exclude the Column and associated rows from the search."""

    col.left.right = col.right
    col.right.left = col.left

    if col.down == col:
        return

    cover_node = col.down

    while cover_node != col:

        node = cover_node.right

        while node != cover_node:
            inner_cover(node)
            node = node.right

        cover_node = cover_node.down


def inner_uncover(node: Node) -> None:
    node.up.down = node
    node.down.up = node
    node.col.size += 1


def uncover(col: Column):
    """Include the Column and associated rows in the search."""

    cover_node = col.up

    while not isinstance(cover_node, Column):

        node = cover_node.left

        while node != cover_node:
            inner_uncover(node)
            node = node.left

        cover_node = cover_node.up

    col.left.right = col
    col.right.left = col


def search(
    pr: Problem,
    depth: int = 0,
    soln: list[int] | None = None,
    soln_length: int | None = None,
    naive: bool = False,
):
    """Recursive algorithm for exact cover problem."""

    soln = [] if soln is None else soln

    if pr.root.right.name == "__root__":
        return soln

    col = pr.choose_column(naive)

    cover(col)
    down = col.down
    while down and down != col:
        if not soln or depth >= len(soln):
            soln.append(down.row_idx)
        else:
            soln[depth] = down.row_idx
        right = down.right
        while right and right != down:
            cover(right.col)
            right = right.right
        search(pr=pr, depth=depth + 1, soln=soln, soln_length=soln_length, naive=naive)
        if soln_length is not None and len(soln) == soln_length:
            return soln
        left = down.left
        while left and left != down:
            uncover(left.col)
            left = left.left
        down = down.down
    uncover(col)
    return soln


def solve(board: Board, naive: bool = False, **kwargs) -> tuple[Board, int]:
    """Solve a sudoku puzzle."""

    pr, m, c = Problem.from_board(board)
    soln = search(pr, soln_length=81, naive=naive)
    return to_board([x for i, x in enumerate(m) if i in soln], c), 0
