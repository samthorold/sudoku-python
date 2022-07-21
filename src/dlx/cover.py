from dlx.models import Column


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
            node.up.down = node.down
            node.down.up = node.up
            node.col.size -= 1
            node = node.right
        cover_node = cover_node.down
