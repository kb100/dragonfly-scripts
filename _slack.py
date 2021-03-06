from dragonfly import MappingRule, Key, Grammar, Text, ShortIntegerRef, Dictation, AppContext

from lib.common import LetterSequenceRef, release

rules = MappingRule(
    name="slack",
    mapping={
        "(escape|kay)": Key('escape'),
        "<letter_sequence>": Key('%(letter_sequence)s'),
        "say <text>": release + Text('%(text)s'),
        "slap": Key("enter"),
        "new message": Key("c-n"),
        "quick switch": Key("c-k"),
        "[show] keyboard shortcuts": Key("c-slash"),
        "[direct] messages": Key("cs-k"),
        "[browse] channels": Key("cs-l"),
        "edit last [message]": Key("c-up"),  # in empty text input
        "back": Key("a-left"),
        "forward": Key("a-right"),
        "[show] threads": Key("cs-t"),
        "search": Key("c-f"),
        "dismiss dialogs": Key("escape"),
        "toggle left [pane|panel]": Key("cs-d"),
        "go left [pane|panel]": Key("cs-d:2"),
        "set [a|my] status": Key("cs-y"),
        "next": Key("tab"),
        "previous": Key("s-tab"),
        "next section": Key("f6"),
        "previous section": Key("s-f6"),
        "[<n>] increase text size": Key("c-plus:%(n)d"),
        "[<n>] decrease text size": Key("c-minus:%(n)d"),
        "[<n>] scroll up": Key("pageup:%(n)d"),
        "[<n>] scroll down": Key("pagedown:%(n)d"),
        "[<n>] previous day": Key("s-pageup:%(n)d"),
        "[<n>] next day": Key("s-pagedown:%(n)d"),
        "toggle right (pane|panel)": Key("c-."),
        "channel info": Key("cs-i"),
        "[show] (mentions|reactions)": Key("cs-m"),
        "(people|directory)": Key("cs-e"),
        "saved items": Key("cs-s"),
        "toggle full screen": Key("cs-f"),
        "unread messages": Key("c-j"),
        "select [text] [to] beginning of [current] line": Key("s-up"),
        "select [text] [to] end of [current] line": Key("s-down"),
        "new line": Key("s-enter"),
        "react to last [message]": Key("cs-backslash"),
        "auto complete username": Key("at"),
        "auto complete channel": Key("hash"),
        "auto complete emoji": Key("colon"),
        "bold [text|that]": Key("c-b"),
        "(italic|italicize) [text|that]": Key("c-i"),
        "(strike|strikethrough) [text|that]": Key("cs-x"),
        "format [text|that] as code": Key("cs-c"),
        "format [selection] [as] bullet list": Key("cs-8"),
        "format [selection] [as] numbered list": Key("cs-7"),
        "format [selection] [as] quote": Key("cs-9"),
        "format selection as code": Key("cas-c"),
        "Mark [all] messages in [current] channel as read": Key("escape"),
        "Mark all messages as read": Key("s-escape"),
        "Mark unread": Key("u"),
        "previous (channel|message|DM)": Key("a-up"),
        "next (channel|message|DM)": Key("a-down"),
        "previous unread (channel|message|DM)": Key("as-up"),
        "next unread [channel|message|DM]": Key("as-down"),
        "add [a] file": Key("c-u"),
        "create [a] snippet": Key("cs-enter"),
        "view [all] downloads": Key("cs-j"),
        "edit [message]": Key("e"),
        "delete [message]": Key("delete"),
        "(add reaction|react)": Key("r"),
        "open thread": Key("t"),
        "toggle pin": Key("p"),
        "share [message]": Key("s"),
        "toggle (star|favorite)": Key(""),
        "Mark as unread from (here|this message)": Key("u"),
        "remind me about this [message]": Key("m"),

    },
    extras=[
        LetterSequenceRef('letter_sequence'),
        Dictation("text"),
        ShortIntegerRef('n', 1, 101)
    ],
    defaults={
        "n": 1
    }
)
context = AppContext(executable="slack")
slack_grammar = Grammar("slack", context=context)
slack_grammar.add_rule(rules)
slack_grammar.load()

EXPORT_GRAMMARS = [slack_grammar]


def unload():
    global slack_grammar
    if slack_grammar: slack_grammar.unload()
    slack_grammar = None
