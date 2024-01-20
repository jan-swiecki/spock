import pytest
from pytest import fixture


@fixture(scope="function", name='my_fixture')
def _my_fixture():
    yield 1000


def test_spock1(my_fixture):
    assert my_fixture == 1000


@pytest.mark.spock("{a} == {b} + 1000")
def test_spock2():
    def expect(my_fixture, a, b):
        assert a == b + my_fixture

    def where(_, a, b):
        _ | a    | b
        _ | 1001 | 1


@pytest.mark.spock("{a} == {b} + 1 + 1000")
def test_spock3():
    def given(my_fixture, me):
        me.data = {'value': my_fixture}

    def when(data):
        data['value'] += 1

    def then(a, b, data, my_fixture):
        assert a == b + data['value'] - 1
        assert a == b + my_fixture

    def where(_, a, b):
        _ | a    | b
        _ | 1001 | 1