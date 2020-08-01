from dragonfly import Function


class GrammarSwitcher(object):
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
