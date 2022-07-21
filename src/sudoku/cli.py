import argparse
import logging

from sudoku.models import Board, Solver
from sudoku.solve import Backtrack, Dlx


parser = argparse.ArgumentParser()
parser.add_argument("method")
parser.add_argument("board_string")
parser.add_argument("--log_level", default="CRITICAL")
parser.add_argument("--iterations", default=100000, type=int)
parser.add_argument("--display", action="store_true")


if __name__ == "__main__":
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    solvers: dict[str, Solver] = {"backtrack": Backtrack(), "dlx": Dlx()}

    board = Board.from_string(args.board_string)
    print(board)
    solved_board = solvers[args.method].solve(
        board=board,
        iterations=args.iterations,
        display=args.display,
    )
    print(solved_board)
