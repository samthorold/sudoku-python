from dlx.cover import cover
from dlx.models import Problem
from dlx.uncover import uncover


def search(
    pr: Problem,
    depth: int = 0,
    soln: list[int] | None = None,
    soln_length: int | None = None,
):
    """Recursive algorithm for exact cover problem."""

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
        search(pr=pr, depth=depth + 1, soln=soln, soln_length=soln_length)
        if soln_length is not None and len(soln) == soln_length:
            return soln
        left = down.left
        while left and left != down:
            uncover(left.col)
            left = left.left
        down = down.down
    uncover(col)
    return soln
