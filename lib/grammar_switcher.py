from dragonfly import MappingRule, Grammar, Function


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


class SwitcherMappingRule(MappingRule):
    mapping = {}
    extras = []
    defaults = {}

    def __init__(self, switcher, switches_to, name=None, mapping=None, extras=None, defaults=None):
        assert isinstance(switches_to, Grammar)
        assert isinstance(switcher, GrammarSwitcher)
        if mapping is None: mapping = self.mapping
        if extras is None: extras = self.extras
        if defaults is None: defaults = self.defaults
        self.switcher = switcher
        self.switches_to = switches_to
        super(SwitcherMappingRule, self).__init__(name, mapping, extras, defaults)

    def value(self, node):
        v = super(SwitcherMappingRule, self).value(node)
        return v + self.switcher.switch_to_action(self.switches_to)
