from dragonfly import *
from dragonfly.test import ElementTester, RecognitionFailure

from lib.elements import Exclusion, PhrasesExclusion


def test_exclusion(engine):
    choice = Choice('choice', choices={'a': 1, 'b': 2})
    repetition = Repetition(choice, min=2, max=3)
    to_exclude = Literal('a a')
    exclusion = Exclusion(element=repetition, exclusion=to_exclude)

    tester = ElementTester(exclusion, engine)
    assert tester.recognize('a a') is RecognitionFailure
    assert tester.recognize('c') is RecognitionFailure
    assert tester.recognize('a b') == [1, 2]
    assert tester.recognize('b a') == [2, 1]
    assert tester.recognize('b b') == [2, 2]


def test_exclusion_by_function(engine):
    choice = Choice('choice', choices={'a': 1, 'b': 2})
    repetition = Repetition(choice, min=2, max=3)
    exclude_if = lambda words: 'a a' in ' '.join(words)
    exclusion = Exclusion(element=repetition, exclude_if_func=exclude_if)

    tester = ElementTester(exclusion, engine)
    assert tester.recognize('a a') is RecognitionFailure
    assert tester.recognize('c') is RecognitionFailure
    assert tester.recognize('a b') == [1, 2]
    assert tester.recognize('b a') == [2, 1]
    assert tester.recognize('b b') == [2, 2]


def test_phrases_exclusion(engine):
    choice = Choice('choice', choices={'a': 1, 'b': 2})
    repetition = Repetition(choice, min=2, max=3)
    phrases = ['a a', 'b b']
    exclusion = PhrasesExclusion(element=repetition, phrases_to_exclude=phrases)

    tester = ElementTester(exclusion, engine)
    assert tester.recognize('a a') is RecognitionFailure
    assert tester.recognize('c') is RecognitionFailure
    assert tester.recognize('a b') == [1, 2]
    assert tester.recognize('b a') == [2, 1]
    assert tester.recognize('b b') is RecognitionFailure
