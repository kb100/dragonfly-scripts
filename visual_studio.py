from dragonfly import *

from cpp_language import CPlusPlusRule
from gvim import VimMode, get_commands, get_transitions, make_vim_grammars
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


commands = get_commands()
commands[VimMode.INSERT].append(CPlusPlusRule(exported=False))
transitions = get_transitions()
context = AppContext(executable="devenv")
grammars, grammar_switcher = make_vim_grammars(commands, transitions, context, prefix='VS')

visual_studio_grammar = Grammar('VStudio global', context=context)
visual_studio_grammar.add_rule(VisualStudioGlobalRule())

EXPORT_GRAMMARS = list(grammars.values()) + [visual_studio_grammar]
grammars = None
for grammar in EXPORT_GRAMMARS:
    grammar.load()
grammar_switcher.switch_to_mode(VimMode.NORMAL)


def unload():
    global EXPORT_GRAMMARS
    if EXPORT_GRAMMARS is not None:
        for grammar in EXPORT_GRAMMARS:
            grammar.unload()
        EXPORT_GRAMMARS = None
