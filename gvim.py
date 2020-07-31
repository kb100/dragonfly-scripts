import logging
from itertools import chain

import enum
from dragonfly import *

from lib.actions import MarkedAction
from lib.common import LetterRef, LetterSequenceRef, single_character_key_map
from lib.elements import RuleOrElemAlternative
from lib.format import FormatRule
from lib.grammar_switcher import GrammarSwitcher
from lib.rules import RepeatActionRule


@enum.unique
class VimMode(enum.Enum):
    NORMAL = 0
    INSERT = 1
    VISUAL = 2
    EX = 3


class VimGrammarSwitcher(GrammarSwitcher):
    def __init__(self, normal=None, insert=None, visual=None, ex=None):
        self.modes = {
            VimMode.NORMAL: normal,
            VimMode.INSERT: insert,
            VimMode.VISUAL: visual,
            VimMode.EX: ex,
        }
        grammars = [g for g in self.modes.values() if g is not None]
        super(VimGrammarSwitcher, self).__init__(grammars)

    def __str__(self):
        active = [mode for mode, gram in self.modes.items() if gram and gram.enabled]
        return str(self.__class__) + str(active)

    def switch_to_mode(self, mode):
        logging.info('Setting vim mode to: ' + str(mode))
        self.switch_to(self.modes[mode])

    def switch_to_mode_action(self, mode):
        return self.switch_to_action(self.modes[mode])

    @staticmethod
    def mark_switches_to_mode(mode):
        assert mode in VimMode

        def class_modifier(cls):
            assert hasattr(cls, 'value')
            assert callable(cls.value)
            old_value = cls.value

            def value(this, node):
                v = old_value(this, node)
                return MarkedAction(v, mark=mode)

            cls.value = value
            return cls

        return class_modifier


class TransitionThenRepeatRule(CompoundRule):
    non_transitions = []
    transitions = []

    def __init__(self, vim_mode_switcher=None, non_transitions=None, transitions=None, name=None, exported=None):
        if vim_mode_switcher is not None: assert isinstance(vim_mode_switcher, VimGrammarSwitcher)
        self.switcher = vim_mode_switcher
        if non_transitions is None: non_transitions = self.non_transitions
        if transitions is None: transitions = self.transitions
        assert all([not isinstance(x, Rule) or not x.exported for x in non_transitions + transitions])
        spec = '<transition_command> [<repeat_command>]'
        extras = [
            RuleRef(RepeatActionRule(RuleOrElemAlternative(non_transitions), exported=False), name='repeat_command'),
            RuleOrElemAlternative(transitions, name='transition_command')]
        super(TransitionThenRepeatRule, self).__init__(name=name, spec=spec, extras=extras, exported=exported)

    def _process_recognition(self, node, extras):
        transition = extras['transition_command']
        transition.execute()
        if isinstance(transition, MarkedAction):
            mode = transition.mark
            self.switcher.switch_to_mode(mode)
        repeat = extras.get('repeat_command', None)
        if repeat is not None:
            repeat.execute()

    def value(self, node):
        transition = node.get_child_by_name('transition_command', shallow=True)
        repeat = node.get_child_by_name('repeat_command', shallow=True)
        transition_value = transition.value()
        v = transition_value + repeat.value() if repeat else transition_value
        if isinstance(transition_value, MarkedAction):
            mode = transition_value.mark
            return MarkedAction(v, mode)
        else:
            return v


class RepeatThenTransitionRule(CompoundRule):
    non_transitions = []
    transitions = []

    def __init__(self, vim_mode_switcher=None, non_transitions=None, transitions=None, name=None, exported=None):
        if vim_mode_switcher is not None: assert isinstance(vim_mode_switcher, VimGrammarSwitcher)
        self.switcher = vim_mode_switcher
        if non_transitions is None: non_transitions = self.non_transitions
        if transitions is None: transitions = self.transitions
        assert all([not isinstance(x, Rule) or not x.exported for x in non_transitions + transitions])
        spec = '(<repeat_command> [<transition_command>]|<transition_command>)'
        extras = [
            RuleRef(RepeatActionRule(RuleOrElemAlternative(non_transitions), exported=False), name='repeat_command'),
            RuleOrElemAlternative(transitions, name='transition_command')]
        super(RepeatThenTransitionRule, self).__init__(name=name, spec=spec, extras=extras, exported=exported)

    def _process_recognition(self, node, extras):
        repeat = extras.get('repeat_command', None)
        if repeat is not None:
            repeat.execute()
        transition = extras.get('transition_command', None)
        if transition is not None:
            transition.execute()
            if isinstance(transition, MarkedAction):
                mode = transition.mark
                self.switcher.switch_to_mode(mode)

    def value(self, node):
        transition = node.get_child_by_name('transition_command', shallow=True)
        repeat = node.get_child_by_name('repeat_command', shallow=True)
        if transition is not None:
            transition_value = transition.value()
            v = transition_value + repeat.value() if repeat else transition_value
            if isinstance(transition_value, MarkedAction):
                mode = transition_value.mark
                return MarkedAction(v, mode)
            else:
                return v
        else:
            return repeat.value()


