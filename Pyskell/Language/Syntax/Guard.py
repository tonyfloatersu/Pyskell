from Pyskell.Language.Syntax.Basic import Syntax


"""
The structure of guard is similar to the one of Pattern
~(Guard(<expr>)
  | c(<test expr 0>) >> <return value 0>
  | c(<test expr 1>) >> <return value 1>
  .
  .
  .
  | c(<test expr n>) >> <return value n>
  | otherwise >> <backup method>
"""


class GuardUnit(Syntax):
    def __init__(self, fn, ret_v):
        super(GuardUnit, self).__init__("Syntax Error in Guard Unit")
        self.fn = fn
        self.return_val = ret_v


class GuardTest(Syntax):
    def __init__(self, test_fn):
        super(GuardTest, self).__init__("Syntax Error In Guard")
        if not callable(test_fn):
            raise TypeError("Guard Expr Func Not Callable")
        self.__test_fn = test_fn

    def __rshift__(self, other):
        if isinstance(other, GuardTest) or \
           isinstance(other, GuardUnit) or \
           isinstance(other, GuardSyntaxBase):
            raise self.invalid_syntax
        return GuardUnit(self.__test_fn, other)


g = GuardTest
otherwise = g(lambda _: True)


class GuardSyntaxBase(Syntax):
    def __init__(self, value):
        super(GuardSyntaxBase, self).__init__("ERROR IN GUARD SYNTAX")
        self.value = value


class GuardUnmatched(GuardSyntaxBase):
    def __or__(self, other):
        if isinstance(other, GuardTest):
            raise SyntaxError("Guard Expression missing")
        elif not isinstance(other, GuardUnit):
            raise SyntaxError("Guard condition error: {}".format(other))
        elif other.fn(self.value):
            return GuardMatched(other.return_val)
        return GuardUnmatched(self.value)

    def __invert__(self):
        raise TypeError("NO MATCH FOR {}".format(self.value))


class GuardMatched(GuardSyntaxBase):
    def __or__(self, other):
        if not isinstance(other, GuardUnit):
            raise self.invalid_syntax
        return self

    def __invert__(self):
        return self.value


class Guard(GuardUnmatched):
    def __invert__(self):
        raise self.invalid_syntax
