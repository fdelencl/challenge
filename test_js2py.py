#!/usr/bin/env python3
import pytest

from .js2py import js2py


def test_empty():
    assert js2py('', {'a': 1}) == {'a': 1}


@pytest.mark.parametrize('js, context, expected', [
    ['a = a + 1', {'a': 1}, {'a': 2}],
    ['a = a + -1', {'a': -1}, {'a': -2}],
    ['a = a-1', {'a': -1}, {'a': -2}],
    ['a = a + b', {'a': 1, 'b': 2}, {'a': 3, 'b': 2}],
    ['a = a - b', {'a': 1, 'b': 2}, {'a': -1, 'b': 2}],
    ['a.x = a.x - 1', {'a': {'x': 1}}, {'a': {'x': 0}}],
    ['a.b = a.x - 1', {'a': {'x': 1}}, {'a': {'b': 0, 'x': 1}}],
    ['a.b.c = a.x - 5', {'a': {'b': {'c': 0}, 'x': 1}}, {'a': {'b': {'c': -4}, 'x': 1}}],
])
def test_math(js, context, expected):
    assert js2py(js, context) == expected


@pytest.mark.parametrize('js, context, expected', [
    ['a = a && true', {'a': False}, {'a': False}],
    ['a = a && true', {'a': True}, {'a': True}],
    ['a = a || true', {'a': False}, {'a': True}],
    ['a = a || true', {'a': True}, {'a': True}],
])
def test_bool(js, context, expected):
    assert js2py(js, context) == expected


@pytest.mark.parametrize('js, context, expected', [
    ['if (a>3) { a = 0}', {'a': 4}, {'a': 0}],
    ['if (a>3) { a = 0}', {'a': 3}, {'a': 3}],
    ['if (a>3 && b == 1) { a = 0}', {'a': 4, 'b': 1}, {'a': 0, 'b': 1}],
    ['if (a>3 && b == 1) { a = 0}', {'a': 4, 'b': 2}, {'a': 4, 'b': 2}],
    ['if (a>3 || b == 1) { a = 0}', {'a': 3, 'b': 1}, {'a': 0, 'b': 1}],
    ['if (b == 1){ if (a > 3) { a = 0}}', {'a': 4, 'b': 1}, {'a': 0, 'b': 1}],
    ['if (b == 1){ if (a > 3) { a = 0}}', {'a': 3, 'b': 1}, {'a': 3, 'b': 1}],
])
def test_if(js, context, expected):
    assert js2py(js, context) == expected


@pytest.mark.parametrize('js, context, expected', [
    ['if (a>3) { a = 0} else { a = 1}', {'a': 4}, {'a': 0}],
    ['if (a>3) { a = 0} else { a = 1}', {'a': 3}, {'a': 1}],
    ['if (a>3) { a = 0} else { if (a == 3) {a = 2}}', {'a': 3}, {'a': 2}],
])
def test_else(js, context, expected):
    assert js2py(js, context) == expected


@pytest.mark.parametrize('js, context, expected', [
    ['a = "x"', {'a': 'b'}, {'a': 'x'}],
    ['if (a == "x") { a = "y"}', {'a': 'x'}, {'a': 'y'}],
    ['if (a == "x") { a = "y"}', {'a': 'm'}, {'a': 'm'}],
    ['if (a == "x") { a = "y"} else { a = "z"}', {'a': "b"}, {'a': "z"}],
    ['if (a == "x") { a = "y"} else { a = "z"}', {'a': "x"}, {'a': "y"}],
])
def test_string(js, context, expected):
    assert js2py(js, context) == expected
