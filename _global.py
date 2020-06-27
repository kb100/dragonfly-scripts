from dragonfly import *


def reload_natlink():
    """Reloads Natlink and custom Python modules."""
    win = Window.get_foreground()
    FocusWindow(executable="natspeak",
                title="Messages from Python Macros").execute()
    Pause("10").execute()
    Key("a-f, r").execute()
    Pause("10").execute()
    win.set_foreground()


class GlobalRule(MappingRule):
    mapping = {
        'mouse': Key('f3,f4/350,f4'),
        "touch": Mouse("left"),
        "touch two": Mouse("left:2"),
        'touch are': Mouse('right'),
        "touch mid": Mouse("middle"),
        "[<n>] scroll down": (Mouse("wheeldown") + Pause('5')) * Repeat(extra='n') * 2,
        "[<n>] scroll up": (Mouse("wheelup") + Pause('5')) * Repeat(extra='n') * 2,
        "[<n>] scroll right": (Mouse("wheelright") + Pause('5')) * Repeat(extra='n') * 2,
        "[<n>] scroll left": (Mouse("wheelleft") + Pause('5')) * Repeat(extra='n') * 2,
        "drag": Mouse("left:down"),
        "drop": Mouse("left:up"),
        "[<n>] alt tab": Key("alt:down,tab/50:%(n)d/50,alt:up"),
        "alt tab show": Key("alt:down,tab/10,s-tab"),
        # 'reload natlink': Function(reload_natlink),
        # crashes
    }
    extras = [IntegerRef('n', 1, 101)]
    defaults = {'n': 1}


global_grammar = Grammar('global grammar')
global_grammar.add_rule(GlobalRule())
global_grammar.load()


# Unload function which will be called at unload time.
def unload():
    global global_grammar
    if global_grammar: global_grammar.unload()
    global_grammar = None
