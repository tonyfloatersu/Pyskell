from abc import ABCMeta, abstractmethod
from .Inference import Inference


class Expression(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if len(other.__dict__) != len(self.__dict__):
            return False
        for k, v in other.__dict__.items():
            if k not in self.__dict__ or self.__dict__[k] != v:
                return False
        return True

    @abstractmethod
    def get_type(self, type_env, type_inference):
        pass


class EVariable(Expression):
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Initialize Syntax Expression Variable Error")
        self.name = name

    def __str__(self):
        return self.name

    def get_type(self, type_env, type_inference):
        if self.name in type_env:
            """
            TOBE implemented
            """
            pass
        raise Exception("Unbound Free Variable: " + self.name)


class EAbstraction(Expression):
    def __init__(self, name, expr):
        if (not isinstance(name, str)) or (not isinstance(expr, Expression)):
            raise Exception("Initialize Syntax Expression Abstraction Error")
        self.name = name
        self.expr = expr

    def __str__(self):
        return "(\\{} -> {})".format(self.name, str(self.expr))

    def get_type(self, type_env, type_inference):
        pass


class EApplication(Expression):
    def __init__(self, expr_func, expr_args):
        self.expr_func = expr_func
        self.expr_args = expr_args

    def __str__(self):
        return "({} {})".format(str(self.expr_func), str(self.expr_args))

    def get_type(self, type_env, type_inference):
        pass


class ELet(Expression):
    def __init__(self, x, e1, e2):
        if (not isinstance(x, str)) or (not isinstance(e1, Expression)) \
                or (not isinstance(e2, Expression)):
            raise Exception("Initialize Syntax Expression Let Error")
        self.x = x
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return "([{0} / {1}] {2})".format(str(self.e1), self.x, str(self.e2))

    def get_type(self, type_env, type_inference):
        pass


class ELiteral(Expression):
    def __init__(self, lit):
        self.lit = lit

    def __str__(self):
        return "lit[{}]".format(str(self.lit))

    def get_type(self, type_env, type_inference):
        pass


class EIf(Expression):
    def __init__(self, cond, e1, e2):
        if (not isinstance(cond, Expression)) or \
            (not isinstance(e1, Expression)) or \
                (not isinstance(e2, Expression)):
            raise Exception("Initialize Syntax Expression If Error")
        self.cond = cond
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return "If {} then {} else {}".format(str(self.cond),
                                              str(self.e1),
                                              str(self.e2))

    def get_type(self, type_env, type_inference):
        pass


class EFixP(Expression):
    def __init__(self, expr):
        if not isinstance(expr, Exception):
            raise Exception("Initialize Syntax Expression Fix Point Error")
        self.expr = expr

    def __str__(self):
        return "fix {}".format(str(self.expr))

    def get_type(self, type_env, type_inference):
        pass


class BinOp:
    @classmethod
    def op_name(cls):
        return cls.__name__

    @classmethod
    def __eq__(cls, other):
        return isinstance(other, BinOp) and other.op_name() == cls.__name__


class Add(BinOp):
    pass


class Sub(BinOp):
    pass


class Mul(BinOp):
    pass


class Eql(BinOp):
    pass


class EOp(Expression):
    def __init__(self, bin_p, e1, e2):
        if (not issubclass(bin_p, BinOp)) or (not isinstance(e1, Expression)) \
                or (not isinstance(e2, Expression)):
            raise Exception("Initialize Syntax Expression BinOperator Error")
        self.binary = bin_p
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return "(Op {} {} {})".format(self.binary.op_name(),
                                      str(self.e1),
                                      str(self.e2))

    def get_type(self, type_env, type_inference):
        pass
