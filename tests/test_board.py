import pytest

from yass.models import Board, InvalidBoard, invalid_board


def test_board_str(board_string: str) -> None:
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


def test_neighbours(board_string: str) -> None:
    board = Board.from_string(board_string)
    assert "".join(sorted(board.neighbour_vals("31"))) == "356789"


@pytest.mark.parametrize(
    "addr,exp",
    (
        ("11", "5"),
        ("31", "124"),
    ),
)
def test_candidates(board_string: str, addr: str, exp: str) -> None:
    candidates = Board.from_string(board_string).candidates(addr)
    assert candidates, "Expected some candidates"
    assert "".join(sorted(candidates)) == exp


def test_is_completed() -> None:
    string = "1" * 81
    board = Board.from_string(string)
    assert board.is_completed()


def test_cannot_unset_original_cell(board_string: str) -> None:
    board = Board.from_string(board_string)
    addr = "11"
    board.unset(addr)
    assert board[addr].val == "5"


def test_valid_board(board_string: str) -> None:
    assert not invalid_board(board_string)
    assert invalid_board(board_string[:-1])


def test_from_string(board_string: str) -> None:
    _ = Board.from_string(board_string)
    with pytest.raises(InvalidBoard):
        _ = Board.from_string(board_string[:-1])
