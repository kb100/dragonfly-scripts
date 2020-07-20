from dragonfly import *

from lib.common import LetterSequenceRef

rules = MappingRule(
    name="template",
    mapping={
        'spoken form': Text('typed form'),
    },
    extras=[
        LetterSequenceRef('letter_sequence'),
        Dictation("text"),
        ShortIntegerRef('n', 1, 101, default=1)
    ],
)
context = AppContext(executable="template")
template_grammar = Grammar("template", context=context)
template_grammar.add_rule(rules)
template_grammar.load()

EXPORT_GRAMMARS = [template_grammar]


def unload():
    global template_grammar
    if template_grammar: template_grammar.unload()
    template_grammar = None
