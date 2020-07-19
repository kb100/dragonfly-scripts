from dragonfly import CompoundRule, Repetition, IntegerRef

from lib.actions import EmptyAction


class RepeatActionRule(CompoundRule):
    _repeat_action_rule_count = 0

    def __init__(self, element, name=None, exported=None):
        """
        :param element: element whose value is an ActionBase
        :param name:
        """
        if name is None:
            name = self.__class__.__name__ + str(self._repeat_action_rule_count)
            RepeatActionRule._repeat_action_rule_count += 1
        spec = "<sequence> [<n> times]"
        extras = [Repetition(element, min=1, max=7, name="sequence"),
                  IntegerRef("n", 1, 100), ]
        self.defaults = {'n': 1}

        super(RepeatActionRule, self).__init__(name=name, spec=spec, extras=extras, exported=exported)

    def value(self, node):
        seq = node.get_child_by_name('sequence', shallow=True).value()
        n_node = node.get_child_by_name('n', shallow=True)
        n = n_node.value() if n_node is not None else self.defaults['n']
        return sum(seq * n, EmptyAction())
