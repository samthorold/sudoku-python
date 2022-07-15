import argparse
import logging
import sys

from sudoku.board import Board
from sudoku.solve import backtrack, dlx


SOLVERS = {"backtrack": backtrack, "dlx": dlx}


parser = argparse.ArgumentParser()
parser.add_argument("method")
parser.add_argument("board_string")
parser.add_argument("--log_level", default="CRITICAL")
parser.add_argument("--iterations", default=100000, type=int)
parser.add_argument("--display", action="store_true")
parser.add_argument("--naive", action="store_true")


if __name__ == "__main__":
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    board = Board.from_string(args.board_string)
    print(board)
    solved_board, *addl = SOLVERS[args.method].solve(
        board=board,
        iterations=args.iterations,
        display=args.display,
        naive=args.naive,
    )
    print(solved_board)
