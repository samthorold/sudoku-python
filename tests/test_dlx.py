import pytest

from sudoku.solve.dlx.models import Problem
from sudoku.solve.dlx.solve import PROBLEM, search


def test_build_problem():
    prob = Problem.from_matrix(PROBLEM)
    assert isinstance(prob, Problem)


@pytest.mark.parametrize("j,exp", ((0, 2), (3, 3), (6, 3)))
def test_column_size(j, exp):
    prob = Problem.from_matrix(PROBLEM)
    i = -1
    col = prob.root
    while True:
        if i == j:
            assert col.size == exp
            break
        col = col.right
        i += 1


def test_choose_column():
    prob = Problem.from_matrix(PROBLEM)
    got = prob.choose_column()
    assert got.name == "0"

    prob = Problem.from_matrix(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
        ]
    )
    got = prob.choose_column()
    assert got.name == "2"


def test_solution():
    got = sorted(search(Problem.from_matrix(PROBLEM)))
    assert got == [0, 3, 4]
