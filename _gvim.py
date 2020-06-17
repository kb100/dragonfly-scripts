from dragonfly import *
from common import executeSelect, LetterRef, LetterSequenceRef, release
from lib.format import FormatRule


def mark(s):
    return Key('m,' + s)


def jumpMark(s):
    return Key('backtick,' + s)


def goToLine(s):
    return Key("colon") + Text("%(" + s + ")d\n") + Pause('10')


def pyCharmAction(s):
    return Key("cs-a/10") + Text(s) + Pause("50") + Key("enter")


class PycharmGlobalRule(MappingRule):
    name = 'pycharm global'
    mapping = {
        'save all': Key('c-s'),
        "go to definition": Key("c-b"),
        'peek definition': Key('cs-i'),
        '(show|peek) docs': Key('c-q'),
        '(show params|param info)': Key('c-p'),
        'show type': Key('cs-p'),
        "reformat": Key('ca-l'),
        "reformat line": Key('escape,V,ca-l,escape'),
        'comment': Key('c-slash'),
        'suggest': Key('a-enter'),
        '(cell|select) [<n>]': Function(executeSelect, offset=1),
        'show error': Key('c-f1'),
        'run program': Key('s-f10'),
        'run dot dot dot': Key('as-f10'),
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
        'close (all but this|others)': pyCharmAction('close others'),
        'git commit': Key('c-k'),
        'next diff': Key('f7'),
        'previous diff': Key('s-f7'),
        'compare next file': Key('a-right'),
        'compare previous file': Key('a-left'),
        'menu <letter>': Key('a-%(letter)s'),
    }
    extras = [
        IntegerRef('n', 1, 10),
        LetterRef('letter'),
    ]
    defaults = {'n': 1, }


