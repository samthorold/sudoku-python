import pytest

from sudoku.solve import dlx


def test_build_problem():
    prob = dlx.build_problem(dlx.PROBLEM)
    assert isinstance(prob, dlx.Problem)


@pytest.mark.parametrize(
    "j,exp",
    ((0, 2), (3, 3), (-1, 3))
)
def test_column_size(j, exp):
    prob = dlx.build_problem(dlx.PROBLEM)
    assert prob.cols[j].size == exp
