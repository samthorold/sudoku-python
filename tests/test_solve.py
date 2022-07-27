import pytest

from yass.models import Board
from yass.solve import Backtrack, Dlx


@pytest.mark.parametrize("solver", (Dlx, Backtrack))
def test_solve_sudoku(solver, board_string, soln_string):
    board = Board.from_string(board_string)
    soln = solver().solve(board)

    assert str(soln) == soln_string
