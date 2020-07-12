from dragonfly import *

release = Key("shift:up, ctrl:up")

lowercase_key_map = {
    'alpha': 'a',
    'bravo': 'b',
    'charlie': 'c',
    'delta': 'd',
    'echo': 'e',
    'foxtrot': 'f',
    'golf': 'g',
    'hotel': 'h',
    'india': 'i',
    'juliet': 'j',
    'kilo': 'k',
    'lima': 'l',
    'mike': 'm',
    'november': 'n',
    'oscar': 'o',
    'papa': 'p',
    'quebec': 'q',
    'romeo': 'r',
    'sierra': 's',
    'tango': 't',
    'uniform': 'u',
    'victor': 'v',
    'whiskey': 'w',
    'x-ray': 'x',
    'yankee': 'y',
    'zulu': 'z',
}

uppercase_key_map = {'(big|upper) ' + spoken: l.upper()
                     for spoken, l in lowercase_key_map.items()}

digits_key_map = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

special_character_key_map = {
    'space': 'space',
    'tab': 'tab',

    'ampersand': 'ampersand',
    'apostrophe': 'apostrophe',
    '(star|asterisk)': 'asterisk',
    'at': 'at',
    'backslash': 'backslash',
    'backtick': 'backtick',
    '(bar|pipe)': 'bar',
    'caret': 'caret',
    'colon': 'colon',
    'comma': 'comma',
    'dollar': 'dollar',
    '(dot|period)': 'dot',
    'double quote': 'dquote',
    'equal': 'equal',
    '(bang|exclamation)': 'exclamation',
    '(hash|pound|number sign)': 'hash',
    'hyphen': 'hyphen',
    'dash': 'hyphen',
    'minus': 'minus',
    'percent': 'percent',
    'plus': 'plus',
    'question': 'question',
    'semicolon': 'semicolon',
    'slash': 'slash',
    '[single] quote': 'squote',
    'tilde': 'tilde',
    '(underscore | score)': 'underscore',
    'langle': 'langle',
    'lace': 'lbrace',
    'lack': 'lbracket',
    'lip': 'lparen',
    'rangle': 'rangle',
    'race': 'rbrace',
    'rack': 'rbracket',
    'rip': 'rparen',
}

single_character_key_map = {}
single_character_key_map.update(lowercase_key_map)
single_character_key_map.update(uppercase_key_map)
single_character_key_map.update(digits_key_map)
single_character_key_map.update(special_character_key_map)


def LetterRef(name=None):
    return Choice(name, single_character_key_map)


class LetterSequenceRef(Modifier):
    def __init__(self, name):
        element = Repetition(LetterRef(), min=1, max=32, name=name)

        def modifier(v):
            return ','.join(v)

        super(LetterSequenceRef, self).__init__(element, modifier)


class SpellLetterSequenceRule(MappingRule):
    mapping = {"spell <letters>": Key("%(letters)s")}
    extras = [LetterSequenceRef("letters")]


def execute_select(n, offset=1):
    n -= offset
    if n > 0:
        Key("down/25:" + str(n) + '/25,enter').execute()
    else:
        Key('enter').execute()
