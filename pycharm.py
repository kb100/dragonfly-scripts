from dragonfly import *

from gvim import get_commands, get_transitions, make_vim_grammars, VimMode
from lib.common import execute_select, LetterRef
from python_language import PythonRule


def pycharm_action(s):
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
        '(cell|select) [<n>]': Function(execute_select, offset=1),
        'show error': Key('c-f1'),
        'run program': Key('s-f10'),
        'run dot dot dot': Key('as-f10'),
        'execute selection [in console]': Key('as-e'),
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
        'close (all but this|others)': pycharm_action('close others'),
        'close left': pycharm_action('close all to the left'),
        'close right': pycharm_action('close all to the right'),
        'unsplit': pycharm_action('unsplit'),
        'git commit': Key('c-k'),
        'git pull': Key('a-s/20,a-u'),
        'git push': Key('cs-k'),
        'show diff': Key('c-d'),
        'next diff': Key('f7'),
        'next section': Key('tab'),
        'previous section': Key('s-tab'),
        'previous diff': Key('s-f7'),
        'compare next file': Key('a-right'),
        'compare previous file': Key('a-left'),
        'menu <letter>': Key('a-%(letter)s'),
        'hide menu': Key('s-escape'),
        'fold all': Key('cs-npsub'),
        '(expand|unfold) all': Key('cs-npadd'),
        'fold': Key('c-npsub'),
        '(expand|unfold)': Key('c-npadd'),
        'open file': Key('a-n/10,f'),
    }
    extras = [
        IntegerRef('n', 1, 10, default=1),
        LetterRef('letter'),
    ]


commands = get_commands()
commands[VimMode.INSERT].append(PythonRule(exported=False))
transitions = get_transitions()
context = AppContext(executable="pycharm")
grammars, grammar_switcher = make_vim_grammars(commands, transitions, context, prefix='Py')

pycharm_grammar = Grammar('pycharm global', context=context)
pycharm_grammar.add_rule(PycharmGlobalRule())

EXPORT_GRAMMARS = list(grammars.values()) + [pycharm_grammar]
grammars = None
for grammar in EXPORT_GRAMMARS:
    grammar.load()
grammar_switcher.switch_to_mode(VimMode.NORMAL)


# class ActiveGrammarsReporter(RecognitionObserver):
#     def on_post_recognition(self, words, rule, node, results):
#         print '!!!!!!' + str(rule) + ' recognized: ' + ' '.join(words)
#         if rule:
#             print str(rule) + ' is enabled: ' + str(rule.enabled)
#             print str(rule) + ' is active: ' + str(rule.active)
#         print 'report grammars'
#         for grammar in [normal_mode_grammar, insert_mode_grammar]:
#             print 'Grammar: ' + grammar.name
#             print 'Enabled', grammar.enabled
#             print 'Active rules:', grammar.active_rules
#             print 'Rules:', grammar.rules
#
#
# reporter = ActiveGrammarsReporter()
# reporter.register()


def unload():
    global EXPORT_GRAMMARS
    if EXPORT_GRAMMARS is not None:
        for grammar in EXPORT_GRAMMARS:
            grammar.unload()
        EXPORT_GRAMMARS = None