class NormalModeKeystrokeRule(MappingRule):
    # exported = False

    mapping = {
        "slap": Key('enter'),
        "[<n>] up": Key("%(n)d,k"),
        "[<n>] down": Key("%(n)d,j"),
        "[<n>] left": Key("%(n)d,h"),
        "[<n>] right": Key("%(n)d,l"),
        "[<n>] page up": Key("c-b:%(n)d"),
        "[<n>] page down": Key("c-f:%(n)d"),
        "hat": Key("caret"),
        "(dollar|doll)": Key("dollar"),
        "match": Key("percent"),
        "doc home": Key("c-home"),
        "doc end": Key("c-end"),

        "lower case": Key("g,u"),
        "upper case": Key("g,U"),
        "(swap case|tilde)": Key("tilde"),

        "visual": Key("v"),
        "visual line": Key("s-v"),
        "visual block": Key("c-v"),

        "next": Key("n"),
        "previous": Key("N"),
        "[<n>] back": Key("b:%(n)d"),
        "[<n>] (whiskey|word)": Key("w:%(n)d"),
        "[<n>] end": Key("e:%(n)d"),

        "Center": Key("z,dot"),
        "format": Key("g,q"),

        "next paragraph": Key("rbrace"),
        "previous paragraph": Key("lbrace"),
        "a paragraph": Key("a,p"),
        "inner paragraph": Key("i,p"),

        "[<n>] (Dell|D) (char|character|car)": Key("x:%(n)d"),
        "[<n>] backspace": Key("backspace:%(n)d"),

        "[<n>] Pete macro": Key("at,at:%(n)d"),

        "[<n>] join": Key("J:%(n)d"),

        '[<n>] deed': Text('d%(n)dd'),
        "(Dell| D)": Key("d"),
        "[<n>] (Dell| D) (whiskey|word)": Text("%(n)ddw"),
        "(Dell| D) a (whiskey | word)": Key("d,a,w"),
        "(Dell| D) inner (whiskey | word)": Key("d,i,w"),
        "(Dell| D) a paragraph": Key("d,a,p"),
        "(Dell| D) inner paragraph": Key("d,i,p"),
        "(Dell| D) a (paren|parenthesis|raip|laip)": Key("d,a,rparen"),
        "(Dell| D) inner (paren|parenthesis|raip|laip)": Key("d,i,rparen"),
        "(Dell| D) a (bracket|rack|lack)": Key("d,a,rbracket"),
        "(Dell| D) inner (bracket|rack|lack)": Key("d,i,rbracket"),
        "(Dell| D) a (bracket|race|lace)": Key("d,a,rbrace"),
        "(Dell| D) inner (bracket|race|lace)": Key("d,i,rbrace"),

        "[<n>] (increment|increase)": Key("c-a:%(n)d"),
        "[<n>] (decrement|decrease)": Key("c-x:%(n)d"),
        "shift (Dell| D.)": Key("s-d"),

        "[<n>] undo": Key("u:%(n)d"),
        "[<n>] redo": Key("c-r:%(n)d"),

        '[<n>] (find|forward) <letter>': Key('%(n)d,f,%(letter)s'),
        '[<n>] shift find <letter>': Key('%(n)d,F,%(letter)s'),
        'find [<n>] <letter>': Key('%(n)d,f,%(letter)s'),
        'shift find [<n>] <letter>': Key('%(n)d,F,%(letter)s'),

        '[<n>] before <letter>': Key('%(n)d,t,%(letter)s'),
        '[<n>] shift before <letter>': Key('%(n)d,T,%(letter)s'),
        'before [<n>] <letter>': Key('%(n)d,t,%(letter)s'),
        'shift before [<n>] <letter>': Key('%(n)d,T,%(letter)s'),

        '[<n>] again': Text('%(n)d;'),
        '[<n>] shift again': Text('%(n)d,'),
        '[<n>] until <letter>': Key('%(n)d,t,%(letter)s'),
        '[<n>] shift until <letter>': Key('%(n)d,T,%(letter)s'),
        'until [<n>] <letter>': Key('%(n)d,t,%(letter)s'),
        'shift until [<n>] <letter>': Key('%(n)d,T,%(letter)s'),

        "[<letter>] (yank | copy)": Key("dquote,%(letter)s,y"),
        "[<letter>] (yank | copy) a paragraph": Key("dquote,%(letter)s,y,a,p"),
        "[<letter>] (yank | copy) inner paragraph": Key("dquote,%(letter)s,y,i,p"),
        "[<letter>] (yank | copy) a (paren|parenthesis|raip|laip)": Key("dquote,%(letter)s,y,a,rparen"),
        "[<letter>] (yank | copy) inner (paren|parenthesis|raip|laip)": Key("dquote,%(letter)s,y,i,rparen"),
        '[<n>] duplicate line': Text('Y%(n)dp'),
        "[<letter>] (yank | copy) line": Key("dquote,%(letter)s,y,y"),
        "[<letter>] (yank | copy) <n> lines": Key("dquote,%(letter)s,%(n)d,Y"),

        "[<letter>] paste": Key("dquote,%(letter)s,p"),
        "[<letter>] (shift|big) paste": Key("dquote,%(letter)s,P"),

        "replace": Key("r"),
        "shift replace": Key("R"),

        "(shift left|unindent)": Key("langle,langle"),
        "(shift right|indent)": Key("rangle,rangle"),

        'Mark <letter>': Key('m,%(letter)s'),
        'jump <letter>': Key('backtick,%(letter)s'),
        'jump old': Key('c-o'),
        'jump new': Key('c-i'),

        '<ln> thru <lm> comment': mark('z') + goToLine('lm') + mark('y') +
                                  goToLine('ln') + Text('V') + jumpMark('y') +
                                  Key('c-slash') + Key('escape') + jumpMark('z'),
        '<ln> thru <lm> (copy|yank)': mark('z') + goToLine('lm') + mark('y') +
                                      goToLine('ln') + Text('V') + jumpMark('y') +
                                      Key('y') + jumpMark('z'),

        # Pete is shorthand for repeat
        "[<n>] Pete": Key("dot:%(n)d"),

        "reverse inside singles": Text("/)?'.\\{-}'\n") + Pause('30') + Key('l'),
        "reverse inside doubles": Text('?".\\{-}"\n') + Pause('30') + Key('l'),
        "inside singles": Text("/'.\\{-}'\n") + Pause('30') + Key('l'),
        "inside doubles": Text('/".\\{-}"\n') + Pause('30') + Key('l'),
        "inside parens": Text("/(\n") + Pause('30') + Key('l'),
        "inside brackets": Text("/\\[\n") + Pause('30') + Key('l'),
        "inside braces": Text("/{\n") + Pause('30') + Key('l'),
        "inside angles": Text("/<\n") + Pause('30') + Key('l'),
        "transpose": Key("x, p"),

        '(after|outside) parens': Text('/)\nl'),
        '(after|outside) brackets': Text('/]\nl'),
        '(after|outside) braces': Text('/}\nl'),
        '(after|outside) singles': Text('/\'\nl'),
        '(after|outside) doubles': Text('/"\nl'),
        '(after|outside) angles': Text('/>\nl'),
        'after dot': Text('/\\.\nl'),
        'after comma': Text('/,\nl'),

        "kay": Key("escape"),
    }
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 101),
        ShortIntegerRef("ln", 1, 10000),
        ShortIntegerRef("lm", 1, 10000),
        LetterRef('letter'),
    ]
    defaults = {"n": 1, "ln": 1, "lm": 1, "letter": "dquote"}


