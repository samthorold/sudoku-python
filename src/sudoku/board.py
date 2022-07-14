from __future__ import annotations
import copy
from dataclasses import dataclass


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


class CellIsSet(Exception):
    pass


def box(col, row):
    return (col - 1) // 3 + 3 * ((row - 1) // 3) + 1


@dataclass(slots=True)
class Cell:
    col: str
    row: str
    box: str
    val: str = "."

    def __str__(self):
        return f"{self.col}{self.row}"

    def with_val(self, val: str) -> Cell:
        if self.val != ".":
            raise CellIsSet(self)
        return Cell(
            col=self.col,
            row=self.row,
            box=self.box,
            val=val,
        )

    def neighbour(self, c: "Cell") -> bool:
        if self.col == c.col and self.row == c.row and self.box == c.box:
            return False
        return (self.col == c.col) or (self.row == c.row) or (self.box == c.box)

    def is_set(self):
        return len(self.val) == 1 and self.val != "."


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

    def items(self):
        return self.cells.items()

    def candidates(self, addr: str) -> str:
        if self[addr].val in self.OPTIONS:
            return self[addr].val
        return "".join(
            sorted(set(self.OPTIONS) - set(c.val for c in self.neighbours[addr]))
        )

    def next(self, addr: str) -> str:
        col, row = [int(x) for x in addr]
        if col == self.SIZE and row == self.SIZE:
            return "11"
        if col < self.SIZE:
            return f"{col + 1}{row}"
        return f"1{row + 1}"

    def set_val(self, addr: str, val: str) -> "Board":
        # board = copy.deepcopy(self)
        self[addr].val = val
        # return board

    def is_completed(self) -> bool:
        return all(c.val in self.OPTIONS for _, c in self.cells.items())
