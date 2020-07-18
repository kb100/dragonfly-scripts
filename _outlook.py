from dragonfly import *

from lib.common import LetterSequenceRef, release

rules = MappingRule(
    name="outlook",
    mapping={
        "(escape|kay)": Key('escape'),
        "<letter_sequence>": Key('%(letter_sequence)s'),
        "say <text>": release + Text('%(text)s'),
        "slap": Key("enter"),
        "new (email|message)": Key("cs-m"),
        "open [email|message]": Key("c-o"),
        "reply [email|message]": Key("c-r"),
        "reply all [email|message]": Key("cs-r"),
        "forward [email|message]": Key("c-f"),
        "print [email|message]": Key("c-p"),
        "send [email|message] now": Key("a-s"),
        "save [email|message] as draft": Key("c-s"),
        "select all": Key("c-a"),
        "[insert|start] bullet list": Key("cs-l"),
        "insert hyperlink": Key("c-k"),
        "align left": Key("c-l"),
        "align center": Key("c-e"),
        "align right": Key("c-r"),
        "spell check": Key("f7"),
        "subject": Key("a-j"),
        "send receive [all]": Key("f9"),
        "del": Key("c-d"),
        "mark [email|message] as read": Key("c-q"),
        "mark [email|message] as unread": Key("c-u"),
        "flag [email|message] [for] follow up": Key("cs-g"),
        "new task": Key("cs-k"),
        "inbox": Key("cs-l"),
        "outbox": Key("cs-o"),
        "previous [email|message]": Key("c-comma"),
        "next [email|message]": Key("c-period"),
        "previous appointment": Key("cs-comma"),
        "next appointment": Key("cs-period"),
        "(search|find)": Key("c-e"),
        "(new|create) appointment": Key("cs-a"),
        "(new|create) meeting request": Key("cs-q"),
        "go to": Key("c-g"),
        "mail view": Key("c-1"),
        "calendar view": Key("c-2"),
        "contacts view": Key("c-3"),
        "(task|tasks) view": Key("c-4"),
        "(note|notes) view": Key("c-5"),
        "(folder|folders) view": Key("c-6"),
        "(new|create) folder": Key("cs-e"),
        "next": Key("tab"),
        "previous": Key("s-tab"),
        "[<n>] increase text size": Key("c-rangle:%(n)d"),
        "[<n>] decrease text size": Key("c-langle:%(n)d"),
        "[<n>] scroll up": Key("pageup:%(n)d"),
        "[<n>] scroll down": Key("pagedown:%(n)d"),
        "bold [text|that]": Key("c-b"),
        "(italic|italicize) [text|that]": Key("c-i"),
        "(strike|strikethrough) [text|that]": Key("cs-x"),
        "underline": Key("c-u"),

    },
    extras=[
        LetterSequenceRef('letter_sequence'),
        Dictation("text"),
        ShortIntegerRef('n', 1, 101, default=1)
    ],
)
context = AppContext(executable="outlook")
outlook_grammar = Grammar("outlook", context=context)
outlook_grammar.add_rule(rules)
outlook_grammar.load()

EXPORT_GRAMMARS = [outlook_grammar]


def unload():
    global outlook_grammar
    if outlook_grammar: outlook_grammar.unload()
    outlook_grammar = None