normal_mode_sequence = Repetition(RuleRef(rule=NormalModeKeystrokeRule()),
                                  min=1, max=16, name="normal_mode_sequence")


class NormalModeRepeatRule(CompoundRule):
    spec = "<normal_mode_sequence> [[[and] repeat [that]] <n> times]"
    extras = [normal_mode_sequence, IntegerRef("n", 1, 100), ]
    defaults = {"n": 1, }

    def _process_recognition(self, node, extras):
        normal_mode_sequence = extras["normal_mode_sequence"]
        count = extras["n"]
        for i in range(count):
            for action in normal_mode_sequence:
                action.execute()
        release.execute()


gvim_window_rule = MappingRule(
    name="gvim_window",
    mapping={
        "window left": Key("c-w,h"),
        "window right": Key("c-w,l"),
        "window up": Key("c-w,k"),
        "window down": Key("c-w,j"),

        "window split": Key("c-w,s"),
        "window vertical split": Key("c-w,v"),
    },
    extras=[]
)

gvim_tabulator_rule = MappingRule(
    name="gvim_tabulators",
    mapping={
        "tap (next|right)": Key("g,t"),
        "tap (previous|left)": Key("g,T"),
    },
    extras=[]
)

gvim_general_rule = MappingRule(
    name="gvim_general",
    mapping={"cancel": Key("escape,u"), },
    extras=[]
)

gvim_navigation_rule = MappingRule(
    name="gvim_navigation",
    mapping={
        "go first line": Key("g,g"),
        "go last line": Key("G"),
        "go old": Key("c-o"),

        "cursor top": Key("s-h"),
        "cursor middle": Key("s-m"),
        "cursor (low | bottom)": Key("s-l"),

        "go <line>": Key("colon") + Text("%(line)d\n"),

        "search <text>": Key("slash") + Text("%(text)s\n"),
        "search this": Key("asterisk"),
        "shift search <text>": Key("question") + Text("%(text)s\n"),

    },
    extras=[
        Dictation("text"),
        IntegerRef("n", 1, 50),
        ShortIntegerRef("line", 1, 10000)
    ]
)


class ExModeEnabler(CompoundRule):
    spec = "execute"

    def _process_recognition(self, node, extras):
        exModeBootstrap.disable()
        NormalModeGrammar.disable()
        ExModeGrammar.enable()
        Key("colon").execute()


class ExModeDisabler(CompoundRule):
    spec = "<command>"
    extras = [Choice("command", {
        "kay": "okay",
        "cancel": "cancel",
    })]

    def _process_recognition(self, node, extras):
        ExModeGrammar.disable()
        exModeBootstrap.enable()
        NormalModeGrammar.enable()
        if extras["command"] == "cancel":
            Key("escape").execute()
        else:
            Key("enter").execute()


