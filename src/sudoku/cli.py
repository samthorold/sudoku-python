import sys

from sudoku.board import Board
from sudoku.solve import backtrack


SOLVERS = {
    "backtrack": backtrack,
}


if __name__ == "__main__":
    board_string, method, it, displ = sys.argv[1:]
    board = Board.from_string(board_string)
    solved_board, *_ = SOLVERS[method].solve(board, int(it), bool(int(displ)))
    print(solved_board)
