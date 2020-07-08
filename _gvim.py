from dragonfly import *

from lib.common import executeSelect, LetterRef, LetterSequenceRef, singleCharacterKeyMap, EmptyAction
from lib.format import FormatRule
from python_language import PythonRule

gvim_exec_context = AppContext(executable="gvim")
pycharm_exec_context = AppContext(executable="pycharm")
vim_putty_context = AppContext(title="vim")
gvim_context = (gvim_exec_context | vim_putty_context | pycharm_exec_context)

ex_mode_grammar = Grammar("ExMode", context=gvim_context)
normal_mode_grammar = Grammar("NormalMode", context=gvim_context)
visual_mode_grammar = Grammar('VisualMode', context=gvim_context)
insert_mode_grammar = Grammar("InsertMode", context=gvim_context)
pycharm_grammar = Grammar('pycharm global', context=gvim_context)

EXPORT_GRAMMARS = [pycharm_grammar, normal_mode_grammar, visual_mode_grammar, insert_mode_grammar, ex_mode_grammar]


class GrammarSwitcher:
    def __init__(self, grammars=None):
        self.grammars = grammars if grammars is not None else []

    def switch_to(self, grammar):
        for other in self.grammars:
            if other is grammar:
                grammar.enable()
            else:
                other.disable()

    def add_grammar(self, grammar):
        self.grammars.append(grammar)

    def switch_to_action(self, grammar):
        return Function(self.switch_to, grammar=grammar)

    def switches_to(self, grammar):
        assert [g for g in self.grammars if g is grammar]

        def class_modifier(cls):
            assert hasattr(cls, 'value')
            assert callable(cls.value)
            old_value = cls.value

            def value(this, node):
                v = old_value(this, node)
                return v + self.switch_to_action(grammar)

            cls.value = value
            return cls

        return class_modifier


grammar_switcher = GrammarSwitcher([normal_mode_grammar, visual_mode_grammar, insert_mode_grammar, ex_mode_grammar])

text_object_keys = {
    "a (word|whiskey)": "a,w",
    "inner (word|whiskey)": "i,w",
    "a (big|shift) (word|whiskey)": "a,W",
    "inner (big|shift) (word|whiskey)": "i,W",
    "a sentence": "a,s",
    "inner sentence": "i,s",
    "a paragraph": "a,p",
    "inner paragraph": "i,p",
    "a (bracket|lack|rack)": "a,rbracket",
    "inner (bracket|lack|rack)": "i,rbracket",
    "a (paren|lip|rip)": "a,rparen",
    "inner (paren|lip|rip)": "i,rparen",
    "a (angle|langle|rangle)": "a,rangle",
    "inner (angle|langle|rangle)": "i,rangle",
    "a tag": "a,t",
    "inner tag": "i,t",
    "a (brace|lace|race)": "a,rbrace",
    "inner (brace|lace|race)": "i,rbrace",
    "a (double quote|D quote|doubles)": "a,dquote",
    "inner (double quote|D quote|doubles)": "i,dquote",
    "a (quote|singles)": "a,squote",
    "inner (quote|singles)": "i,squote",
    "a (backtick|tick|grave)": "a,backtick",
    "inner (backtick|tick|grave)": "i,backtick",
}
paired_symbols_keys = {
    "(bracket|lack|rack)": "lbracket,rbracket",
    "(paren|lip|rip)": "lparen,rparen",
    "(angle|langle|rangle)": "langle,rangle",
    "(brace|lace|race)": "lbrace,rbrace",
    "(double quote|D quote|doubles)": "dquote,dquote",
    "(quote|singles)": "squote,squote",
    "(backtick|tick|grave)": "backtick,backtick",
}
paired_symbol_keys = {
    "(bracket|lack|rack)": "rbracket",
    "(paren|lip|rip)": "rparen",
    "(angle|langle|rangle)": "rangle",
    "(brace|lace|race)": "rbrace",
    "(double quote|D quote|doubles)": "dquote",
    "(quote|singles)": "squote",
    "(backtick|tick|grave)": "backtick",
}
optional_count_motion_keys = {
    'left': 'h',
    '(right|char)': 'l',
    'again': 'semicolon',
    '(reverse|shift) again': 'comma',

    'up': 'k',
    'down': 'j',

    '(word|whiskey)': 'w',
    '(big|shift) (word|whiskey)': 'W',
    'end': 'e',
    '(big|shift) end': 'E',
    'back': 'b',
    '(big|shift) back': 'B',

    '((big|shift) sentence|lip)': 'lparen',
    '(sentence|rip)': 'rparen',
    '((big|shift) paragraph|lace)': 'lbrace',
    '(paragraph|race)': 'rbrace',

    "page up": "pageup",
    "page down": "pagedown",

    "next": "n",
    "previous": "N",
}
mandatory_count_motion_keys = {
    '(bar|pipe|column)': 'bar',
    'go': 'G',
    'percent': 'percent',
}
no_count_motion_keys = {
    '(zero|first char)': '0',
    '(dollar|end of line)': 'dollar',
    'last non blank': 'g,score',
    'hat': 'caret',
    'half line': 'g,m',
    'match': 'percent',
    "doc home": "g,g",
    "doc end": "G",
}
find_motion_keys = {
    'find': 'f',
    '(big|shift) find': 'F',
    '(until|before)': 't',
    '(big|shift) (until|before)': 'T',
}


