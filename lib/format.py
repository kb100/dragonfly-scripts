# Format: some_words
from dragonfly import Text, Function, MappingRule, Dictation


def format_score(dictation):  # Function name must start with "format_".
    """ (snake|score) <dictation> """  # Docstring defining spoken-form.
    text = str(dictation)  # Get written-form of dictated text.
    return "_".join(text.split(" "))  # Put underscores between words.

# __some_words
def format_double_score(dictation):
    """ (double score|double under|dunder) <dictation> """
    text = str(dictation)
    return "__" + "_".join(text.split(" "))


# Format: some_words()
def format_under_function(dictation):
    """ under func <dictation> """
    text = str(dictation)
    return "_".join(text.split(" ")) + "()"


# Format: SomeWords
def format_title(dictation):
    """ title <dictation> """
    text = str(dictation)
    words = [word.capitalize() for word in text.split(" ")]
    return "".join(words)


# Format: somewords
def format_one_word(dictation):
    """ [all] one word <dictation> """
    text = str(dictation)
    return "".join(text.split(" "))


# Format: SOMEWORDS
def format_upper_one_word(dictation):
    """ one word upper <dictation> """
    text = str(dictation)
    words = [word.upper() for word in text.split(" ")]
    return "".join(words)


# Format: SOME_WORDS
def format_upper_score(dictation):
    """ upper score <dictation> """
    text = str(dictation)
    words = [word.upper() for word in text.split(" ")]
    return "_".join(words)


# Format: someWords
def format_camel(dictation):
    """ camel <dictation> """
    text = str(dictation)
    words = text.split(" ")
    return words[0] + "".join(w.capitalize() for w in words[1:])

# Format: some words
def format_say(dictation):
    """ say <dictation> """
    text = str(dictation)
    return text


def FormatAction(function):
    def wrap_function(function):
        def _function(dictation):
            formatted_text = function(dictation)
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
