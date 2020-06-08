from dragonfly import *
from common import LetterRef, LetterSequenceRef, release, noSpaceNoCaps, executeLetter, executeLetterSequence, \
    executeSelect

context = AppContext(executable="chrome")
grammar = Grammar("chrome", context=context)

rules = MappingRule(
    name="chrome",
    mapping={
        "console": Key("cs-j"),
        "(escape|kay)": Key('escape'),
        "<letter_sequence>": Function(executeLetterSequence),
        "say <text>": release + Text('%(text)s'),
        "slap": Key("enter"),

        '[<n>] scroll down': Key('escape') + Text('%(n)d') + Key('j'),
        '[<n>] scroll up': Key('escape') + Text('%(n)d') + Key('k'),
        '[scroll] to the top': Key('escape') + Key('g,g'),
        '[scroll] to the bottom': Key('escape') + Key('G'),
        '[<n>] page down': Key('escape') + Text('%(n)d') + Key('d'),
        '[<n>] page up': Key('escape') + Text('%(n)d') + Key('u'),
        '[<n>] scroll left': Key('escape') + Text('%(n)d') + Key('h'),
        '[<n>] scroll right': Key('escape') + Text('%(n)d') + Key('l'),
        '[scroll] all the way left': Key('escape') + Key('z,H'),
        '[scroll] all the way right': Key('escape') + Key('z,L'),
        '(reload|refresh)': Key('escape') + Key('r'),
        '(yank|copy) current url': Key('escape') + Key('y,y'),
        'open clip': Key('escape') + Key('p'),
        '(big|shift) open clip': Key('escape') + Key('P'),
        '[<n>] see dee dot dot': Key('escape') + Text('%(n)d') + Key('g,u'),
        'see dee root': Key('escape') + Key('g,U'),
        'insert': Key('escape') + Key('i'),
        'visual': Key('escape') + Key('v'),
        'visual line': Key('escape') + Key('V'),
        'focus input': Key('escape') + Key('g,i'),
        '(follow|jump)': Key('escape') + Key('f'),
        '(big|shift) (follow|jump)': Key('escape') + Key('F'),
        # 'multi jump': Key('a-f'),
        '(yank|copy) link': Key('escape') + Key('y,f'),
        '(follow|jump) previous': Key('escape') + Key('[,['),
        '(follow|jump) next': Key('escape') + Key('],]'),
        'next frame': Key('escape') + Key('g,f'),
        '(top|main) frame': Key('escape') + Key('g,F'),
        'mark <letter_sequence>': Key('m') + Function(executeLetterSequence),
        'go to [mark] <letter_sequence>': Key('escape') + Key('backtick') + Function(executeLetterSequence),
        "open": Key("escape, o"),
        '(big|shift) open': Key('escape,O'),
        'bookmark': Key('escape') + Key('b'),
        '(big|shift) bookmark': Key('escape') + Key('B'),
        'search tabs': Key('escape') + Key('T'),
        'edit url': Key('escape') + Key('g,e'),
        '(big|shift) edit url': Key('escape') + Key('g,E'),
        '(search page|find)': Key('escape') + Key('slash'),
        '[<n>] next': Key('escape') + Text('%(n)d') + Key('n'),
        '[<n>] previous': Key('escape') + Text('%(n)d') + Key('N'),
        '[<n>] back': Key('escape') + Text('%(n)d') + Key('H'),
        '[<n>] forward': Key('escape') + Text('%(n)d') + Key('L'),
        '[<n>] new tab': Key('escape') + Text('%(n)d') + Key('t'),
        '[<n>] tab left': Key('escape') + Text('%(n)d') + Key('J'),
        '[<n>] tab right': Key('escape') + Text('%(n)d') + Key('K'),
        'tab back': Key('escape') + Key('^'),
        'tab first': Key('escape') + Key('g,0'),
        'tab last': Key('escape') + Key('g,dollar'),
        'tab [<n>]': Key('escape') + Key('c-%(n)d'),
        '[<n>] (dupe|duplicate) tab': Key('escape') + Text('%(n)d') + Key('y,t'),
        '(pin|unpin) tab': Key('escape') + Key('a-p'),
        '(mute|unmute) tab': Key('escape') + Key('a-m'),
        '[<n>] (dell|close) tab': Key('escape') + Text('%(n)d') + Key('x'),
        "kill tab": Key("c-w"),
        '[<n>] restore tab': Key('escape') + Text('%(n)d') + Key('X'),
        'move tab to [new] window': Key('escape') + Key('W'),
        '[<n>] move tab left': Key('escape') + Text('%(n)d') + Key('<,<'),
        '[<n>] move tab right': Key('escape') + Text('%(n)d') + Key('>,>'),
        'show help': Key('escape') + Key('?'),
        'view source': Key('escape') + Key('g,s'),

        '(cell|select) [<n>]': Function(executeSelect, offset=0),
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

grammar.add_rule(rules)

grammar.load()


def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
