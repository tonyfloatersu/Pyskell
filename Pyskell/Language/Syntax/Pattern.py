from Pyskell.Language.PyskellTypeSystem import pattern_match
from collections import deque
from Basic import undefined


class IncompletePMError(Exception):
    pass


class MatchStackFrame(object):
    def __init__(self, value):
        self.value = value
        self.cache = {}
        self.matched = False


class MatchStack(object):
    __stack__ = deque()

    @classmethod
    def push(cls, value):
        cls.__stack__.append(MatchStackFrame(value))

    @classmethod
    def pop(cls):
        cls.__stack__.pop()

    @classmethod
    def get_frame(cls):
        return cls.__stack__[-1]

    @classmethod
    def get_name(cls, name):
        if cls.get_frame().matched:
            return undefined
        return cls.get_frame().cache.get(name, undefined)
