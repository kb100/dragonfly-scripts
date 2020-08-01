from dragonfly import MappingRule, Key, Grammar, IntegerRef


class TaskRule(MappingRule):
    mapping = {
        "task [minus] <n>": Key("space"),
        "(menu | pop up) task [minus] <n>": Key("space/10,a-space"),
        "new task [minus] <n>": Key("s-enter"),
        "close task [minus] <n>": Key("space/10,a-space/10,c"),
        "restore task [minus] <n>": Key("space/10,a-space/10,r"),
        "(minimize | min) task [minus] <n>": Key("space/10,a-space/10,n"),
        "(maximize | max) task [minus] <n>": Key("space/10,a-space/10,x"),
    }
    extras = [IntegerRef("n", 1, 30)]

    def _process_recognition(self, value, extras):
        node = extras['_node']
        if 'minus' in node.words():
            count = extras['n']
            direction = 'left'
        else:
            count = extras['n'] - 1
            direction = 'right'
        action = Key("w-b/10, s-tab/10, " + direction + ":%d/10" % count) + value
        action.execute()


class IconRule(MappingRule):
    mapping = {
        "[open] icon <n>": Key("enter"),
        "(menu | pop up) icon <n>": Key("apps"),
    }
    extras = [IntegerRef("n", 1, 12)]

    def _process_recognition(self, value, extras):
        count = extras["n"] - 1
        action = Key("w-b/10, right:%d/10" % count) + value
        action.execute()


taskbar_grammar = Grammar("taskbar")
taskbar_grammar.add_rule(TaskRule())
taskbar_grammar.add_rule(IconRule())
taskbar_grammar.load()


def unload():
    global taskbar_grammar
    if taskbar_grammar:
        taskbar_grammar.unload()
    taskbar_grammar = None
