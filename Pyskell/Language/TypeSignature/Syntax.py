from .TypedFunction import *
from inspect import isclass


class TS:
    def __init__(self, sig):
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


class Signature:
    def __init__(self, args, constraints):
        self.signature = TypeSignature(constraints, args)

    def __rshift__(self, other):
        other = other.signature if isinstance(other, Signature) else other
        return Signature(self.signature.args + (other,),
                         self.signature.constraints)

    def __rpow__(self, other):
        return TS(self)(other)


class Constraints:
    def __init__(self, constraints=()):
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
