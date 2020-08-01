from dragonfly import MappingRule, Key, Grammar


class NomachineRule(MappingRule):
    mapping = {
        'toggle fullscreen': Key('ca-f'),
        '[toggle] grab keyboard [input]': Key('ca-k'),
        'no machine (menu|settings)': Key('ca-0'),
    }


nomachine_grammar = Grammar('nomachine')
nomachine_grammar.add_rule(NomachineRule())
nomachine_grammar.load()


def unload():
    global nomachine_grammar
    if nomachine_grammar: nomachine_grammar.unload()
    nomachine_grammar = None
