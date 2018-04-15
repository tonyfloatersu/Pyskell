from collections import deque
from Basic import *
from Pyskell.Language.TypeClasses import show


class MatchStackFrame(object):
    def __init__(self, value):
        self.value = value
        self.env_cache = {}
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
        return cls.get_frame().env_cache.get(name, undefined)


"""
The IMPLEMENTATION OF THE PATTERN MATCHING IS NOT THREAD SAFE
"""


class PatternBindingList(Syntax, PatternMatchListBind):
    def __init__(self, head, tail):
        super(PatternBindingList, self).__init__("Error Pattern Matching List")
        self.head = [head]
        self.tail = tail

    def __rxor__(self, other):
        self.head.insert(0, other)
        return self


class PatternBinding(Syntax, PatternMatchBind):
    def __init__(self, name):
        super(PatternBinding, self).__init__("Error in Pattern Matching")
        self.name = name

    def __xor__(self, other):
        if isinstance(other, PatternBindingList):
            return other.__rxor__(self)
        elif isinstance(other, PatternBinding):
            return PatternBindingList(self, other)
        raise TypeError("Error in Pattern Matching Name")

    def __rxor__(self, other):
        return PatternBindingList(other, self)


class LineMatchFromTo(Syntax):
    def __init__(self, is_matched, ret_val):
        super(LineMatchFromTo, self).__init__("Invalid Line Match Error")
        self.is_matched = is_matched
        self.ret_val = ret_val


class LineMatchTest(Syntax):
    def __init__(self, is_matched):
        super(LineMatchTest, self).__init__("Invalid Line Match Error")
        self.is_matched = is_matched

    def __rshift__(self, other):
        return LineMatchFromTo(self.is_matched, other)


class VariableBinding(Syntax):
    def __getattr__(self, item):
        return PatternBinding(item)

    def __call__(self, pattern):
        is_match, env = pattern_match(MatchStack.get_frame().value, pattern)
        if is_match and not MatchStack.get_frame().matched:
            MatchStack.get_frame().env_cache = env
        return LineMatchTest(is_match)


class VariableAccess(Syntax):
    def __getattr__(self, item):
        return MatchStack.get_name(item)


class UnmatchedCase(Syntax):
    def __or__(self, other):
        if other.is_matched:
            MatchStack.get_frame().matched = True
            return MatchedCase(other.ret_val)
        return self

    def __invert__(self):
        val = MatchStack.get_frame().value
        MatchStack.pop()
        if is_builtin_type(val):
            raise RuntimeError("Error in Case Match: {}".format(val))
        else:
            return RuntimeError("Error in Case Match: {}".format(show % val))


class MatchedCase(Syntax):
    def __init__(self, value):
        super(MatchedCase, self).__init__("I dont know why this place is wrong\n"
                                          "But apparently something happened.")
        self.value = value

    def __or__(self, other):
        return self

    def __invert__(self):
        MatchStack.pop()
        return self.value


class CaseOf(UnmatchedCase):
    def __init__(self, value):
        super(CaseOf, self).__init__("Error in CaseOf")
        if isinstance(value, SyntaxUndefined):
            raise TypeError("Undefined for Case Of")
        MatchStack.push(value)


pb = VariableBinding("Syntax error in pattern match")
va = VariableAccess("Syntax error in pattern match")
