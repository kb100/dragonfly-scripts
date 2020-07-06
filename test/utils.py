from dragonfly import Keyboard, Pause, ActionBase
import pytest

@pytest.fixture()
def typed_keys(monkeypatch):
    events_buffer = []

    def send_keyboard_events(cls, events):
        events_buffer.extend([(key, down, 0) for key, down, pause_time in events])

    def pause(self, interval):
        return True

    def execute(self, data=None):
        return self._execute(data)

    monkeypatch.setattr(ActionBase, 'execute', execute)
    monkeypatch.setattr(Keyboard, 'send_keyboard_events', send_keyboard_events)
    monkeypatch.setattr(Pause, '_execute_events', pause)

    return events_buffer

def assert_same_typed_keys(typed_keys, actual, expected):
    actual.execute()
    actual_events = typed_keys[:]
    del typed_keys[:]

    expected.execute()
    expected_events = typed_keys[:]
    del typed_keys[:]

    assert actual_events == expected_events
