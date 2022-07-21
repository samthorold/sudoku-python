from dlx.models import Column


def uncover(col: Column):
    """Include the Column and associated rows in the search."""

    cover_node = col.up
    while cover_node != col:
        node = cover_node.left
        while node != cover_node:
            node.up.down = node
            node.down.up = node
            node.col.size += 1
            node = node.left
        cover_node = cover_node.up
    col.left.right = col
    col.right.left = col
