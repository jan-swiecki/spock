from typing import Any
from typing import Callable

import pytest

from _spock.parameter import AddArgumentsFailed
from _spock.parameter import BuildExpressionError
from _spock.parameter import Expression
from _spock.parameter import Parameter
from _spock.parameter import declare


@pytest.fixture(scope="function")
def a():
    return Parameter("a")


@pytest.fixture(scope="function")
def b():
    return Parameter("b")


class TestParameter:
    def test_repr(self, a: Parameter):
        assert repr(a) == "Parameter(a)"

    def test_call(self, a: Parameter):
        assert a(a=1) == 1

    def test_bitwise_left_shift_operator(self, a: Parameter):
        a << [1, 2, 3]
        assert a.__param_arguments__ == [1, 2, 3]

        with pytest.raises(AddArgumentsFailed):
            a << 2

    def test_bitwise_right_shift_operator(self, a: Parameter):
        [1, 2, 3] >> a
        assert a.__param_arguments__ == [1, 2, 3]

        with pytest.raises(AddArgumentsFailed):
            2 >> a  # type: ignore

    def test_handle_operator_when_deny_accept_expression(self, a: Parameter):
        with pytest.raises(BuildExpressionError):
            a + 1

    @pytest.mark.parametrize(
        "exp,arg,expected",
        [
            (lambda a: +a, 1, 1),
            (lambda a: -a, 1, -1),
            (lambda a: ~a, 0, -1),
            (lambda a: a + 1, 1, 2),
            (lambda a: a - 1, 1, 0),
            (lambda a: a * 2, 2, 4),
            (lambda a: a / 2, 5, 2.5),
            (lambda a: a // 2, 5, 2),
            (lambda a: a % 2, 5, 1),
            (lambda a: a ** 2, 5, 25),
            (lambda a: a << 1, 5, 10),
            (lambda a: a >> 1, 5, 2),
            (lambda a: a & 1, 5, 1),
            (lambda a: a | 1, 5, 5),
            (lambda a: a ^ 1, 5, 4),
            (lambda a: a > 5, 4, False),
            (lambda a: a >= 5, 5, True),
            (lambda a: a < 5, 4, True),
            (lambda a: a <= 5, 5, True),
            (lambda a: a == 5, 5, True),
            (lambda a: a != 5, 6, True),
        ],
    )
    def test_operator(self, a: Parameter, exp: Callable[[Parameter], Any], arg: Any, expected: Any):
        a.__accept_expression__ = True
        assert exp(a)(a=arg) == expected

    @pytest.mark.parametrize(
        "exp,arg,expected",
        [
            (lambda a, b: a + b, (4, 5), 9),
            (lambda a, b: a - b * 4, (50, 2), 42),
            (lambda a, _: a + a, (4, 9), 8),
            (lambda a, b: a + (b ** 4) // 2 << 3, (4, 2), 96),
        ],
    )
    def test_multi_params(
        self, a: Parameter, b: Parameter, exp: Callable[[Parameter, Parameter], Any], arg: Any, expected: Any
    ):
        a.__accept_expression__ = True
        b.__accept_expression__ = True
        assert exp(a, b)(a=arg[0], b=arg[1]) == expected


def test_declare():
    a, b, c = declare("a", "b", "c")
    assert a.__name__ == "a"
    assert b.__name__ == "b"
    assert c.__name__ == "c"


@pytest.mark.parametrize(
    "exp,arg,expected",
    [
        (lambda a: +a, 1, 1),
        (lambda a: -a, 1, -1),
        (lambda a: ~a, 0, -1),
        (lambda a: a + 1, 1, 2),
        (lambda a: a - 1, 1, 0),
        (lambda a: a * 2, 2, 4),
        (lambda a: a / 2, 5, 2.5),
        (lambda a: a // 2, 5, 2),
        (lambda a: a % 2, 5, 1),
        (lambda a: a ** 2, 5, 25),
        (lambda a: a << 1, 5, 10),
        (lambda a: a >> 1, 5, 2),
        (lambda a: a & 1, 5, 1),
        (lambda a: a | 1, 5, 5),
        (lambda a: a ^ 1, 5, 4),
        (lambda a: a > 5, 4, False),
        (lambda a: a >= 5, 5, True),
        (lambda a: a < 5, 4, True),
        (lambda a: a <= 5, 5, True),
        (lambda a: a == 5, 5, True),
        (lambda a: a != 5, 6, True),
    ],
)
def test_expression(exp: Callable, arg: Any, expected: Any):
    assert exp(Expression(lambda a: a))(a=arg) == expected


def test_multi_expression():
    exp1 = Expression(lambda a, **_: a)
    exp2 = Expression(lambda b, **_: b)
    assert (exp1 - 5 + exp2 * 3)(a=20, b=3) == (15 + 9)