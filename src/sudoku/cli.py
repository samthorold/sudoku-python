import sys

from sudoku.solve import backtrack


if __name__ == "__main__":
    board_string, it, displ = sys.argv[1:]
    _ = backtrack.solve(board_string, int(it), bool(displ))
