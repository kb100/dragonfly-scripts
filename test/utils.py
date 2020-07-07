def assert_same_typed_keys(typed_keys, actual, expected):
    expected.execute()
    typed_keys['expected'] = typed_keys['buffer'][:]
    del typed_keys['buffer'][:]

    actual.execute()
    typed_keys['actual'] = typed_keys['buffer'][:]
    del typed_keys['buffer'][:]

    assert typed_keys['actual'] == typed_keys['expected']