class FindMotionRef(Choice):
    def __init__(self, name, default=None):
        choices = {k + ' <letter>': f for k, f in find_motion_keys.iteritems()}
        extras = [LetterRef('letter')]
        super(FindMotionRef, self).__init__(name, choices, extras, default)

    def value(self, node):
        f = super(FindMotionRef, self).value(node)
        letter = node.get_child_by_name('letter', shallow=True).value()
        return f + ',' + letter


valid_registers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'dot', 'percent',
                   'hash', 'colon', 'dquote']
register_keys = {k: v for k, v in singleCharacterKeyMap.iteritems() if v.lower() in valid_registers}


def mark(s):
    return Key('m,' + s)


def jumpMark(s):
    return Key('backtick,' + s)


def goToLine(s):
    return Key("colon") + Text("%(" + s + ")d\n") + Pause('10')


def pyCharmAction(s):
    return Key("cs-a/10") + Text(s) + Pause("50") + Key("enter")


class RuleAlternative(Alternative):
    def __init__(self, rules, name=None, default=None):
        super(RuleAlternative, self).__init__([RuleRef(rule) for rule in rules], name, default)


class RepeatActionRule(CompoundRule):
    def __init__(self, element, name=None):
        spec = "<sequence> [<n> times]"
        extras = [Repetition(element, min=1, max=7, name="sequence"),
                  IntegerRef("n", 1, 100), ]
        self.defaults = {'n': 1}
        super(RepeatActionRule, self).__init__(name, spec, extras)

    def value(self, node):
        seq = node.get_child_by_name('sequence', shallow=True).value()
        n_node = node.get_child_by_name('n', shallow=True)
        n = n_node.value() if n_node is not None else self.defaults['n']
        return sum(seq * n, EmptyAction())


class PycharmGlobalRule(MappingRule):
    name = 'pycharm global'
    mapping = {
        'save all': Key('c-s'),
        "go to definition": Key("c-b"),
        '(show|find) usages': Key("a-f7"),
        'highlight usages': Key("cs-f7"),
        'peek definition': Key('cs-i'),
        '(show|peek) docs': Key('c-q'),
        '(show params|param info)': Key('c-p'),
        'show type': Key('cs-p'),
        'show type hierarchy': Key('c-h'),
        'show call hierarchy': Key('ca-h'),
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
        'close left': pyCharmAction('close all to the left'),
        'close right': pyCharmAction('close all to the right'),
        'git commit': Key('c-k'),
        'show diff': Key('c-d'),
        'next diff': Key('f7'),
        'next section': Key('tab'),
        'previous section': Key('s-tab'),
        'previous diff': Key('s-f7'),
        'compare next file': Key('a-right'),
        'compare previous file': Key('a-left'),
        'menu <letter>': Key('a-%(letter)s'),
        'hide menu': Key('s-escape'),
        'fold': Key('c-npsub'),
        '(expand|unfold)': Key('c-npadd'),
        'open file': Key('a-n/10,f'),
    }
    extras = [
        IntegerRef('n', 1, 10),
        LetterRef('letter'),
    ]
    defaults = {'n': 1, }


