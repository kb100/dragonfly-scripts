from dragonfly import *

from cpp_language import CPlusPlusRule
from gvim import InsertModeRule, VimGrammarSwitcher, NormalModeRule, VisualModeRule, ExModeRule, VimMode
from lib.common import LetterRef, execute_select


def toggle_vim():
    return Key('cs-f12/10')


def focus_search():
    return Key('c-q/10')


def visual_studio_action(s):
    return toggle_vim() + focus_search() + Text(s) + Pause('10') + Key('enter/10') + toggle_vim()


class VisualStudioGlobalRule(MappingRule):
    mapping = {
        'save all': Key('cs-s'),
        "go to definition": Key("f12"),
        '(show|find) [all] (usages|references)': Key("a-f7"),
        'peek definition': Key('a-f12'),
        '(show params|param info)': Key('cs-space'),
        '(show type|quick info)': visual_studio_action('Quick Info'),
        'show (type|class) (view|hierarchy)': Key('cs-c'),
        'show call hierarchy': Key('ca-k'),
        '(format|reformat) [document]': visual_studio_action('Reformat Document'),
        '(format|reformat) selection': visual_studio_action('Reformat Selection'),
        '[toggle] [line] comment': visual_studio_action('Toggle Line Comment'),
        '[toggle] block comment': visual_studio_action('Toggle Block Comment'),
        'suggest': Key('c-dot'),
        '(cell|select) [<n>]': Function(execute_select, offset=1),
        'show error': visual_studio_action('Quick Info'),
        'rename': visual_studio_action('Rename'),
        'extract variable': Key('c-dot'),
        'close tab': Key('c-f4'),
        'git commit': Key('c-0,g'),
        'next diff': Key('c-f8'),
        'previous diff': Key('cs-f8'),

    }
    extras = [
        IntegerRef('n', 1, 10, default=1),
        LetterRef('letter'),
    ]


class CPPInsertModeRule(InsertModeRule):
    non_transitions = InsertModeRule.non_transitions + [CPlusPlusRule(exported=False)]


context = AppContext(executable="devenv")

ex_mode_grammar = Grammar("VSExMode", context=context)
normal_mode_grammar = Grammar("VSNormalMode", context=context)
visual_mode_grammar = Grammar('VSVisualMode', context=context)
insert_mode_grammar = Grammar("VSInsertMode", context=context)
visual_studio_grammar = Grammar('VisualStudio', context=context)

grammar_switcher = VimGrammarSwitcher(normal_mode_grammar, insert_mode_grammar, visual_mode_grammar, ex_mode_grammar)

normal_mode_grammar.add_rule(NormalModeRule(grammar_switcher))
visual_mode_grammar.add_rule(VisualModeRule(grammar_switcher))
insert_mode_grammar.add_rule(CPPInsertModeRule(grammar_switcher))
ex_mode_grammar.add_rule(ExModeRule(grammar_switcher))

visual_studio_grammar.add_rule(VisualStudioGlobalRule())

EXPORT_GRAMMARS = [visual_studio_grammar, normal_mode_grammar, visual_mode_grammar, insert_mode_grammar,
                   ex_mode_grammar]
for grammar in EXPORT_GRAMMARS:
    grammar.load()
grammar_switcher.switch_to_mode(VimMode.NORMAL)


def unload():
    global visual_studio_grammar
    if visual_studio_grammar: visual_studio_grammar.unload()
    visual_studio_grammar = None

    global normal_mode_grammar
    if normal_mode_grammar: normal_mode_grammar.unload()
    normal_mode_grammar = None

    global visual_mode_grammar
    if visual_mode_grammar: visual_mode_grammar.unload()
    visual_mode_grammar = None

    global insert_mode_grammar
    if insert_mode_grammar: insert_mode_grammar.unload()
    insert_mode_grammar = None

    global ex_mode_grammar
    if ex_mode_grammar: ex_mode_grammar.unload()
    ex_mode_grammar = None
