from dragonfly import Alternative, RuleRef, ElementBase, Rule


class RuleOrElemAlternative(Alternative):
    def __init__(self, rules_or_elements, name=None, default=None):
        assert all([isinstance(x, Rule) or isinstance(x, ElementBase) for x in rules_or_elements])

        def wrap_if_rule(x):
            return RuleRef(x) if isinstance(x, Rule) else x

        children = [wrap_if_rule(x) for x in rules_or_elements]
        super(RuleOrElemAlternative, self).__init__(children, name, default)