class NormalModeKeystrokeRule(MappingRule):
    # exported = False

    mapping = {
        "kay": Key("escape"),
        "slap": Key('enter'),

        '[<n>] <optional_count_motion>': Text('%(n)d') + Key('%(optional_count_motion)s'),
        '<no_count_motion>': Key('%(no_count_motion)s'),
        '<ln> <mandatory_count_motion>': Text('%(ln)d') + Key('%(mandatory_count_motion)s'),
        '[<n>] <find_motion>': Text('%(n)d') + Key('%(find_motion)s'),

        '[<n>] lower case <optional_count_motion>': Text('%(n)d') + Key("g,u") + Key('%(optional_count_motion)s'),
        'lower case <no_count_motion>': Key("g,u") + Key('%(no_count_motion)s'),
        '[<n>] lower case <text_object_selection>': Text('%(n)d') + Key("g,u") + Key('%(text_object_selection)s'),
        '<ln> lower case <mandatory_count_motion>': Text('%(ln)d') + Key("g,u") + Key('%(mandatory_count_motion)s'),
        '[<n>] lower case <find_motion>': Text('%(n)d') + Key("g,u") + Key('%(find_motion)s'),

        '[<n>] upper case <optional_count_motion>': Text('%(n)d') + Key("g,U") + Key('%(optional_count_motion)s'),
        'upper case <no_count_motion>': Key("g,U") + Key('%(no_count_motion)s'),
        '[<n>] upper case <text_object_selection>': Text('%(n)d') + Key("g,U") + Key('%(text_object_selection)s'),
        '<ln> upper case <mandatory_count_motion>': Text('%(ln)d') + Key("g,U") + Key('%(mandatory_count_motion)s'),
        '[<n>] upper case <find_motion>': Text('%(n)d') + Key("g,U") + Key('%(find_motion)s'),

        "(swap case|tilde)": Key("tilde"),

        "Center": Key("z,dot"),

        "[<n>] Dell <optional_count_motion> [register <register>]":
            Text('%(n)d') + Key('dquote,%(register)s,d,%(optional_count_motion)s'),
        "Dell <no_count_motion> [register <register>]":
            Key('dquote,%(register)s,d,%(no_count_motion)s'),
        '[<n>] Dell <text_object_selection> [register <register>]':
            Text('%(n)d') + Key('dquote,%(register)s,d,%(text_object_selection)s'),
        '[<n>] Dell <find_motion> [register <register>]':
            Text('%(n)d') + Key('dquote,%(register)s,d,%(find_motion)s'),

        "[<n>] Pete macro": Key("at,at:%(n)d"),

        "[<n>] join": Key("J:%(n)d"),

        '[<n>] deed': Text('d%(n)dd'),
        "Dell pair": Key("m,z,percent,m,y,percent,x,backtick,y,x,backtick,z,left"),

        "[<n>] (increment|increase)": Key("c-a:%(n)d"),
        "[<n>] (decrement|decrease)": Key("c-x:%(n)d"),
        "shift Dell": Key("s-d"),

        # to do: how to make commands undoable in a single keystroke
        "[<n>] undo": Key("u:%(n)d"),
        "[<n>] redo": Key("c-r:%(n)d"),

        "[<n>] (yank|copy) <optional_count_motion> [register <register>]":
            Text('%(n)d') + Key('dquote,%(register)s,y,%(optional_count_motion)s'),
        "(yank|copy) <no_count_motion> [register <register>]":
            Key('dquote,%(register)s,y,%(no_count_motion)s'),
        '[<n>] (yank|copy) <text_object_selection> [register <register>]':
            Text('%(n)d') + Key('dquote,%(register)s,y,%(text_object_selection)s'),
        '[<n>] (yank|copy) <find_motion> [register <register>]':
            Text('%(n)d') + Key('dquote,%(register)s,y,%(find_motion)s'),

        '[<n>] duplicate line': Text('Y%(n)dp'),
        "(yank|copy) line [register <register>]": Key("dquote,%(register)s,y,y"),
        "(yank|copy) <n> lines [register <register>]": Key("dquote,%(register)s") + Text("%(n)dY"),

        "(paste|put) [register <register>]": Key("dquote,%(register)s,p"),
        "(shift|big) (paste|put) [register <register>]": Key("dquote,%(register)s,P"),

        "replace <letter>": Key("r,%(letter)s"),

        "[<n>] (shift left|unindent)": Text('%(n)d') + Key("langle,langle"),
        "[<n>] (shift right|indent)": Text('%(n)d') + Key("rangle,rangle"),

        'Mark <letter>': Key('m,%(letter)s'),
        'jump <letter>': Key('backtick,%(letter)s'),
        'jump old': Key('c-o'),
        'jump new': Key('c-i'),

        '<ln> thru <lm> comment': mark('z') + goToLine('lm') + mark('y') +
                                  goToLine('ln') + Text('V') + jumpMark('y') +
                                  Key('c-slash') + Key('escape') + jumpMark('z'),
        '<ln> thru <lm> (copy|yank)': Key('colon/10') + Text("%(ln)d,%(lm)dy\n"),

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

        "[<n>] strip <paired_symbol>": Text('%(n)d') + Key("dquote,z,d,i,%(paired_symbol)s,left,2,x,dquote,z,P"),
        'surround <text_object_selection> with <paired_symbols>':
            Key('dquote,z,d,%(text_object_selection)s,i,%(paired_symbols)s,escape,dquote,z,P'),

        'record macro': Key('q,a'),
        'stop recording': Key('q'),
        'play macro': Key('at,a'),

        "window left": Key("c-w,h"),
        "window right": Key("c-w,l"),
        "window up": Key("c-w,k"),
        "window down": Key("c-w,j"),

        "window split": Key("c-w,s"),
        "window vertical split": Key("c-w,v"),

        "[<n>] table (next|right)": Key("g,t/10") * Repeat('n'),
        "[<n>] table (previous|left)": Key("g,T/10") * Repeat('n'),

        "cursor top": Key("s-h"),
        "cursor middle": Key("s-m"),
        "cursor (low | bottom)": Key("s-l"),

        "search <text>": Key("slash/10") + Text("%(text)s\n"),
        "shift search <text>": Key("question/10") + Text("%(text)s\n"),
        "search this": Key("asterisk"),

        '[<n>] swap up [<m> lines]': Text('%(n)d') + Key('d,d') + Text('%(m)d') + Key('k,P'),
        '[<n>] swap down [<m> lines]': Text('%(n)d') + Key('d,d') + Text('%(m)d') + Key('j,P'),
    }
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 101, default=1),
        IntegerRef('m', 1, 101, default=1),
        ShortIntegerRef("ln", 1, 10000, default=1),
        ShortIntegerRef("lm", 1, 10000, default=1),
        LetterRef('letter'),
        Choice('no_count_motion', no_count_motion_keys),
        Choice('optional_count_motion', optional_count_motion_keys),
        Choice('mandatory_count_motion', mandatory_count_motion_keys),
        Choice('text_object_selection', text_object_keys),
        FindMotionRef('find_motion'),
        Choice('register', register_keys, default='dquote'),
        Choice('paired_symbol', paired_symbol_keys),
        Choice('paired_symbols', paired_symbols_keys),
    ]