class ExModeCommands(MappingRule):
    mapping = {
        "read": Text("r "),
        "(write|save) file": Text("w "),
        "quit": Text("q "),
        "write and quit": Text("wq "),
        "edit": Text("e "),
        "tab edit": Text("tabe "),

        "set number": Text("set number "),
        "set relative number": Text("set relativenumber "),
        "set ignore case": Text("set ignorecase "),
        "set no ignore case": Text("set noignorecase "),
        "set file format UNIX": Text("set fileformat=unix "),
        "set file format DOS": Text("set fileformat=dos "),
        "set file type Python": Text("set filetype=python"),
        "set file type tex": Text("set filetype=tex"),

        "P. W. D.": Text("pwd "),

        "help": Text("help"),
        "substitute": Text("s/"),
        "up": Key("up"),
        "down": Key("down"),
        "[<n>] left": Key("left:%(n)d"),
        "[<n>] right": Key("right:%(n)d"),
    }
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 50),
    ]
    defaults = {"n": 1, }


class InsertModeEnabler(CompoundRule):
    spec = "<command>"
    extras = [Choice("command", {
        "insert": "i",
        "(shift|big) insert": "I",

        "change": "c",
        "change (word|whiskey)": "c,w",
        "change inner (word|whiskey)": "c,i,w",
        "change (echo|end)": "c,e",
        "change a paragraph": "c,a,p",
        "change inner paragraph": "c,i,p",
        "change a double quote": 'c,a,dquote',
        "change inner double quote": "c,i,dquote",
        "change a quote": 'c,a,quote',
        "change inner quote": "c,i,quote",
        "change a (paren|parenthesis|raip|laip)": "c,a,rparen",
        "change inner (paren|parenthesis|raip|laip)": "c,i,rparen",
        "shift change": "C",

        "(sub|change) line": "S",

        "(after | append)": "a",
        "(shift|big) (after | append)": "A",

        "open": "o",
        "(shift|big) open": "O",
    })]

    def _process_recognition(self, node, extras):
        InsertModeBootstrap.disable()
        NormalModeGrammar.disable()
        InsertModeGrammar.enable()
        for string in extras["command"].split(','):
            key = Key(string)
            key.execute()


class InsertModeDisabler(CompoundRule):
    spec = "<command>"
    extras = [Choice("command", {
        "kay": "okay",
        "cancel": "cancel",
    })]

    def _process_recognition(self, node, extras):
        InsertModeGrammar.disable()
        InsertModeBootstrap.enable()
        NormalModeGrammar.enable()
        Key("escape").execute()
        if extras["command"] == "cancel":
            Key("u").execute()


# handles InsertMode control structures
class InsertModeCommands(MappingRule):
    mapping = {
        "<text>": Text("%(text)s"),
        "say <text>": release + Text('%(text)s'),
        "spell <letter_sequence>": Key('%(letter_sequence)s'),
        # "spell <letter_sequence>": Function(executeLetterSequence),
        "[<n>] (scratch|Dell)": Key("c-w:%(n)d"),
        "[<n>] slap": Key("enter:%(n)d"),
        "[<n>] tab": Key("tab:%(n)d"),
        "[<n>] backspace": Key("backspace:%(n)d"),
        "(scratch|Dell) line": Key("c-u"),
        "[<n>] left": Key("left:%(n)d"),
        "[<n>] right": Key("right:%(n)d"),

        "assign": Key("space,equal,space"),
        "plus": Key("space,plus,space"),
        "minus": Key("space,minus,space"),
        "times": Key("space,asterisk,space"),
        "equals": Key("space,equal,equal,space"),
        "not equals": Key("space,exclamation,equal,space"),
        "triple quote": Key("dquote,dquote,dquote"),
        'parens': Key('lparen,rparen,escape,i'),
        'brackets': Key('lbracket,rbracket,escape,i'),
        'braces': Key('lbrace,rbrace,escape,i'),
        'angles': Key('langle,rangle,escape,i'),
        'quotes': Key('squote,squote,escape,i'),
        'double quotes': Key('dquote,dquote,escape,i'),

        '(after|outside) parens': Key('escape/10') + Text('/)\na'),
        '(after|outside) brackets': Key('escape/10') + Text('/]\na'),
        '(after|outside) braces': Key('escape/10') + Text('/}\na'),
        '(after|outside) singles': Key('escape/10') + Text('/\'\na'),
        '(after|outside) doubles': Key('escape/10') + Text('/"\na'),
        '(after|outside) angles': Key('escape/10') + Text('/>\na'),
        'after dot': Key('escape/10') + Text('/\\.\na'),
        'after colon': Key('escape/10') + Text('/:\na'),
        'after equal': Key('escape/10') + Text('/=\na'),
        'after comma': Key('escape/10') + Text('/,\na'),
        'after (doll|dollar)': Key('escape/10,A'),
        # snippets for snipmate

        "comp list": Text("compl\t"),
        "comp list if": Text("compli\t"),
        "comp gen": Text("compg\t"),
        "comp gen if": Text("compgi\t"),
        "comp set": Text("comps\t"),
        "comp set if": Text("compsi\t"),
        "comp dick": Text("compd\t"),
        "comp dick if": Text("compdi\t"),
        "new for": Text("iter\t"),
        "new for enum": Text("itere\t"),
        "if name main": Text("main\t"),
        "prop get": Text("prop\t"),
        "prop set": Text("props\t"),
        "prop dell": Text("propsd\t"),
        "call super": Text("super\t"),
        "new function": Text("defn\t"),
        "annotated function": Text("defna\t"),
        "new while": Text("whilelpa\t"),
        "new attr class": Text("attrclass\t"),
        # "try except": Text("tryex\t"),

        "new fixture": Key("f,i,x,tab"),
        "new method": Key("d,e,f,s,tab"),
        "new class": Key("c,l,tab"),
        # "new function": Key("d,e,f,tab"),
        # "new while loop": Key("w,h,tab"),
        # "new for loop": Key("f,o,r,tab"),
    }
    extras = [
        LetterSequenceRef('letter_sequence'),
        Dictation("text"),
        IntegerRef("n", 1, 50),
    ]
    defaults = {"n": 1, }

