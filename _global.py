from dragonfly import *


class MouseRule(MappingRule):
    mapping = {
        "touch": Mouse("left"),
        "touch two": Mouse("left:2"),
        'touch are': Mouse('right'),
        "touch mid": Mouse("middle"),
        "[<n>] scroll down": (Mouse("wheeldown") + Pause('5')) * Repeat(extra='n') * 2,
        "[<n>] scroll up": (Mouse("wheelup") + Pause('5')) * Repeat(extra='n') * 2,
        "[<n>] scroll right": (Mouse("wheelright") + Pause('5')) * Repeat(extra='n') * 2,
        "[<n>] scroll left": (Mouse("wheelleft") + Pause('5')) * Repeat(extra='n') * 2,

    }
    extras = [IntegerRef('n', 1, 101)]
    defaults = {'n': 1}

global_grammar = Grammar('global grammar')
global_grammar.add_rule(MouseRule())
global_grammar.load()


# Unload function which will be called at unload time.
def unload():
    global global_grammar
    if global_grammar: global_grammar.unload()
    global_grammar = None
