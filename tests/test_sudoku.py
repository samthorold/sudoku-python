from sudoku.board import Board


def test_board_str(board_string):
    got = str(Board.from_string(board_string))
    expected = (
        "53.|.7.|...\n"
        "6..|195|...\n"
        ".98|...|.6.\n"
        "---|---|---\n"
        "8..|.6.|..3\n"
        "4..|8.3|..1\n"
        "7..|.2.|..6\n"
        "---|---|---\n"
        ".6.|...|28.\n"
        "...|419|..5\n"
        "...|.8.|.79\n"
    )
    assert got == expected


def test_neighbours(board_string):
    board = Board.from_string(board_string)
    assert "".join(sorted(set(c.val for c in board.neighbours["31"]))) == ".356789"


def test_candidates(board_string):
    assert Board.from_string(board_string).candidates("11") == "5"
    assert Board.from_string(board_string).candidates("31") == "124"


def test_is_completed():
    board = Board()
    for _, cell in board.cells.items():
        cell.val = "1"
    assert board.is_completed()
