import logging

from sudoku.solve.dlx.models import Column, Problem


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

    cover_node = col.down
    cover_col_ix = cover_node.col_idx

    while not isinstance(cover_node, Column) and cover_node.down:
        logger.debug(f"{cover_node=}")

        node = cover_node.right

        while node.col_idx != cover_col_ix:
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
    cover_col_ix = cover_node.col_idx

    while not isinstance(cover_node, Column) and cover_node.up:
        logger.debug(f"{cover_node=}")

        node = cover_node.left

        while node.col_idx != cover_col_ix:
            logger.info(f"Adding {node}")
            node.up.down = node
            node.down.up = node
            logger.debug(f"{node.up.down=}, {node.down.up=}")
            node = node.left

        cover_node = cover_node.up

    col.left.right = col
    col.right.left = col

    logger.debug(f"{col.left.right=}, {col.right.left=}")


def search(pr: Problem, depth: int = 0):
    """Recursive algorithm for exact cover problem."""

    logging.info(f"{depth=}")

    # breakpoint()

    if pr.root.right.name == "__root__":
        return

    if any(not c.size for c in pr.active_cols):
        return

    col = pr.choose_column()

    cover(col)
    down = col.down
    while down and down != col:
        right = down.right
        while right and right != down:
            cover(right.col)
            right = right.right
        search(pr, depth + 1)
        left = down.left
        while left and left != down:
            uncover(left.col)
            left = left.left
    uncover(col)
