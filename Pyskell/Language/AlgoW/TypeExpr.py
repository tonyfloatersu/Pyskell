from abc import abstractmethod, ABCMeta
from functools import reduce


class Type(metaclass=ABCMeta):
    @abstractmethod
    def free_type_variable(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def apply_sub(self, sub):
        pass


class TypeOperator:
    def __init__(self, binder, abstracter):
        for i in binder:
            if not isinstance(i, TVariable):
                raise Exception("Error Initialize Type Operator in binder")
        self.binder = set(binder)
        if not isinstance(abstracter, Type):
            raise Exception("Error Initialize Type Operator in abstracter")
        self.abstracter = abstracter

    def free_type_variable(self):
        return self.abstracter.free_type_variable() - self.binder

    def __str__(self):
        return "<{}>.({})".format(", ".join(map(str, self.binder)),
                                  str(self.abstracter))


class TVariable(Type):
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Error Initialize Type Variable")
        self.name = name

    def free_type_variable(self):
        return {self}

    def __str__(self):
        return self.name

    def apply_sub(self, sub):
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, TVariable) and other.name == self.name


class TArrow(Type):
    def __init__(self, t1, t2):
        if (not isinstance(t1, Type)) or (not isinstance(t2, Type)):
            raise Exception("Error Initialize Arrow Type")
        self.t1 = t1
        self.t2 = t2

    def free_type_variable(self):
        return self.t1.free_type_variable() | self.t2.free_type_variable()

    def __str__(self):
        return "{} -> {}".format(str(self.t1), str(self.t2))

    def apply_sub(self, sub):
        pass


class TCon(Type):
    def __init__(self, py_t):
        self.py_t = py_t

    def free_type_variable(self):
        return {}

    def __str__(self):
        return str(self.py_t)

    def apply_sub(self, sub):
        pass


class TTupleOp(TypeOperator):
    pass


class TListOp(TypeOperator):
    pass


class Context:
    """
    \Gamma: x: \tau
    """
    def __init__(self, gamma):
        if not isinstance(gamma, dict):
            raise Exception("Error Initialize Context Gamma")
        self.gamma = gamma

    def free_type_variables(self):
        return reduce(
            lambda x, y: x | y,
            map(lambda x: x.free_type_variable(), self.gamma.values())
        )

    def __contains__(self, item):
        return item in self.gamma

    def __getitem__(self, item):
        return self.gamma[item]
