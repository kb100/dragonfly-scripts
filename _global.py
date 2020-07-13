from dragonfly import *

from lib.common import SpellLetterSequenceRule
from lib.format import FormatRule
from lib.sound import play, SND_DING, SND_DEACTIVATE


def reload_natlink():
    import natlink
    natlink.setMicState('off')
    natlink.setMicState('on')
    play(SND_DING)


def go_to_sleep():
    import natlink
    natlink.setMicState('sleeping')
    play(SND_DEACTIVATE)


class GlobalRule(MappingRule):
    mapping = {
        '[<text>] go to sleep': Function(go_to_sleep),
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
        'reload natlink': Function(reload_natlink),
    }
    extras = [
        IntegerRef('n', 1, 101, default=1),
        Dictation('text'),
    ]


global_grammar = Grammar('global grammar')
global_grammar.add_rule(GlobalRule())
global_grammar.add_rule(FormatRule())
global_grammar.add_rule(SpellLetterSequenceRule())
global_grammar.load()


def unload():
    global global_grammar
    if global_grammar: global_grammar.unload()
    global_grammar = None
