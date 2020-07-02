from dragonfly import *

release = Key("shift:up, ctrl:up")

lowercaseKeyMap = {
    'alpha': 'a',
    'bravo': 'b',
    'charlie': 'c',
    '(delta|dixie)': 'd',
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
    '(queen|quebec)': 'q',
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

uppercaseKeyMap = {'(big|upper) ' + spoken: l.upper()
                   for spoken, l in lowercaseKeyMap.items()}

digitsKeyMap = {
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

specialCharacterKeyMap = {
    'space': 'space',
    'tab': 'tab',

    'ampersand': 'ampersand',
    'apostrophe': 'apostrophe',
    'asterisk': 'asterisk',
    'at': 'at',
    'backslash': 'backslash',
    'backtick': 'backtick',
    'bar|pipe': 'bar',
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
    'underscore | score': 'underscore',
    'langle': 'langle',
    'lace': 'lbrace',
    'lack': 'lbracket',
    'lip': 'lparen',
    'rangle': 'rangle',
    'race': 'rbrace',
    'rack': 'rbracket',
    'rip': 'rparen',
}

singleCharacterKeyMap = {}
singleCharacterKeyMap.update(lowercaseKeyMap)
singleCharacterKeyMap.update(uppercaseKeyMap)
singleCharacterKeyMap.update(digitsKeyMap)
singleCharacterKeyMap.update(specialCharacterKeyMap)


def LetterRef(name):
    return Choice(name, singleCharacterKeyMap)


class LetterSequenceRule(CompoundRule):
    spec = '<letter_sequence>'
    extras = [Repetition(LetterRef('letter'), min=1, max=32, name='letter_sequence')]

    def value(self, node):
        seq = node.get_child_by_name('letter_sequence')
        return ','.join(seq.value())


def LetterSequenceRef(name):
    return RuleRef(LetterSequenceRule(), name)

class SpellLetterSequenceRule(MappingRule):
    mapping = {"spell <letter_sequence>": Key("%(letter_sequence)s")}
    extras = [LetterSequenceRef("letter_sequence")]


noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")


def executeSelect(n, offset=1):
    n -= offset
    if n > 0:
        Key("down/25:" + str(n) + '/25,enter').execute()
    else:
        Key('enter').execute()


class EmptyAction(ActionBase):
    def execute(self, data=None):
        pass
