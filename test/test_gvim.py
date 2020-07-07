import pytest
from dragonfly import *
from dragonfly.test import ElementTester, RecognitionFailure

from _gvim import GrammarSwitcher, FindMotionRef, mark, jumpMark, goToLine, pyCharmAction, RuleAlternative, \
    RepeatActionRule, PycharmGlobalRule, NormalModeKeystrokeRule
from test.utils import assert_same_typed_keys


@pytest.fixture(scope='session')
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


@pytest.fixture()
def pycharm_global_rule_tester(engine):
    element = RuleRef(PycharmGlobalRule())
    tester = ElementTester(element, engine)
    yield tester


def test_global_reformat(pycharm_global_rule_tester, typed_keys):
    actual = pycharm_global_rule_tester.recognize('reformat')
    expected = Key('ca-l')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_global_menu_select_default(pycharm_global_rule_tester, typed_keys):
    actual = pycharm_global_rule_tester.recognize('cell')
    expected = Key('enter')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_global_menu_select_one(pycharm_global_rule_tester, typed_keys):
    actual = pycharm_global_rule_tester.recognize('cell one')
    expected = Key('enter')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_global_menu_select_two(pycharm_global_rule_tester, typed_keys):
    actual = pycharm_global_rule_tester.recognize('cell two')
    expected = Key('down,enter')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_global_open_menu(pycharm_global_rule_tester, typed_keys):
    actual = pycharm_global_rule_tester.recognize('menu alpha')
    expected = Key('a-a')
    assert_same_typed_keys(typed_keys, actual, expected)


@pytest.fixture()
def normal_mode_keystroke_tester(engine):
    element = RuleRef(NormalModeKeystrokeRule())
    tester = ElementTester(element, engine)
    yield tester


def test_normal_mode_kay(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('kay')
    expected = Key('escape')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_optional_count_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('down')
    expected = Key('1,j')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_optional_count_motion_with_count(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('ten down')
    expected = Key('1,0,j')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_no_count_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('hat')
    expected = Key('caret')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_mandatory_count_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('fifty column')
    expected = Key('5,0,bar')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_find_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('find alpha')
    expected = Key('1,f,a')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_find_motion_with_count(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('ten find alpha')
    expected = Key('1,0,f,a')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_optional_count_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('lower case whiskey')
    expected = Key('1,g,u,w')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_optional_count_motion_with_count(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('two lower case whiskey')
    expected = Key('2,g,u,w')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_no_count_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('lower case match')
    expected = Key('g,u,percent')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_text_object_selection(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('lower case inner quote')
    expected = Key('1,g,u,i,squote')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_text_object_selection_with_count(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('two lower case inner quote')
    expected = Key('2,g,u,i,squote')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_mandatory_count_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('two lower case column')
    expected = Key('2,g,u,bar')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_find_motion(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('lower case find alpha')
    expected = Key('1,g,u,f,a')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_lower_case_find_motion_with_count(normal_mode_keystroke_tester, typed_keys):
    actual = normal_mode_keystroke_tester.recognize('two lower case find alpha')
    expected = Key('2,g,u,f,a')
    assert_same_typed_keys(typed_keys, actual, expected)