@grammar_switcher.switches_to(insert_mode_grammar)
class NormalModeToInsertModeRule(MappingRule):
    mapping = {
        "insert": Key("i"),
        "(shift|big) insert": Key("I"),
        'change <no_count_motion>': Key('c,%(no_count_motion)s,'),
        '[<n>] change <optional_count_motion>': Text('%(n)d') + Key('c,%(optional_count_motion)s'),
        '<n> change <mandatory_count_motion>': Text('%(n)d') + Key('c,%(mandatory_count_motion)s'),
        '[<n>] change <text_object_selection>': Text('%(n)d') + Key("c,%(text_object_selection)s"),
        '[<n>] change <find_motion>': Text('%(n)d') + Key('c,%(find_motion)s'),
        "(big|shift) change": Key("C"),
        "change (char|letter)": Key("s"),
        "(sub|change) line": Key("S"),
        "(after|append)": Key("a"),
        "(shift|big) (after|append)": Key("A"),
        "open": Key("o"),
        "(shift|big) open": Key("O"),
    }

    extras = [
        Choice('no_count_motion', no_count_motion_keys),
        Choice('optional_count_motion', optional_count_motion_keys),
        Choice('mandatory_count_motion', mandatory_count_motion_keys),
        Choice('text_object_selection', text_object_keys),
        FindMotionRef('find_motion'),
        IntegerRef('n', 1, 101, default=1),
    ]


