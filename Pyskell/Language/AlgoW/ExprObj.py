from abc import ABCMeta, abstractmethod
from .Inference import Inference


class Expression(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_type(self, type_env, type_inference):
        pass


class EVariable(Expression):
    def __init__(self, name):
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
        self.name = name
        self.expr = expr

    def __str__(self):
        return "(\\{} -> {})".format(str(self.name), str(self.expr))

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
        self.x = x
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return "([{0} / {1}] {2})".format(str(self.e1), self.x, str(self.e2))

    def get_type(self, type_env, type_inference):
        pass
