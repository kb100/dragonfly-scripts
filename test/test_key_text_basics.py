import pytest
from dragonfly import *

from test.utils import assert_same_typed_keys


def test_key_reflexive(typed_keys):
    assert_same_typed_keys(typed_keys, Key('a'), Key('a'))


def test_text_reflexive(typed_keys):
    assert_same_typed_keys(typed_keys, Text('!'), Text('!'))


def test_key_distributes_over_plus(typed_keys):
    assert_same_typed_keys(typed_keys, Key('a') + Key('b'), Key('a,b'))


def test_text_distributes_over_plus(typed_keys):
    assert_same_typed_keys(typed_keys, Text('a') + Text('b'), Text('ab'))


def test_key_and_text_are_same(typed_keys):
    assert_same_typed_keys(typed_keys, Key('colon'), Text(':'))


def test_bad_key_raises(typed_keys):
    with pytest.raises(ActionError):
        assert_same_typed_keys(typed_keys, Key('notakey'), Key('notakey'))


def test_trailing_comma_does_not_affect_key(typed_keys):
    assert_same_typed_keys(typed_keys, Key('a,'), Key('a'))


def test_key_repeat(typed_keys):
    assert_same_typed_keys(typed_keys, Key('a,a'), Key('a:2'))


def test_key_times_factor(typed_keys):
    assert_same_typed_keys(typed_keys, Key('a,a'), Key('a') * Repeat('n').factor({'n': 2}))
