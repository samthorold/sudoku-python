import pytest

from yass.models import Cell


def test_is_set():
    c = Cell("", "", "")
    assert not c.is_set()

    sc = c.with_val("4")
    assert sc.is_set()

    with pytest.raises(ValueError):
        _ = sc.with_val("9")
