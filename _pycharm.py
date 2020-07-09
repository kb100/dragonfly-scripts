from dragonfly import *

from gvim import InsertModeRule, VimGrammarSwitcher, NormalModeRule, VisualModeRule, ExModeRule, VimMode
from lib.common import executeSelect, LetterRef
from python_language import PythonRule


def pyCharmAction(s):
    return Key("cs-a/10") + Text(s) + Pause("50") + Key("enter")


class PycharmGlobalRule(MappingRule):
    mapping = {
        'save all': Key('c-s'),
        "go to definition": Key("c-b"),
        '(show|find) usages': Key("a-f7"),
        'highlight usages': Key("cs-f7"),
        'peek definition': Key('cs-i'),
        '(show|peek) docs': Key('c-q'),
        '(show params|param info)': Key('c-p'),
        'show type': Key('cs-p'),
        'show type hierarchy': Key('c-h'),
        'show call hierarchy': Key('ca-h'),
        "reformat": Key('ca-l'),
        "reformat line": Key('escape,V,ca-l,escape'),
        'comment': Key('c-slash'),
        'suggest': Key('a-enter'),
        '(cell|select) [<n>]': Function(executeSelect, offset=1),
        'show error': Key('c-f1'),
        'run program': Key('s-f10'),
        'run dot dot dot': Key('as-f10'),
        'kill program': Key('c-f2'),
        'debug program': Key('s-f9'),
        'debug dot dot dot': Key('as-f9'),
        'toggle breakpoint': Key('c-f8'),
        'step out': Key('s-f8'),
        'step over': Key('f8'),
        'step into': Key('f7'),
        'resume program': Key('f9'),
        'rename': Key('s-f6'),
        'extract variable': Mimic('kay') + Mimic('insert') + Key('ca-v'),
        'new (file|dot dot dot)': Key('a-f/20,a-insert'),
        'panel <n>': Key('a-%(n)d'),
        'close tab': Key('c-f4'),
        'close (all but this|others)': pyCharmAction('close others'),
        'close left': pyCharmAction('close all to the left'),
        'close right': pyCharmAction('close all to the right'),
        'unsplit': pyCharmAction('unsplit'),
        'git commit': Key('c-k'),
        'show diff': Key('c-d'),
        'next diff': Key('f7'),
        'next section': Key('tab'),
        'previous section': Key('s-tab'),
        'previous diff': Key('s-f7'),
        'compare next file': Key('a-right'),
        'compare previous file': Key('a-left'),
        'menu <letter>': Key('a-%(letter)s'),
        'hide menu': Key('s-escape'),
        'fold': Key('c-npsub'),
        '(expand|unfold)': Key('c-npadd'),
        'open file': Key('a-n/10,f'),
    }
    extras = [
        IntegerRef('n', 1, 10, default=1),
        LetterRef('letter'),
    ]


class PythonInsertModeRule(InsertModeRule):
    non_transitions = InsertModeRule.non_transitions + [PythonRule()]


context = AppContext(executable="pycharm")

ex_mode_grammar = Grammar("ExMode", context=context)
normal_mode_grammar = Grammar("NormalMode", context=context)
visual_mode_grammar = Grammar('VisualMode', context=context)
insert_mode_grammar = Grammar("InsertMode", context=context)
pycharm_grammar = Grammar('pycharm global', context=context)

grammar_switcher = VimGrammarSwitcher(normal_mode_grammar, insert_mode_grammar, visual_mode_grammar, ex_mode_grammar)

normal_mode_grammar.add_rule(NormalModeRule(grammar_switcher))
visual_mode_grammar.add_rule(VisualModeRule(grammar_switcher))
insert_mode_grammar.add_rule(PythonInsertModeRule(grammar_switcher))
ex_mode_grammar.add_rule(ExModeRule(grammar_switcher))

pycharm_grammar.add_rule(PycharmGlobalRule())

EXPORT_GRAMMARS = [pycharm_grammar, normal_mode_grammar, visual_mode_grammar, insert_mode_grammar, ex_mode_grammar]
for grammar in EXPORT_GRAMMARS:
    grammar.load()
grammar_switcher.switch_to_mode(VimMode.NORMAL)


def unload():
    global pycharm_grammar
    if pycharm_grammar: pycharm_grammar.unload()
    pycharm_grammar = None

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
