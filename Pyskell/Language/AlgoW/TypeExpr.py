from abc import abstractmethod, ABCMeta


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

    def get_free_variable(self):
        return self.abstracter.free_type_variable() - self.binder

    def __str__(self):
        return "<{}>.{}".format(", ".join([i for i in self.binder]),
                                str(self.abstracter))


class TVariable(Type):
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Error Initialize Type Variable")
        self.name = name

    def free_type_variable(self):
        return {self.name}

    def __str__(self):
        pass

    def apply_sub(self, sub):
        pass


class TArrow(Type):
    def __init__(self, t1, t2):
        if (not isinstance(t1, Type)) or (not isinstance(t2, Type)):
            raise Exception("Error Initialize Arrow Type")
        self.t1 = t1
        self.t2 = t2

    def free_type_variable(self):
        pass

    def __str__(self):
        pass

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
    def __init__(self, gamma):
        self.gamma = gamma

    def __contains__(self, item):
        return item in self.gamma

    def __getitem__(self, item):
        return self.gamma[item]
