import pytest

from sudoku.board import box


@pytest.mark.parametrize(
    "col,row,exp",
    (
        (1, 1, 1),
        (2, 1, 1),
        (3, 1, 1),
        (4, 1, 2),
        (5, 1, 2),
        (6, 1, 2),
        (7, 1, 3),
        (8, 1, 3),
        (9, 1, 3),
        (1, 2, 1),
        (2, 2, 1),
        (3, 2, 1),
        (4, 2, 2),
        (5, 2, 2),
        (6, 2, 2),
        (7, 2, 3),
        (8, 2, 3),
        (9, 2, 3),
        (1, 3, 1),
        (2, 3, 1),
        (3, 3, 1),
        (4, 3, 2),
        (5, 3, 2),
        (6, 3, 2),
        (7, 3, 3),
        (8, 3, 3),
        (9, 3, 3),
        (1, 4, 4),
        (2, 4, 4),
        (3, 4, 4),
        (4, 4, 5),
        (5, 4, 5),
        (6, 4, 5),
        (7, 4, 6),
        (8, 4, 6),
        (9, 4, 6),
        (1, 5, 4),
        (2, 5, 4),
        (3, 5, 4),
        (4, 5, 5),
        (5, 5, 5),
        (6, 5, 5),
        (7, 5, 6),
        (8, 5, 6),
        (9, 5, 6),
        (1, 6, 4),
        (2, 6, 4),
        (3, 6, 4),
        (4, 6, 5),
        (5, 6, 5),
        (6, 6, 5),
        (7, 6, 6),
        (8, 6, 6),
        (9, 6, 6),
        (1, 7, 7),
        (2, 7, 7),
        (3, 7, 7),
        (4, 7, 8),
        (5, 7, 8),
        (6, 7, 8),
        (7, 7, 9),
        (8, 7, 9),
        (9, 7, 9),
        (1, 8, 7),
        (2, 8, 7),
        (3, 8, 7),
        (4, 8, 8),
        (5, 8, 8),
        (6, 8, 8),
        (7, 8, 9),
        (8, 8, 9),
        (9, 8, 9),
        (1, 9, 7),
        (2, 9, 7),
        (3, 9, 7),
        (4, 9, 8),
        (5, 9, 8),
        (6, 9, 8),
        (7, 9, 9),
        (8, 9, 9),
        (9, 9, 9),
    ),
)
def test_box(col, row, exp):
    assert box(col, row) == exp