@grammar_switcher.switches_to(visual_mode_grammar)
class NormalModeToVisualModeRule(MappingRule):
    mapping = {
        "visual": Key("v"),
        "visual line": Key("s-v"),
        "visual block": Key("c-v"),
        'reselect': Key('g,v'),
        'select all': Key('g,g,V,G'),
    }


@grammar_switcher.switches_to(ex_mode_grammar)
class NormalModeToExModeRule(MappingRule):
    mapping = {
        'execute': Key('colon'),
        '(sub|substitute)': Key('colon,s,slash'),
        'search': Key('slash'),
        '(big|shift) search': Key('question'),
    }


class NormalModeRule(CompoundRule):
    spec = '(<normal_repeat_command> [<transition_command>]|<transition_command>)'
    extras = [
        RuleRef(RepeatActionRule(RuleRef(NormalModeKeystrokeRule())), name='normal_repeat_command'),
        RuleAlternative([
            NormalModeToInsertModeRule(),
            NormalModeToExModeRule(),
            NormalModeToVisualModeRule(),
        ], name='transition_command')]

    def _process_recognition(self, node, extras):
        extras.get('normal_repeat_command', EmptyAction()).execute()
        extras.get('transition_command', EmptyAction()).execute()


@grammar_switcher.switches_to(normal_mode_grammar)
class VisualModeToNormalModeRule(MappingRule):
    mapping = {
        'kay': Key('escape'),
        'join': Key('J'),
        'upper case': Key('U'),
        'lower case': Key('u'),
        '(swap|switch) case': Key('tilde'),
        'Dell [register <register>]': Key('dquote,%(register)s,d'),
        'Dell lines [register <register>]': Key('dquote,%(register)s,D'),
        'yank [register <register>]': Key('dquote,%(register)s,y'),
        'yank lines [register <register>]': Key('dquote,%(register)s,Y'),
        '(paste|put) [register <register>]': Key('dquote,%(register)s,p'),
        '[<n>] (indent|shift right)': Text('%(n)d') + Key('rangle'),
        '[<n>] (unindent|shift left)': Text('%(n)d') + Key('langle'),
        'surround with <paired_symbols>': Key('dquote,z,d,i,%(paired_symbols)s,escape,dquote,z,P'),
        'replace <letter>': Key('r,%(letter)s'),
    }

    extras = [
        LetterRef('letter'),
        IntegerRef('n', min=1, max=30, default=1),
        Choice('register', register_keys, default='dquote'),
        Choice('paired_symbols', paired_symbols_keys),
    ]


