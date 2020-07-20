from dragonfly import *

rules = MappingRule(
    name="logiCapture",
    mapping={
        '(start|stop|toggle) recording': Key('a-r'),
        '(pause|unpause) recording': Key('a-p'),
    },
)
context = None  # AppContext(executable="logiCapture")
logi_capture_grammar = Grammar("logiCapture", context=context)
logi_capture_grammar.add_rule(rules)
logi_capture_grammar.load()

EXPORT_GRAMMARS = [logi_capture_grammar]


def unload():
    global logi_capture_grammar
    if logi_capture_grammar: logi_capture_grammar.unload()
    logi_capture_grammar = None