gvim_exec_context = AppContext(executable="gvim")
pycharm_exec_context = AppContext(executable="pycharm")
# set the window title to vim in the putty session for the following context to
# work.
vim_putty_context = AppContext(title="vim")
gvim_context = (gvim_exec_context | vim_putty_context | pycharm_exec_context)

# set up the grammar for vim's ex mode
exModeBootstrap = Grammar("ExMode bootstrap", context=gvim_context)
exModeBootstrap.add_rule(ExModeEnabler())
exModeBootstrap.load()
ExModeGrammar = Grammar("ExMode grammar", context=gvim_context)
ExModeGrammar.add_rule(ExModeCommands())
ExModeGrammar.add_rule(ExModeDisabler())
ExModeGrammar.load()
ExModeGrammar.disable()

# set up the grammar for vim's insert mode
InsertModeBootstrap = Grammar("InsertMode bootstrap", context=gvim_context)
InsertModeBootstrap.add_rule(InsertModeEnabler())
InsertModeBootstrap.load()
InsertModeGrammar = Grammar("InsertMode grammar", context=gvim_context)
InsertModeGrammar.add_rule(InsertModeCommands())
InsertModeGrammar.add_rule(InsertModeDisabler())
InsertModeGrammar.add_rule(FormatRule())
InsertModeGrammar.load()
InsertModeGrammar.disable()

NormalModeGrammar = Grammar("NormalMode grammar", context=gvim_context)
NormalModeGrammar.add_rule(NormalModeRepeatRule())
NormalModeGrammar.add_rule(gvim_window_rule)
NormalModeGrammar.add_rule(gvim_tabulator_rule)
NormalModeGrammar.add_rule(gvim_general_rule)
NormalModeGrammar.add_rule(gvim_navigation_rule)
NormalModeGrammar.load()

pycharm_global_grammar = Grammar('pycharm global grammar', context=gvim_context)
pycharm_global_grammar.add_rule(PycharmGlobalRule())
pycharm_global_grammar.load()


# Unload function which will be called at unload time.
def unload():
    global NormalModeGrammar
    if NormalModeGrammar: NormalModeGrammar.unload()
    NormalModeGrammar = None

    global ExModeGrammar
    if ExModeGrammar: ExModeGrammar.unload()
    ExModeGrammar = None

    global InsertModeGrammar
    if InsertModeGrammar: InsertModeGrammar.unload()
    InsertModeGrammar = None

    global pycharm_global_grammar
    if pycharm_global_grammar: pycharm_global_grammar.unload()
    pycharm_global_grammar = None
