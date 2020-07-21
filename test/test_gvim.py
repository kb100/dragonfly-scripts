import pytest
from dragonfly.test import ElementTester, RecognitionFailure

from gvim import *
from gvim import _make_mode_rules, _make_transition_then_repeats
from lib.actions import MarkedAction
from lib.grammar_switcher import GrammarSwitcher
from test.utils import assert_same_typed_keys


@pytest.fixture(scope='session')
def mode_rules():
    vgs = VimGrammarSwitcher()
    prefix = ''
    commands = get_commands()
    transitions = get_transitions()
    transitions_then_repeats = _make_transition_then_repeats(commands, prefix, transitions)
    return _make_mode_rules(commands, vgs, '', transitions_then_repeats)


@pytest.fixture()
def normal_mode_keystroke_tester(engine):
    element = RuleRef(NormalModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def normal_mode_rule_tester(mode_rules, rule_test_grammar):
    rule_test_grammar.add_rule(mode_rules[VimMode.NORMAL])
    return rule_test_grammar


def test_normal_mode_rule(normal_mode_rule_tester, typed_keys):
    extras = normal_mode_rule_tester.recognize_extras('up up down change word down up')
    actual = extras['repeat_command'] + extras['transition_command']
    expected = Key('1,k,1,k,1,j,1,c,w,down,up')
    assert_same_typed_keys(typed_keys, actual, expected)


@pytest.fixture()
def normal_mode_to_insert_mode_tester(engine):
    element = RuleRef(NormalModeToInsertModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def normal_mode_to_visual_mode_tester(engine):
    element = RuleRef(NormalModeToVisualModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def normal_mode_to_ex_mode_tester(engine):
    element = RuleRef(NormalModeToExModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def visual_mode_to_normal_mode_tester(engine):
    element = RuleRef(VisualModeToNormalModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def visual_mode_keystroke_tester(engine):
    element = RuleRef(VisualModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def visual_mode_to_ex_mode_tester(engine):
    element = RuleRef(VisualModeToExModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def visual_mode_rule_tester(mode_rules, rule_test_grammar):
    rule_test_grammar.add_rule(mode_rules[VimMode.VISUAL])
    return rule_test_grammar


def test_visual_mode_rule_motion_then_yank(visual_mode_rule_tester, typed_keys):
    extras = visual_mode_rule_tester.recognize_extras('inner lip yank down up')
    actual = extras['repeat_command'] + extras['transition_command']
    expected = Key('i,rparen,dquote,dquote,y,1,j,1,k')
    assert_same_typed_keys(typed_keys, actual, expected)


@pytest.fixture()
def insert_mode_to_normal_mode_tester(engine):
    element = RuleRef(InsertModeToNormalModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def insert_mode_to_normal_mode_tester(engine):
    element = RuleRef(InsertModeToNormalModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def insert_mode_commands_tester(engine):
    element = RuleRef(InsertModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def insert_mode_rule_tester(mode_rules, rule_test_grammar):
    rule_test_grammar.add_rule(mode_rules[VimMode.INSERT])
    return rule_test_grammar


def test_insert_mode_rule(insert_mode_rule_tester, typed_keys):
    extras = insert_mode_rule_tester.recognize_extras('skip kay down up')
    actual = extras['repeat_command'] + extras['transition_command']
    expected = Key('end,escape,1,j,1,k')
    assert_same_typed_keys(typed_keys, actual, expected)


@pytest.fixture()
def ex_mode_to_normal_mode_tester(engine):
    element = RuleRef(ExModeToNormalModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def ex_mode_commands_tester(engine):
    element = RuleRef(ExModeCommands())
    tester = ElementTester(element, engine)
    return tester


@pytest.fixture()
def ex_mode_rule_tester(mode_rules, rule_test_grammar):
    rule_test_grammar.add_rule(mode_rules[VimMode.EX])
    return rule_test_grammar


def test_ex_mode_rule(ex_mode_rule_tester, typed_keys):
    extras = ex_mode_rule_tester.recognize_extras('substitute alpha slash bravo slash slap down up')
    actual = extras['repeat_command'] + extras['transition_command']
    expected = Text('s/a/b/\n1j1k')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_empty_grammar_switcher_does_not_error():
    grammar_switcher = GrammarSwitcher()
    anything = None
    grammar_switcher.switch_to(anything)


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


def test_empty_vim_grammar_switcher_does_not_error():
    vgs = VimGrammarSwitcher()
    vgs.switch_to_mode(VimMode.VISUAL)


def test_vim_grammar_switcher_mark_switches_to(engine):
    @VimGrammarSwitcher.mark_switches_to_mode(VimMode.NORMAL)
    class Rule1(MappingRule):
        mapping = {'foo': Key('f')}

    tester = ElementTester(RuleRef(Rule1()), engine)
    value = tester.recognize('foo')
    assert isinstance(value, MarkedAction)
    assert value.mark is VimMode.NORMAL


def test_repeat_then_transition_rule(rule_test_grammar, typed_keys):
    class RepeatRule(MappingRule):
        mapping = {'foo': Key('f')}

    class TransitionRule(MappingRule):
        mapping = {'bar': Key('b')}

    vim_mode_switcher = VimGrammarSwitcher()
    non_transitions = [RepeatRule(exported=False)]
    transitions = [TransitionRule(exported=False)]
    rule = RepeatThenTransitionRule(vim_mode_switcher, non_transitions, transitions)

    rule_test_grammar.add_rule(rule)

    extras = rule_test_grammar.recognize_extras('foo foo')
    assert_same_typed_keys(typed_keys, extras['repeat_command'], Key('f,f'))
    assert 'transition_command' not in extras

    extras = rule_test_grammar.recognize_extras('bar')
    assert 'repeat_command' not in extras
    assert_same_typed_keys(typed_keys, extras['transition_command'], Key('b'))

    extras = rule_test_grammar.recognize_extras('foo foo bar')
    assert_same_typed_keys(typed_keys, extras['repeat_command'], Key('f,f'))
    assert_same_typed_keys(typed_keys, extras['transition_command'], Key('b'))

    with pytest.raises(Exception):
        rule_test_grammar.recognize_extras('')


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


def test_rule_alternative(engine):
    v1 = object()
    v2 = object()

    class Rule1(MappingRule):
        mapping = {'foo': v1}

    class Rule2(MappingRule):
        mapping = {'test': v2}

    rules = [Rule1(), Rule2()]
    element = RuleOrElemAlternative(rules)
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


def test_normal_mode_to_insert_mode_insert(normal_mode_to_insert_mode_tester, typed_keys):
    actual = normal_mode_to_insert_mode_tester.recognize('insert')
    expected = Key('i')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_to_visual_mode_visual_line(normal_mode_to_visual_mode_tester, typed_keys):
    actual = normal_mode_to_visual_mode_tester.recognize('visual line')
    expected = Key('V')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_normal_mode_to_ex_mode_substitute(normal_mode_to_ex_mode_tester, typed_keys):
    actual = normal_mode_to_ex_mode_tester.recognize('substitute')
    expected = Key('colon,s,slash')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_visual_mode_to_normal_mode_yank(visual_mode_to_normal_mode_tester, typed_keys):
    actual = visual_mode_to_normal_mode_tester.recognize('yank')
    expected = Key('dquote,dquote,y')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_visual_mode_keystroke_other(visual_mode_keystroke_tester, typed_keys):
    actual = visual_mode_keystroke_tester.recognize('other')
    expected = Key('o')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_visual_mode_to_ex_mode_substitute(visual_mode_to_ex_mode_tester, typed_keys):
    actual = visual_mode_to_ex_mode_tester.recognize('substitute')
    expected = Key('colon,s,slash')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_insert_mode_to_normal_mode_kay(insert_mode_to_normal_mode_tester, typed_keys):
    actual = insert_mode_to_normal_mode_tester.recognize('kay')
    expected = Key('escape')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_insert_mode_commands_skip(insert_mode_commands_tester, typed_keys):
    actual = insert_mode_commands_tester.recognize('skip')
    expected = Key('end')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_ex_mode_to_normal_mode_kay(ex_mode_to_normal_mode_tester, typed_keys):
    actual = ex_mode_to_normal_mode_tester.recognize('kay')
    expected = Key('escape')
    assert_same_typed_keys(typed_keys, actual, expected)


def test_ex_mode_commands_substitute(ex_mode_commands_tester, typed_keys):
    actual = ex_mode_commands_tester.recognize('substitute')
    expected = Key('s,slash')
    assert_same_typed_keys(typed_keys, actual, expected)
