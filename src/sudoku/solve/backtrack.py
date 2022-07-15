from typing import Iterator

from sudoku.board import Board


def candidate_boards(board: Board, addr: str, depth: int = 0) -> Iterator[Board]:
    for candidate in board.candidates(addr):
        if board[addr].val == ".":
            board.set_val(addr, candidate)
        yield board
        naddr = board.next(addr)
        yield from candidate_boards(board, naddr, depth=depth + 1)
        board.set_val(addr, ".")


def solve(
    board: Board, iterations: int = 10000, display: bool = False, **kwargs
) -> tuple[Board, int]:
    """Solve a sudoku puzzle."""

    trials = 0
    candidates = candidate_boards(board, "11")
    for _ in range(iterations):
        if board.is_completed():
            break
        board = next(candidates)
        trials += 1
        if display:
            print(trials)
            print(board)

    return board, trials
