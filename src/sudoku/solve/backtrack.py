from typing import Iterator

from sudoku.models import Board


def candidate_boards(board: Board, addr: str, depth: int = 0) -> Iterator[Board]:
    for candidate in board.candidates(addr):
        board.set(addr, candidate)
        yield board
        naddr = board.next(addr)
        yield from candidate_boards(board, naddr, depth=depth + 1)
        board.unset(addr)


def solve(
    board: Board, iterations: int = 10000, **kwargs
) -> tuple[Board, int]:
    """Solve a sudoku puzzle."""

    for t, b in enumerate(candidate_boards(board, "11"), 1):
        if t >= iterations or b.is_completed():
            break
    return b, t
