from HMTypeSystem import *
from PyskellTypeSystem import *
from inspect import isclass


def _t(obj):
    return str(type_of(obj))


def _q(quit_status=None):
    if quit_status is None:
        quit()
    else:
        quit(quit_status)


__magic_methods__ = ["__%s__" % s for s in {
    "len", "getitem", "setitem", "delitem", "iter", "reversed", "contains",
    "missing", "delattr", "call", "enter", "exit", "eq", "ne", "gt", "lt",
    "ge", "le", "pos", "neg", "abs", "invert", "round", "floor", "ceil",
    "trunc", "add", "sub", "mul", "div", "truediv", "floordiv", "mod",
    "divmod", "pow", "lshift", "rshift", "or", "and", "xor", "radd", "rsub",
    "rmul", "rdiv", "rtruediv", "rfloordiv", "rmod", "rdivmod", "rpow",
    "rlshift", "rrshift", "ror", "rand", "rxor", "isub", "imul", "ifloordiv",
    "idiv", "imod", "idivmod", "irpow", "ilshift", "irshift", "ior", "iand",
    "ixor", "nonzero"}]


def replace_magic_methods(some_class, fn):
    for attr in __magic_methods__:
        setattr(some_class, attr, fn)
    return


class Syntax(object):
    def __init__(self, error_message):
        self.__syntax_error_message = error_message
        self.invalid_syntax = SyntaxError(self.__syntax_error_message)
        replace_magic_methods(Syntax, lambda x, _: self.__raise())

    def __raise(self):
        raise self.invalid_syntax


class Instance(Syntax):
    def __init__(self, type_class, some_class):
        super(Instance, self).__init__("Instance Error")
        if not (isclass(type_class) and issubclass(type_class, TypeClass)):
            raise TypeError("{} is not a type-class".format(type_class))
        self.type_class = type_class
        self.cls = some_class

    def where(self, **kwargs):
        self.type_class.make_instance(self.cls, **kwargs)


class Constraints(Syntax):
    def __init__(self, constraints=()):
        super(Constraints, self).__init__("Syntax Error in Type Signature")

    def __add_tc_constraints(self, con):
        pass

    def __getitem__(self, item):
        return Constraints(item)

    def __div__(self, other):
        pass

    def __truediv__(self, other):
        return self.__div__(other)
