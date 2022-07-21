from typing import Iterator

from sudoku.models import Board, Solver


def candidate_boards(board: Board, addr: str, depth: int = 0) -> Iterator[Board]:
    candidates = board.candidates(addr)
    assert candidates is not None
    for candidate in candidates:
        board.set(addr, candidate)
        yield board
        naddr = board.next(addr)
        yield from candidate_boards(board, naddr, depth=depth + 1)
        board.unset(addr)


class Backtrack:
    def solve(self, board: Board, iterations: int = 10000, **kwargs) -> Board:
        """Solve a sudoku puzzle."""

        b = board

        for t, b in enumerate(candidate_boards(board, "11"), 1):
            if t >= iterations or b.is_completed():
                break
        return b
