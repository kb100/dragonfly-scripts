import pytest

from lib.format import *


@pytest.mark.parametrize('words,expected', [
    (['alpha', 'bravo'], ['a', 'b']),
    (['test', 'alpha', 'bravo'], ['test', 'a', 'b']),
])
def test_replace_lowercase_keys(words, expected):
    actual = replace_lowercase_keys(words)
    assert actual == expected


@pytest.mark.parametrize('words,expected', [
    (['a'], ['a']),
    (['test'], ['test']),
    (['a', 'b', 'c', 'variable'], ['abc', 'variable']),
    (['variable', 'a', 'b', 'c'], ['variable', 'abc']),
])
def test_squash_single_letter_words(words, expected):
    actual = squash_single_letter_words_together(words)
    assert actual == expected


@pytest.mark.parametrize('dictation,expected', [
    ('some words', 'some_words'),
    ('oneword', 'oneword'),
    ('one two three', 'one_two_three'),
    ('non-negotiable', 'non_negotiable'),
    ('alpha variable', 'a_variable'),
    ('alpha bravo charlie variable', 'abc_variable'),
    ('type tango', 'type_t'),
    ('Proper Noun', 'proper_noun'),
])
def test_format_score(dictation, expected):
    actual = format_score(dictation)
    assert actual == expected


def test_format_double_score():
    actual = format_double_score('some words')
    expected = '__some_words'
    assert actual == expected


def test_format_under_func():
    actual = format_under_function('some words')
    expected = 'some_words()'
    assert actual == expected


def test_format_title():
    actual = format_title('some words')
    expected = 'SomeWords'
    assert actual == expected


def test_format_one_word():
    actual = format_one_word('some words')
    expected = 'somewords'
    assert actual == expected


def test_format_upper_one_word():
    actual = format_upper_one_word('some words')
    expected = 'SOMEWORDS'
    assert actual == expected


def test_format_upper_score():
    actual = format_upper_score('some words')
    expected = 'SOME_WORDS'
    assert actual == expected


def test_format_camel():
    actual = format_camel('some words')
    expected = 'someWords'
    assert actual == expected


def test_format_say():
    actual = format_say('some words')
    expected = 'some words'
    assert actual == expected


def test_format_prose():
    actual = format_prose('Some words, a full sentence. And another.')
    expected = 'Some words, a full sentence. And another.'
    assert actual == expected
