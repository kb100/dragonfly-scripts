from dragonfly import Alternative, RuleRef, ElementBase, Rule


class RuleOrElemAlternative(Alternative):
    def __init__(self, rules_or_elements, name=None, default=None):
        assert all([isinstance(x, Rule) or isinstance(x, ElementBase) for x in rules_or_elements])

        def wrap_if_rule(x):
            return RuleRef(x) if isinstance(x, Rule) else x

        children = [wrap_if_rule(x) for x in rules_or_elements]
        super(RuleOrElemAlternative, self).__init__(children, name, default)


class Exclusion(Alternative):
    """
    Prevents a child element from decoding if it matches an exclusion element or function.
    """

    def __init__(self, element, exclusion=None, exclude_if_func=None):
        """
        :param element: element to be wrapped
        :param exclusion: element to exclude, may be None
        :param exclude_if_func: function accepting words, may be None
        """
        self._element = element
        self._exclusion = exclusion
        self._exclude_if_func = exclude_if_func
        super(Exclusion, self).__init__((element,), name=element.name, default=element.default)

    def decode(self, state):
        state.decode_attempt(self)

        # see if this decoding should be excluded
        if self._exclusion is not None:
            for _ in self._exclusion.decode(state):
                state.decode_failure(self)
                return
            state.decode_rollback(self)

        if self._exclude_if_func is not None:
            # let the element try to match and then see if it should be excluded by words
            begin = state._index
            for _ in self._element.decode(state):
                end = state._index
                words = state.words(begin, end)
                if not self._exclude_if_func(words):
                    state.decode_success(self)
                    yield state
                state.decode_retry(self)
        else:
            # the decoding doesn't need to be excluded, continue as normal
            for _ in self._element.decode(state):
                state.decode_success(self)
                yield state
                state.decode_retry(self)

        state.decode_failure(self)
        return


class PhrasesExclusion(Exclusion):
    def __init__(self, element, phrases_to_exclude):
        self._phrases = phrases_to_exclude

        def exclude_if(words):
            text = ' '.join(words)
            return any(phrase in text for phrase in phrases_to_exclude)

        super(PhrasesExclusion, self).__init__(element, exclude_if_func=exclude_if)
