import pytest
from dragonfly import ActionBase, Keyboard, Pause


@pytest.fixture()
def typed_keys(monkeypatch):
    events_buffer = []
    actual_buffer = []
    expected_buffer = []
    ret = {'buffer': events_buffer, 'actual': actual_buffer, 'expected': expected_buffer}

    def send_keyboard_events(cls, events):
        events_buffer.extend([(key, down) for key, down, pause_time in events])

    def pause(self, interval):
        return True

    def execute(self, data=None):
        return self._execute(data)

    monkeypatch.setattr(ActionBase, 'execute', execute)
    monkeypatch.setattr(Keyboard, 'send_keyboard_events', send_keyboard_events)
    monkeypatch.setattr(Pause, '_execute_events', pause)

    return ret
