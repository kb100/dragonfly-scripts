from dragonfly import Text, Function, MappingRule, Dictation

from lib.common import lowercase_key_map


def replace_lowercase_keys(words):
    return [lowercase_key_map.get(word, word) for word in words]


def words_from_dictation(dictation, make_lowercase=True, hyphens_to_spaces=True, replace_nato_with_key=True):
    text = str(dictation)
    if make_lowercase:
        text = text.lower()
    if hyphens_to_spaces:
        text = text.replace('-', ' ')
    words = text.split(' ')
    if replace_nato_with_key:
        words = replace_lowercase_keys(words)
    return words


def squash_single_letter_words_together(words):
    new_words = []
    curr = []
    for word in words:
        if len(word) == 1:
            curr.append(word)
        else:
            if curr:
                new_words.append(''.join(curr))
                curr = []
            new_words.append(word)
    if curr:
        new_words.append(''.join(curr))
    return new_words


# Format: some_words
def format_score(dictation):
    """ (snake|score) <dictation> """
    words = words_from_dictation(dictation)
    words = squash_single_letter_words_together(words)
    return "_".join(words)


# Format: __some_words
def format_double_score(dictation):
    """ (double score|double under|dunder) <dictation> """
    words = words_from_dictation(dictation)
    words = squash_single_letter_words_together(words)
    return "__" + "_".join(words)


# Format: some_words()
def format_under_function(dictation):
    """ under func <dictation> """
    words = words_from_dictation(dictation)
    words = squash_single_letter_words_together(words)
    return "_".join(words) + "()"


# Format: SomeWords
def format_title(dictation):
    """ title <dictation> """
    words = words_from_dictation(dictation)
    words = [word.capitalize() for word in words]
    return "".join(words)


# Format: somewords
def format_one_word(dictation):
    """ [all] one word <dictation> """
    words = words_from_dictation(dictation)
    return "".join(words)


# Format: SOMEWORDS
def format_upper_one_word(dictation):
    """ one word upper <dictation> """
    words = words_from_dictation(dictation)
    words = [word.upper() for word in words]
    return "".join(words)


# Format: SOME_WORDS
def format_upper_score(dictation):
    """ upper score <dictation> """
    words = words_from_dictation(dictation)
    words = squash_single_letter_words_together(words)
    words = [word.upper() for word in words]
    return "_".join(words)


# Format: someWords
def format_camel(dictation):
    """ camel <dictation> """
    words = words_from_dictation(dictation)
    return words[0] + "".join(w.capitalize() for w in words[1:])


# Format: some words
def format_say(dictation):
    """ say <dictation> """
    words = words_from_dictation(dictation)
    return ' '.join(words)


# Format: Some words, and some more. And some more.
def format_prose(dictation):
    """ prose <dictation> """
    return str(dictation)


def FormatAction(function):
    def wrap_function(f):
        def _function(dictation):
            formatted_text = f(dictation)
            Text(formatted_text).execute()

        return Function(_function)

    action = wrap_function(function)
    return action


def FormatMapping(functions):
    format_functions = {}
    for function in functions:
        spoken_form = function.__doc__.strip()
        action = FormatAction(function)
        format_functions[spoken_form] = action
    return format_functions


ALL_FORMAT_FUNCTIONS = [function for name, function in globals().items()
                        if name.startswith("format_") and callable(function)]


class FormatRule(MappingRule):
    mapping = FormatMapping(ALL_FORMAT_FUNCTIONS)
    extras = [Dictation("dictation")]
