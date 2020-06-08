from dragonfly import *


release = Key("shift:up, ctrl:up")

class LetterRule(MappingRule):
    exported = True
    mapping = {
        'alpha': Key('a', static=True),
        'bravo': Key('b', static=True),
        'charlie': Key('c', static=True),
        '(delta|dixie)': Key('d', static=True),
        'echo': Key('e', static=True),
        'foxtrot': Key('f', static=True),
        'golf': Key('g', static=True),
        'hotel': Key('h', static=True),
        'india': Key('i', static=True),
        'juliet': Key('j', static=True),
        'kilo': Key('k', static=True),
        'lima': Key('l', static=True),
        'mike': Key('m', static=True),
        'november': Key('n', static=True),
        'oscar': Key('o', static=True),
        'papa': Key('p', static=True),
        '(queen|quebec)': Key('q', static=True),
        'romeo': Key('r', static=True),
        'sierra': Key('s', static=True),
        'tango': Key('t', static=True),
        'uniform': Key('u', static=True),
        'victor': Key('v', static=True),
        'whiskey': Key('w', static=True),
        'x-ray': Key('x', static=True),
        'yankee': Key('y', static=True),
        'zulu': Key('z', static=True),

        '(upper|big) alpha': Key('A', static=True),
        '(upper|big) bravo': Key('B', static=True),
        '(upper|big) charlie': Key('C', static=True),
        '(upper|big) (delta|dixie)': Key('D', static=True),
        '(upper|big) echo': Key('E', static=True),
        '(upper|big) foxtrot': Key('F', static=True),
        '(upper|big) golf': Key('G', static=True),
        '(upper|big) hotel': Key('H', static=True),
        '(upper|big) india': Key('I', static=True),
        '(upper|big) juliet': Key('J', static=True),
        '(upper|big) kilo': Key('K', static=True),
        '(upper|big) lima': Key('L', static=True),
        '(upper|big) mike': Key('M', static=True),
        '(upper|big) november': Key('N', static=True),
        '(upper|big) oscar': Key('O', static=True),
        '(upper|big) papa': Key('P', static=True),
        '(upper|big) (queen|quebec)': Key('Q', static=True),
        '(upper|big) romeo': Key('R', static=True),
        '(upper|big) sierra': Key('S', static=True),
        '(upper|big) tango': Key('T', static=True),
        '(upper|big) uniform': Key('U', static=True),
        '(upper|big) victor': Key('V', static=True),
        '(upper|big) whiskey': Key('W', static=True),
        '(upper|big) x-ray': Key('X', static=True),
        '(upper|big) yankee': Key('Y', static=True),
        '(upper|big) zulu': Key('Z', static=True),

        'zero': Key('0'),
        'one': Key('1'),
        'two': Key('2'),
        'three': Key('3'),
        'four': Key('4'),
        'five': Key('5'),
        'six': Key('6'),
        'seven': Key('7'),
        'eight': Key('8'),
        'nine': Key('9'),

        'space': Key('space'),
        'tab': Key('tab'),

        'ampersand': Key('ampersand'),
        'apostrophe': Key('apostrophe'),
        'asterisk': Key('asterisk'),
        'at': Key('at'),
        'backslash': Key('backslash'),
        'backtick': Key('backtick'),
        'bar': Key('bar'),
        'caret': Key('caret'),
        'colon': Key('colon'),
        'comma': Key('comma'),
        'dollar': Key('dollar'),
        '(dot|period)': Key('dot'),
        'double quote': Key('dquote'),
        'equal': Key('equal'),
        'bang': Key('exclamation'),
        'hash': Key('hash'),
        'hyphen': Key('hyphen'),
        'minus': Key('minus'),
        'percent': Key('percent'),
        'plus': Key('plus'),
        'question': Key('question'),
        # Getting Invalid key name: 'semicolon'
        # 'semicolon': Key('semicolon'),
        'slash': Key('slash'),
        '[single] quote': Key('squote'),
        'tilde': Key('tilde'),
        'underscore | score': Key('underscore'),

        'langle': Key('langle'),
        'lace': Key('lbrace'),
        'lack': Key('lbracket'),
        'laip': Key('lparen'),
        'rangle': Key('rangle'),
        'race': Key('rbrace'),
        'rack': Key('rbracket'),
        'raip': Key('rparen'),
    }


def LetterRef(name):
    return RuleRef(rule=LetterRule(), name=name)


def LetterSequenceRef(name, min=1, max=32):
    return Repetition(LetterRef(name+'_letter'), min=min, max=max, name=name)


noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")


def executeLetter(letter):
    letter.execute()


def executeLetterSequence(letter_sequence):
    for letter in letter_sequence:
        letter.execute()

def executeSelect(n):
    n -= 1
    if n > 0:
        Key("down/25:" + str(n) + '/25,enter').execute()
    else:
        Key('enter').execute()
