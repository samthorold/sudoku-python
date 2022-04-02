"""

https://en.wikipedia.org/wiki/Sudoku

"""

import copy
from dataclasses import dataclass
import sys
from typing import Iterator


BOARDS = [
    (
        "53..7...."
        "6..195..."
        ".98....6."
        "8...6...3"
        "4..8.3..1"
        "7...2...6"
        ".6....28."
        "...419..5"
        "....8..79"
    ),
]


def box(col, row):
    return (col - 1) // 3 + 3 * ((row - 1) // 3) + 1


@dataclass
class Cell:
    col: str
    row: str
    box: str
    val: str = "."

    def __str__(self):
        return f"{self.col}{self.row}"

    def neighbour(self, c: "Cell") -> bool:
        if self.col == c.col and self.row == c.row and self.box == c.box:
            return False
        return (self.col == c.col) or (self.row == c.row) or (self.box == c.box)


class InvalidBoard(Exception):
    """"""


def valid_board(string: str):
    err = {}
    if not len(string) == 81:
        err["msg"] = "Incorrect number of cells"
    return err


class Board:
    """Sudoku board."""

    SIZE = 9
    OPTIONS = "123456789"

    @classmethod
    def from_string(cls, string: str) -> "Board":
        board = cls()
        if err := valid_board(string):
            raise InvalidBoard(err["msg"])
        for cell, val in zip(board, string):
            if val in board.OPTIONS:
                board[cell].val = val
        return board

    def __init__(self):
        self.cells = {
            f"{col}{row}": Cell(
                str(col),
                str(row),
                str(box(col, row)),
            )
            for row in range(1, self.SIZE + 1)
            for col in range(1, self.SIZE + 1)
        }
        self.neighbours = {
            f"{col}{row}": [
                c
                for _, c in self.cells.items()
                if c.neighbour(self.cells[f"{col}{row}"])
            ]
            for row in range(1, self.SIZE + 1)
            for col in range(1, self.SIZE + 1)
        }

    def __iter__(self):
        return iter(self.cells)

    def __getitem__(self, k):
        return self.cells[k]

    def __str__(self):
        s = ""
        for row in range(1, self.SIZE + 1):
            for col in range(1, self.SIZE + 1):
                s += self[f"{col}{row}"].val
                if col in [3, 6]:
                    s += "|"
            s += "\n"
            if row in [3, 6]:
                s += "---|---|---\n"
        return s

    def candidates(self, addr: str) -> str:
        return "".join(
            sorted(set(self.OPTIONS) - set(c.val for c in self.neighbours[addr]))
        )

    def next(self, addr: str) -> str:
        col, row = [int(x) for x in addr]
        if col == self.SIZE and row == self.SIZE:
            return
        if col < self.SIZE:
            return f"{col + 1}{row}"
        return f"1{row + 1}"

    def set_val(self, addr: str, val: str) -> "Board":
        board = copy.deepcopy(self)
        board[addr].val = val
        return board


def candidate_boards(board: Board, addr: str, depth: int = 0) -> Iterator[Board]:
    while board[addr].val != ".":
        addr = board.next(addr)
    if not (candidates := board.candidates(addr)):
        return
    for candidate in candidates:
        cboard = board.set_val(addr, candidate)
        yield cboard
        naddr = board.next(addr)
        yield from candidate_boards(cboard, naddr, depth=depth + 1)


def main(string: str, iterations: int = 10000, display: bool = False) -> Board:
    """Solve a sudoku puzzle."""

    board = Board.from_string(string)
    candidates = candidate_boards(board, "11")
    for _ in range(iterations):
        cboard = next(candidates)
        if display:
            print(cboard)

    return cboard


if __name__ == "__main__":
    string, it, displ = sys.argv[1:]

    _ = main(string, int(it), bool(displ))