class VisualModeKeystrokeRule(MappingRule):
    # exported = False

    mapping = {
        "slap": Key('enter'),
        '[<n>] <optional_count_motion>': Text('%(n)d') + Key('%(optional_count_motion)s'),
        '<no_count_motion>': Key('%(no_count_motion)s'),
        '<ln> <mandatory_count_motion>': Text('%(ln)d') + Key('%(mandatory_count_motion)s'),
        '<text_object_selection>': Key('%(text_object_selection)s'),
        '[<n>] <find_motion>': Text('%(n)d') + Key('%(find_motion)s'),
        'other': Key('o'),
        'other side': Key('O'),
        "Center": Key("z,dot"),
        "replace <letter>": Key("r,%(letter)s"),

        'Mark <letter>': Key('m,%(letter)s'),
        'jump <letter>': Key('backtick,%(letter)s'),
        'jump old': Key('c-o'),
        'jump new': Key('c-i'),

        "reverse inside singles": Text("/)?'.\\{-}'\n") + Pause('30') + Key('l'),
        "reverse inside doubles": Text('?".\\{-}"\n') + Pause('30') + Key('l'),
        "inside singles": Text("/'.\\{-}'\n") + Pause('30') + Key('l'),
        "inside doubles": Text('/".\\{-}"\n') + Pause('30') + Key('l'),
        "inside parens": Text("/(\n") + Pause('30') + Key('l'),
        "inside brackets": Text("/\\[\n") + Pause('30') + Key('l'),
        "inside braces": Text("/{\n") + Pause('30') + Key('l'),
        "inside angles": Text("/<\n") + Pause('30') + Key('l'),

        '(after|outside) parens': Text('/)\nl'),
        '(after|outside) brackets': Text('/]\nl'),
        '(after|outside) braces': Text('/}\nl'),
        '(after|outside) singles': Text('/\'\nl'),
        '(after|outside) doubles': Text('/"\nl'),
        '(after|outside) angles': Text('/>\nl'),
        'after dot': Text('/\\.\nl'),
        'after comma': Text('/,\nl'),

        "cursor top": Key("s-h"),
        "cursor middle": Key("s-m"),
        "cursor (low | bottom)": Key("s-l"),

        "search <text>": Key("slash/10") + Text("%(text)s\n"),
        "search this": Key("asterisk"),
        "shift search <text>": Key("question/10") + Text("%(text)s\n"),

    }
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 101),
        ShortIntegerRef("ln", 1, 10000),
        ShortIntegerRef("lm", 1, 10000),
        LetterRef('letter'),
        Choice('no_count_motion', no_count_motion_keys),
        Choice('optional_count_motion', optional_count_motion_keys),
        Choice('mandatory_count_motion', mandatory_count_motion_keys),
        Choice('text_object_selection', text_object_keys),
        FindMotionRef('find_motion'),
        Choice('register', register_keys),
        Choice('paired_symbol', paired_symbol_keys),
        Choice('paired_symbols', paired_symbols_keys),
    ]
    defaults = {"n": 1, "ln": 1, "lm": 1, "register": "dquote"}


@grammar_switcher.switches_to(ex_mode_grammar)
class VisualModeToExModeRule(MappingRule):
    mapping = {
        '(sub|substitute)': Key('colon,s,slash'),
    }


class VisualModeRule(CompoundRule):
    spec = '(<visual_repeat_command> [<transition_command>]|<transition_command>)'
    extras = [
        RuleRef(RepeatActionRule(RuleRef(VisualModeKeystrokeRule())), name='visual_repeat_command'),
        RuleAlternative([
            VisualModeToNormalModeRule(),
            VisualModeToExModeRule(),
        ], name='transition_command')]

    def _process_recognition(self, node, extras):
        extras.get('visual_repeat_command', EmptyAction()).execute()
        extras.get('transition_command', EmptyAction()).execute()


@grammar_switcher.switches_to(normal_mode_grammar)
class InsertModeToNormalModeRule(MappingRule):
    mapping = {
        "kay": Key('escape'),
        "cancel": Key('escape,u'),
    }


