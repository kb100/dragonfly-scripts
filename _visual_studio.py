from dragonfly import *

from cpp_language import CPlusPlusRule
from gvim import InsertModeRule, VimGrammarSwitcher, NormalModeRule, VisualModeRule, ExModeRule, VimMode
from lib.common import LetterRef


class VisualStudioGlobalRule(MappingRule):
    mapping = {
        'foo': Text('foobar'),
    }
    extras = [
        IntegerRef('n', 1, 10, default=1),
        LetterRef('letter'),
    ]


class CPPInsertModeRule(InsertModeRule):
    non_transitions = InsertModeRule.non_transitions + [CPlusPlusRule(exported=False)]


context = AppContext(executable="devenv")

ex_mode_grammar = Grammar("ExMode", context=context)
normal_mode_grammar = Grammar("NormalMode", context=context)
visual_mode_grammar = Grammar('VisualMode', context=context)
insert_mode_grammar = Grammar("InsertMode", context=context)
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