text_object_selection_exclusive_keys = {
    'a': 'a',
    '(inner|in)': 'i',
}
text_object_selection_objects = {
    "(word|whiskey)": "w",
    "(big|shift) (word|whiskey)": "W",
    "sentence": "s",
    "paragraph": "p",
    "(bracket|lack|rack)": "rbracket",
    "(paren|lip|rip)": "rparen",
    "(angle|langle|rangle)": "rangle",
    "tag": "t",
    "(brace|lace|race)": "rbrace",
    "(double quote|D quote|doubles)": "dquote",
    "(quote|singles)": "squote",
    "(backtick|tick|grave)": "backtick",
}
text_object_keys = {}
for sp1, k1 in text_object_selection_exclusive_keys.items():
    for sp2, k2 in text_object_selection_objects.items():
        text_object_keys[sp1 + ' ' + sp2] = k1 + ',' + k2
paired_symbols_keys = {
    "(bracket|lack|rack)": "lbracket,rbracket",
    "(paren|lip|rip)": "lparen,rparen",
    "(angle|langle|rangle)": "langle,rangle",
    "(brace|lace|race)": "lbrace,rbrace",
    "(double quote|D quote|doubles)": "dquote,dquote",
    "(quote|singles)": "squote,squote",
    "(backtick|tick|grave)": "backtick,backtick",
    'space': 'space,space',
}
paired_symbol_keys = {
    "(bracket|lack|rack)": "rbracket",
    "(paren|lip|rip)": "rparen",
    "(angle|langle|rangle)": "rangle",
    "(brace|lace|race)": "rbrace",
    "(double quote|D quote|doubles)": "dquote",
    "(quote|singles)": "squote",
    "(backtick|tick|grave)": "backtick",
    'space': 'space',
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
        choices = {k + ' <letter>': f for k, f in find_motion_keys.items()}
        extras = [LetterRef('letter')]
        super(FindMotionRef, self).__init__(name, choices, extras, default)

    def value(self, node):
        f = super(FindMotionRef, self).value(node)
        letter = node.get_child_by_name('letter', shallow=True).value()
        return f + ',' + letter


valid_registers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'dot', 'percent',
                   'hash', 'colon', 'dquote']
register_keys = {k: v for k, v in single_character_key_map.items() if v.lower() in valid_registers}


def mark(s):
    return Key('m,' + s)


def jump_mark(s):
    return Key('backtick,' + s)


def go_line(s):
    return Key("colon") + Text("%(" + s + ")d\n") + Pause('10')


def swap_quotes_action(n, swap_quotes):
    q1 = swap_quotes
    q2 = 'squote' if q1 == 'dquote' else 'dquote'
    (Text(str(n)) + Key("dquote,z,d,i," + q1 + ',left,2,r,' + q2 + ',right,dquote,z,P')).execute()


class NormalModeCommands(MappingRule):
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

        '[<n>] (duplicate|dupe) [line]': Text('Y%(n)dp'),
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

        '<ln> thru <lm> comment': mark('z') + go_line('lm') + mark('y') +
                                  go_line('ln') + Text('V') + jump_mark('y') +
                                  Key('c-slash') + Key('escape') + jump_mark('z'),
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
        "[<n>] swap <swap_quotes>": Function(swap_quotes_action),
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
        Choice('swap_quotes',
               choices={
                   "(double quote|D quote|doubles)": "dquote",
                   "(quote|singles)": "squote",
               })
    ]


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.INSERT)
class NormalModeToInsertModeCommands(MappingRule):
    mapping = {
        "insert": Key("i"),
        "(shift|big) insert": Key("I"),
        'change <no_count_motion>': Key('c,%(no_count_motion)s,'),
        '[<n>] change <optional_count_motion>': Text('%(n)d') + Key('c,%(optional_count_motion)s'),
        '<n> change <mandatory_count_motion>': Text('%(n)d') + Key('c,%(mandatory_count_motion)s'),
        '[<n>] chan <text_object_selection_object>': Text('%(n)d') + Key("c,a,%(text_object_selection_object)s"),
        '[<n>] chin <text_object_selection_object>': Text('%(n)d') + Key("c,i,%(text_object_selection_object)s"),
        '[<n>] chat <letter>': Text('%(n)d') + Key("c,t,%(letter)s"),
        '[<n>] chaff <letter>': Text('%(n)d') + Key("c,f,%(letter)s"),
        '[<n>] chew': Text('%(n)d') + Key('c,w'),
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
        LetterRef('letter'),
        Choice('no_count_motion', no_count_motion_keys),
        Choice('optional_count_motion', optional_count_motion_keys),
        Choice('mandatory_count_motion', mandatory_count_motion_keys),
        Choice('text_object_selection', text_object_keys),
        Choice('text_object_selection_object', text_object_selection_objects),
        FindMotionRef('find_motion'),
        IntegerRef('n', 1, 101, default=1),
    ]


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.VISUAL)
class NormalModeToVisualModeCommands(MappingRule):
    mapping = {
        "visual": Key("v"),
        "visual line": Key("s-v"),
        "visual block": Key("c-v"),
        'reselect': Key('g,v'),
        'select all': Key('g,g,V,G'),
    }


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.EX)
class NormalModeToExModeCommands(MappingRule):
    mapping = {
        'execute': Key('colon'),
        '(sub|substitute)': Key('colon,s,slash'),
        'search': Key('slash'),
        '(big|shift) search': Key('question'),
    }


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.NORMAL)
class VisualModeToNormalModeCommands(MappingRule):
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


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.INSERT)
class VisualModeToInsertModeCommands(MappingRule):
    mapping = {
        'change': Key('c'),
    }


