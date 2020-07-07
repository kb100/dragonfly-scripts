def assert_same_typed_keys(typed_keys, actual, expected):
    actual.execute()
    actual_events = typed_keys[:]
    del typed_keys[:]

    expected.execute()
    expected_events = typed_keys[:]
    del typed_keys[:]

    assert actual_events == expected_events
