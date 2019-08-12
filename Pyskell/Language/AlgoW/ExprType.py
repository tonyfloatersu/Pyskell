from abc import ABCMeta, abstractmethod
from .Inference import Inference


class Expression(metaclass=ABCMeta):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def get_type(self, type_env, type_inference):
        pass


class EVariable(Expression):
    def __init__(self, name):
        self.name = name

    def show(self):
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

    def show(self):
        return "(\\{} -> {})".format(self.name, self.expr)

    def get_type(self, type_env, type_inference):
        pass


class EApplication(Expression):
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def show(self):
        return "({} {})".format(self.e1.show(), self.e2.show())

    def get_type(self, type_env, type_inference):
        pass


class ELet(Expression):
    def __init__(self, x, e1, e2):
        self.x = x
        self.e1 = e1
        self.e2 = e2

    def show(self):
        return "([{e1} / {x}] {e2})".format(e1=self.e1.show(),
                                            x=self.x,
                                            e2=self.e2.show())

    def get_type(self, type_env, type_inference):
        pass


class ELit(Expression):
    def __init__(self, lit):
        self.lit = lit

    def show(self):
        return self.lit.show()

    def get_type(self, type_env, type_inference):
        pass


class TypeOperator:
    def __init__(self, binder, abstracter):
        self.binder = set(binder)
        self.abstracter = abstracter

    def get_free_variable(self):
        return self.abstracter.get_free_varible() - self.binder


class Type(metaclass=ABCMeta):
    @abstractmethod
    def free_type_variable(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