class VisualModeCommands(MappingRule):
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
        IntegerRef("n", 1, 101, default=1),
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


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.EX)
class VisualModeToExModeCommands(MappingRule):
    mapping = {
        '(sub|substitute)': Key('colon,s,slash'),
    }


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.NORMAL)
class InsertModeToNormalModeCommands(MappingRule):
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


@VimGrammarSwitcher.mark_switches_to_mode(VimMode.NORMAL)
class ExModeToNormalModeCommands(MappingRule):
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


def get_transitions():
    return {
        (VimMode.NORMAL, VimMode.INSERT): [NormalModeToInsertModeCommands(exported=False)],
        (VimMode.NORMAL, VimMode.VISUAL): [NormalModeToVisualModeCommands(exported=False)],
        (VimMode.NORMAL, VimMode.EX): [NormalModeToExModeCommands(exported=False)],
        (VimMode.INSERT, VimMode.NORMAL): [InsertModeToNormalModeCommands(exported=False)],
        (VimMode.VISUAL, VimMode.NORMAL): [VisualModeToNormalModeCommands(exported=False)],
        (VimMode.VISUAL, VimMode.INSERT): [VisualModeToInsertModeCommands(exported=False)],
        (VimMode.VISUAL, VimMode.EX): [VisualModeToExModeCommands(exported=False)],
        (VimMode.EX, VimMode.NORMAL): [ExModeToNormalModeCommands(exported=False)],
    }


def get_commands():
    return {
        VimMode.NORMAL: [NormalModeCommands(exported=False)],
        VimMode.VISUAL: [VisualModeCommands(exported=False)],
        VimMode.INSERT: [InsertModeCommands(exported=False), FormatRule(exported=False)],
        VimMode.EX: [ExModeCommands(exported=False)],
    }


def transitions_into_mode(transitions, mode):
    return list(chain.from_iterable(
        rules for (source, destination), rules in transitions.items() if destination is mode
    ))


def transitions_out_of_mode(transitions, mode):
    return list(chain.from_iterable(
        rules for (source, destination), rules in transitions.items() if source is mode
    ))


def _make_transition_then_repeats(commands, prefix, transitions):
    return {
        (source, destination):
            [TransitionThenRepeatRule(non_transitions=commands[destination],
                                      transitions=transitions[(source, destination)],
                                      name=prefix + source.name.capitalize() + 'To' + destination.name.capitalize() + 'Rule',
                                      exported=False)]
        for (source, destination) in transitions
    }


def _make_mode_rules(commands, grammar_switcher, prefix, transition_then_repeats):
    return {
        mode: RepeatThenTransitionRule(vim_mode_switcher=grammar_switcher,
                                       non_transitions=commands[mode],
                                       transitions=transitions_out_of_mode(transition_then_repeats, mode),
                                       name=prefix + mode.name.capitalize() + 'Rule')
        for mode in commands
    }


def make_vim_grammars(commands, transitions, context=None, prefix=''):
    transition_then_repeats = _make_transition_then_repeats(commands, prefix, transitions)
    grammars = {mode: Grammar(prefix + mode.name.capitalize() + 'Mode', context=context) for mode in commands}

    grammar_switcher = VimGrammarSwitcher(grammars[VimMode.NORMAL], grammars[VimMode.INSERT], grammars[VimMode.VISUAL],
                                          grammars[VimMode.EX])
    mode_rules = _make_mode_rules(commands, grammar_switcher, prefix, transition_then_repeats)
    for mode in commands:
        grammars[mode].add_rule(mode_rules[mode])
    return grammars, grammar_switcher
