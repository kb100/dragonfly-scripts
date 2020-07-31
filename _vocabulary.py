from dragonfly import *
from dragonfly.windows import Clipboard

clipboard = Clipboard()
vocab_dict = DictList('vocab_dict')
vocab_dict['test'] = 'test_vocab'


def add_clipboard_contents_to_vocabulary(text):
    # note that set clipboard=unnamaedplus is needed to work with vim
    clipboard.copy_from_system()
    clip_text = clipboard.get_text()
    if text and clip_text:
        vocab_dict[str(text)] = clip_text


def del_from_vocabulary(text):
    vocab_dict.pop(str(text), None)


def clear_vocabulary():
    vocab_dict.clear()


def type_out_vocabulary():
    action = Text('%(key)s: %(value)s')
    for k, v in vocab_dict.items():
        action.bind({'key': k, 'value': v}).execute()


class VocabRule(MappingRule):
    mapping = {
        'new vocab <text>': Function(add_clipboard_contents_to_vocabulary),
        '(Dell|delete) vocab <text>': Function(del_from_vocabulary),
        'clear vocab': Function(clear_vocabulary),
        'recall <vocab>': Text('%(vocab)s'),
        'list vocab': Function(type_out_vocabulary)
    }
    extras = [
        Dictation('text'),
        DictListRef('vocab', vocab_dict)
    ]
    defaults = {}


vocab_grammar = Grammar('vocab grammar')
vocab_grammar.add_rule(VocabRule())
vocab_grammar.load()


# Unload function which will be called at unload time.
def unload():
    global vocab_grammar
    if vocab_grammar: vocab_grammar.unload()
    vocab_grammar = None
