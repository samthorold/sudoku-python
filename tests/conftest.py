import pytest

from yass.dlx.examples import PROBLEM
from yass.dlx.models import Column, from_matrix


@pytest.fixture
def board_string() -> str:
    return (
        "53..7...."
        "6..195..."
        ".98....6."
        "8...6...3"
        "4..8.3..1"
        "7...2...6"
        ".6....28."
        "...419..5"
        "....8..79"
    )


@pytest.fixture
def soln_string() -> str:
    return (
        "534|678|912\n"
        "672|195|348\n"
        "198|342|567\n"
        "---|---|---\n"
        "859|761|423\n"
        "426|853|791\n"
        "713|924|856\n"
        "---|---|---\n"
        "961|537|284\n"
        "287|419|635\n"
        "345|286|179\n"
    )


@pytest.fixture
def example_problem() -> Column:
    return from_matrix(PROBLEM)
