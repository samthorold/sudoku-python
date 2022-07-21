import pytest

from dlx.examples import PROBLEM
from dlx.models import Problem, from_matrix
from dlx.search import search


def test_build_problem():
    prob = from_matrix(PROBLEM)
    assert isinstance(prob, Problem)


@pytest.mark.parametrize("j,exp", ((0, 2), (3, 3), (6, 3)))
def test_column_size(example_problem, j, exp):
    i = -1
    col = example_problem.root
    while True:
        if i == j:
            assert col.size == exp
            break
        col = col.right
        i += 1


def test_choose_column(example_problem):
    got = example_problem.choose_column()
    assert got.name == "0"

    prob = from_matrix(
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
        ]
    )
    got = prob.choose_column()
    assert got.name == "2"


def test_solution(example_problem):
    got = sorted(search(example_problem))
    assert got == [0, 3, 4]
