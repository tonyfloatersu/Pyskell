from abc import abstractmethod, ABCMeta


class Type(metaclass=ABCMeta):
    @abstractmethod
    def free_type_variable(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def apply_sub(self, sub):
        pass


class TypeOperator:
    def __init__(self, binder, abstracter):
        self.binder = set(binder)
        self.abstracter = abstracter

    def get_free_variable(self):
        return self.abstracter.get_free_varible() - self.binder

    def __str__(self):
        return "<{}>.{}".format(", ".join([i for i in self.binder]),
                                str(self.abstracter))


class TVariable(Type):
    def __init__(self, name):
        self.name = name

    def free_type_variable(self):
        return {self.name}

    def __repr__(self):
        pass

