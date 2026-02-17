import pytest
from app.example import add, multiply

@pytest.mark.parametrize("a, b, res", [
    (2, 3, 5), (5, 5, 10), (-1, -1, -2)
])
def test_add(a, b, res) :
    print ("Testing add function")
    assert add(a, b) == res


@pytest.mark.parametrize ("a, b, res", [
    (1, 1, 1), (1, 2, 2), (0, 0, 0),
    (-1, -1, 1), (-1, 0, 0)
])
def test_multiply(a, b, res) :
    print ("Testing multiply function")
    assert multiply(a, b) == res
