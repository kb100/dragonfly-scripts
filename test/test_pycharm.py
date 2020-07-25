import pytest
from dragonfly import *
from dragonfly.test import ElementTester

from pycharm import pycharm_action, PycharmGlobalRule
from test.utils import assert_same_typed_keys


def test_pycharm_action(typed_keys):
    actual = pycharm_action('reformat')
    expected = Key('cs-a,r,e,f,o,r,m,a,t,enter')
    assert_same_typed_keys(typed_keys, actual, expected)


@pytest.fixture()
def pycharm_global_rule_tester(engine):
    element = RuleRef(PycharmGlobalRule())
    tester = ElementTester(element, engine)
    return tester


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
