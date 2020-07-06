import pytest
from dragonfly import *
from dragonfly.test import ElementTester, RecognitionFailure

from _gvim import unload, GrammarSwitcher, FindMotionRef, mark, jumpMark, goToLine, pyCharmAction, RuleAlternative, \
    RepeatActionRule

unload()

from test.utils import assert_same_typed_keys, typed_keys

typed_keys  # todo how to tell pycharm this is not unused?


@pytest.fixture()
def engine():
    e = get_engine()
    e.connect()
    try:
        yield e
    finally:
        e.disconnect()


def test_grammar_switcher(engine):
    grammar_a = Grammar('a', engine=engine)
    grammar_b = Grammar('b', engine=engine)
    grammars = [grammar_a, grammar_b]
    grammar_switcher = GrammarSwitcher(grammars)
    grammar_switcher.switch_to(grammar_a)
    assert grammar_a.enabled is True
    assert grammar_b.enabled is False
    grammar_switcher.switch_to(grammar_b)
    assert grammar_a.enabled is False
    assert grammar_b.enabled is True


def test_mark(typed_keys):
    actual = mark('a')
    expected = Key('m,a')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_jump_to_mark(typed_keys):
    actual = jumpMark('a')
    expected = Key('backtick,a')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_go_to_line(typed_keys):
    actual = goToLine('n').bind({'n': 100})
    expected = Text(':100\n')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_pycharm_action(typed_keys):
    actual = pyCharmAction('reformat')
    expected = Key('cs-a,r,e,f,o,r,m,a,t,enter')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_rule_alternative(engine):
    v1 = object()
    v2 = object()

    class Rule1(MappingRule):
        mapping = {'foo': v1}

    class Rule2(MappingRule):
        mapping = {'test': v2}

    rules = [Rule1(), Rule2()]
    element = RuleAlternative(rules)
    tester = ElementTester(element, engine)
    assert tester.recognize('foo') is v1
    assert tester.recognize('test') is v2
    assert tester.recognize('blah') is RecognitionFailure


def test_repeat_action_rule(engine, typed_keys):
    class Rule1(MappingRule):
        mapping = {'foo': Key('a')}

    element = RuleRef(RepeatActionRule(RuleRef(Rule1())))
    tester = ElementTester(element, engine)
    assert_same_typed_keys(typed_keys, tester.recognize('foo'), Key('a'))
    assert_same_typed_keys(typed_keys, tester.recognize('foo two times'), Key('a,a'))
    assert tester.recognize('blah') is RecognitionFailure


def test_find_motion(engine):
    element = FindMotionRef('find')
    tester = ElementTester(element, engine)
    actual = tester.recognize('find alpha')
    expected = 'f,a'
    assert actual == expected
