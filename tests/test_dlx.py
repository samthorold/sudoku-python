import pytest

from dlx.examples import PROBLEM
from dlx.models import Column, choose_column, from_matrix
from dlx.search import search


def test_build_problem():
    root = from_matrix(PROBLEM)
    assert isinstance(root, Column)


@pytest.mark.parametrize("j,exp", ((0, 2), (3, 3), (6, 3)))
def test_column_size(example_problem, j, exp):
    i = -1
    col = example_problem
    while True:
        if i == j:
            assert col.size == exp
            break
        col = col.right
        i += 1


def test_choose_column(example_problem):
    got = choose_column(example_problem)
    assert got.name == "0"

    root = from_matrix(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
        ]
    )
    got = choose_column(root)
    assert got.name == "2"


def test_solution(example_problem):
    got = sorted(search(example_problem))
    assert got == [0, 3, 4]
