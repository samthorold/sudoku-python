import logging

from sudoku.board import Board
from sudoku.solve.dlx.models import Column, Node, Problem


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


def cover(col: Column):
    """Exclude the Column and associated rows from the search."""

    logger.info(f"Covering {col}")

    col.left.right = col.right
    col.right.left = col.left

    logger.debug(f"{col.left.right=}, {col.right.left=}")

    if col.down == col:
        return

    cover_node = col.down

    while cover_node != col:
        logger.debug(f"{cover_node=}")

        node = cover_node.right

        while node != cover_node:
            logger.info(f"Removing {node}")
            node.up.down = node.down
            node.down.up = node.up
            logger.debug(f"{node.up.down=}, {node.down.up=}")
            node = node.right

        cover_node = cover_node.down


def uncover(col: Column):
    """Include the Column and associated rows in the search."""

    logger.info(f"Uncovering {col}")

    cover_node = col.up

    while not isinstance(cover_node, Column):
        logger.debug(f"{cover_node=}")

        node = cover_node.left

        while node != cover_node:
            logger.info(f"Adding {node}")
            node.up.down = node
            node.down.up = node
            logger.debug(f"{node.up.down=}, {node.down.up=}")
            node = node.left

        cover_node = cover_node.up

    col.left.right = col
    col.right.left = col

    logger.debug(f"{col.left.right=}, {col.right.left=}")


def search(pr: Problem, depth: int = 0, soln: list[int] | None = None):
    """Recursive algorithm for exact cover problem."""

    logger.warning(
        f"Entered search {depth=} {soln=} {', '.join(str(c) for c in pr.active_cols)}"
    )

    soln = [] if soln is None else soln

    if pr.root.right.name == "__root__":
        return soln

    col = pr.choose_column()

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
        search(pr, depth + 1, soln)
        left = down.left
        while left and left != down:
            uncover(left.col)
            left = left.left
        down = down.down
    uncover(col)
    logger.warning(
        f"Exit search {depth=} {soln=} {', '.join(str(c) for c in pr.active_cols)}"
    )
    return soln


def solve(board: Board, **kwargs) -> tuple[Board, int]:
    """Solve a sudoku puzzle."""
