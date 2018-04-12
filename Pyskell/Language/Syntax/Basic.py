from Pyskell.Language.PyskellTypeSystem import *
from inspect import isclass
from collections import defaultdict


def ct(obj):
    return str(type_of(obj))


__magic_methods__ = ["__{}__".format(s) for s in {
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
        replace_magic_methods(Syntax, lambda x, *a: x.__raise())

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


class TS(Syntax):
    """Type Signature"""
    def __init__(self, sig):
        super(TS, self).__init__("Syntax Error in Type Signature")
        if not isinstance(sig, Signature):
            raise SyntaxError("Signature expected in TS() found {}"
                              .format(sig))
        elif len(sig.signature.args) < 2:
            raise SyntaxError("Type Signature Argument Not Enough")
        self.signature = sig.signature

    def __call__(self, fn):
        func_args = type_sig_build(self.signature)
        func_type = make_func_type(func_args)
        return TypedFunction(fn, func_args, func_type)


class Signature(Syntax):
    def __init__(self, args, constraints):
        super(Signature, self).__init__("Syntax Error in Type Signature")
        self.signature = TypeSignature(constraints, args)

    def __rshift__(self, other):
        other = other.signature if isinstance(other, Signature) else other
        return Signature(self.signature.args + (other,),
                         self.signature.constraints)

    def __rpow__(self, other):
        return TS(self)(other)


class Constraints(Syntax):
    def __init__(self, constraints=()):
        super(Constraints, self).__init__("Syntax Error in Type Signature")
        self.constraints = defaultdict(list)
        if len(constraints) > 0:
            if isinstance(constraints[0], tuple):
                for con in constraints:
                    self.__add_tc_constraints(con)
            else:
                self.__add_tc_constraints(constraints)

    def __add_tc_constraints(self, con):
        if len(con) != 2 or not isinstance(con, tuple):
            raise SyntaxError("Invalid Type-class Constraint: {}"
                              .format(str(con)))
        if not isinstance(con[1], str):
            raise SyntaxError("{} is not type variable".format(con[1]))
        if not (isclass(con[0]) and issubclass(con[0], TypeClass)):
            raise SyntaxError("{} is not a type-class".format(con[0]))
        self.constraints[con[1]].append(con[0])
        return

    def __getitem__(self, item):
        return Constraints(item)

    def __div__(self, other):
        return Signature((), self.constraints) >> other

    def __truediv__(self, other):
        return self.__div__(other)


C = Constraints()
py_func = PythonFunctionType


class SyntaxUndefined(Undefined):
    pass


replace_magic_methods(SyntaxUndefined, lambda *x: Undefined())
undefined = SyntaxUndefined()


def t(type_constructor, *parameters):
    if issubclass(type_constructor, ADT) and isclass(type_constructor) and \
       len(type_constructor.__parameters__) != len(parameters):
        raise TypeError("Incorrect number of type parameter {}"
                        .format(type_constructor.__name__))
    parameters = [i.signature if isinstance(i, Signature) else i
                  for i in parameters]
    return TypeSignatureHigherKind(type_constructor, parameters)


def typify_py_func(fn, high=None):
    if not is_py_func_type(fn):
        raise TypeError("Provided not Python Function Type")
    type_name_list = ["a" + str(i) for i in range(fn.func_code.co_argcount + 1)]
    if high is not None:
        type_name_list[-1] = high(type_name_list[-1])
    return TS(Signature(type_name_list, []))
