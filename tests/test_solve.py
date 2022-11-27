import pytest

from yass.models import Board, Solver
from yass.solve import Backtrack, Dlx


@pytest.mark.parametrize("solver", (Dlx(), Backtrack()))
def test_solve_sudoku(solver: Solver, board_string: str, soln_string: str) -> None:
    board = Board.from_string(board_string)
    soln = solver.solve(board)

    assert str(soln) == soln_string
