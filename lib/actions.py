from dragonfly import ActionBase


class EmptyAction(ActionBase):
    def execute(self, data=None):
        pass


class MarkedAction(ActionBase):
    def __init__(self, action, mark=None):
        assert isinstance(action, ActionBase)
        self.action = action
        self.mark = mark
        super(MarkedAction, self).__init__()

    def execute(self, data=None):
        return self.action.execute(data)
