import time

from dragonfly import *
from dragonfly.engines.base.timer import Timer
from enum import Enum


class ScrollType(Enum):
    WHEEL_DOWN = Mouse('wheeldown')
    WHEEL_UP = Mouse('wheelup')
    PAGE_DOWN = Key('pagedown')
    PAGE_UP = Key('pageup')


class ScrollState(object):
    timer = None  # type: Optional[Timer]
    speed = 0  # type: int
    action = ScrollType.WHEEL_DOWN  # type: ScrollType

    @classmethod
    def reset(cls):
        cls.timer = None
        cls.speed = 0
        cls.direction = ScrollType.WHEEL_DOWN


def start_scrolling(speed, scroll_action):
    speed = max(0, speed)
    if ScrollState.timer is None:
        if speed == 0: return

        def do_scroll():
            ScrollState.action.value.execute()

        e = get_engine()
        interval = 1.0 / speed
        repeating = True
        timer = e.create_timer(do_scroll, interval, repeating)
        ScrollState.speed = speed
        ScrollState.action = scroll_action
        ScrollState.timer = timer
        ScrollState.timer.next_time = time.time()
        timer.start()
    elif speed != 0:
        ScrollState.timer.interval = 1.0 / speed
        ScrollState.speed = speed
        ScrollState.action = scroll_action
        ScrollState.timer.next_time = time.time()
    else:
        stop_scrolling()


def scroll_faster():
    start_scrolling(ScrollState.speed + 1, ScrollState.action)


def scroll_slower():
    start_scrolling(ScrollState.speed - 1, ScrollState.action)


def stop_scrolling():
    if ScrollState.timer is not None:
        ScrollState.timer.stop()
        ScrollState.reset()


class ScrollingRule(MappingRule):
    mapping = {
        '[<speed>] start <scroll_action>': Function(start_scrolling),
        'faster': Function(scroll_faster),
        'slower': Function(scroll_slower),
        'stop': Function(stop_scrolling),
    }
    extras = [
        IntegerRef('speed', min=1, max=10, default=3),
        Choice('scroll_action', choices={
            'scrolling [down]': ScrollType.WHEEL_DOWN,
            'scrolling up': ScrollType.WHEEL_UP,
            'paging [down]': ScrollType.PAGE_DOWN,
            'paging up': ScrollType.PAGE_UP,
        }, default=ScrollType.WHEEL_DOWN),
    ]


grammar = Grammar('scrolling')
grammar.add_rule(ScrollingRule())
grammar.load()


def unload():
    stop_scrolling()

    global grammar
    if grammar: grammar.unload()
    grammar = None