class InsertModeCommands(MappingRule):
    mapping = {
        # "<text>": Text("%(text)s"),
        "<letter_sequence>": Key('%(letter_sequence)s'),
        # "spell <letter_sequence>": Function(executeLetterSequence),
        "[<n>] (scratch|Dell)": Key("c-w:%(n)d"),
        "[<n>] slap": Key("enter:%(n)d"),
        "[<n>] tab": Key("tab:%(n)d"),
        "[<n>] back": Key("backspace:%(n)d"),
        "skip": Key('end'),
        "(scratch|Dell) line": Key("c-u"),
        "[<n>] left": Key("left:%(n)d"),
        "[<n>] right": Key("right:%(n)d"),
        "[<n>] up": Key("up:%(n)d"),
        "[<n>] down": Key("down:%(n)d"),

        'parens': Key('lparen,rparen,escape,i'),
        'brackets': Key('lbracket,rbracket,escape,i'),
        'braces': Key('lbrace,rbrace,escape,i'),
        'angles': Key('langle,rangle,escape,i'),
        '(singles|quotes)': Key('squote,squote,escape,i'),
        '(doubles|double quotes)': Key('dquote,dquote,escape,i'),

        '(after|outside) parens': Key('escape/10') + Text('/)\na'),
        '(after|outside) brackets': Key('escape/10') + Text('/]\na'),
        '(after|outside) braces': Key('escape/10') + Text('/}\na'),
        '(after|outside) singles': Key('escape/10') + Text('/\'\na'),
        '(after|outside) doubles': Key('escape/10') + Text('/"\na'),
        '(after|outside) angles': Key('escape/10') + Text('/>\na'),
        'after (doll|dollar)': Key('escape/10,A'),

        '[<n>] after <letter>': Key('escape/10,%(n)d,f,%(letter)s,a'),
        '[<n>] shift after <letter>': Key('escape/10,%(n)d,F,%(letter)s,a'),
        '[<n>] before <letter>': Key('escape/10,%(n)d,f,%(letter)s,i'),
        '[<n>] shift before <letter>': Key('escape/10,%(n)d,F,%(letter)s,i'),

        # snippets
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

    }
    extras = [
        LetterSequenceRef('letter_sequence'),
        LetterRef('letter'),
        Dictation("text"),
        IntegerRef("n", 1, 50, default=1),
    ]


class InsertModeRule(CompoundRule):
    spec = '<alternative>'
    extras = [RuleAlternative([
        RepeatActionRule(RuleAlternative([PythonRule(), InsertModeCommands(), FormatRule()])),
        InsertModeToNormalModeRule(),
    ], name='alternative')]

    def _process_recognition(self, node, extras):
        extras['alternative'].execute()


@grammar_switcher.switches_to(normal_mode_grammar)
class ExModeToNormalModeRule(MappingRule):
    mapping = {
        "kay": Key('escape'),
        "cancel": Key('escape'),
        "slap": Key('enter'),
    }


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
        "<letter_sequence>": Key('%(letter_sequence)s'),
    }
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 50, default=1),
        LetterSequenceRef('letter_sequence'),
    ]


class ExModeRule(CompoundRule):
    spec = '<alternative>'
    extras = [RuleAlternative([ExModeCommands(), ExModeToNormalModeRule()], name='alternative')]

    def _process_recognition(self, node, extras):
        extras['alternative'].execute()


normal_mode_grammar.add_rule(NormalModeRule())
visual_mode_grammar.add_rule(VisualModeRule())
insert_mode_grammar.add_rule(InsertModeRule())
ex_mode_grammar.add_rule(ExModeRule())
pycharm_grammar.add_rule(PycharmGlobalRule())

for grammar in EXPORT_GRAMMARS:
    grammar.load()
grammar_switcher.switch_to(normal_mode_grammar)


def unload():
    global pycharm_grammar
    if pycharm_grammar: pycharm_grammar.unload()
    pycharm_grammar = None

    global normal_mode_grammar
    if normal_mode_grammar: normal_mode_grammar.unload()
    normal_mode_grammar = None

    global visual_mode_grammar
    if visual_mode_grammar: visual_mode_grammar.unload()
    visual_mode_grammar = None

    global insert_mode_grammar
    if insert_mode_grammar: insert_mode_grammar.unload()
    insert_mode_grammar = None

    global ex_mode_grammar
    if ex_mode_grammar: ex_mode_grammar.unload()
    ex_mode_grammar = None
