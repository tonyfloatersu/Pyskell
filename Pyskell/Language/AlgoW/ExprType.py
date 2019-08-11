from abc import ABCMeta, abstractmethod


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
    def show(self):
        pass

    def get_type(self, type_env, type_inference):
        pass


class ELet(Expression):
    def show(self):
        pass

    def get_type(self, type_env, type_inference):
        pass


class TypeOperator:
    pass


class Type(metaclass=ABCMeta):
    @abstractmethod
    def free_type_variable(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
