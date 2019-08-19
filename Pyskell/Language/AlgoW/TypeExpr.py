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
    def subst(self, sub):
        pass


class TVariable(Type):
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Error Initialize Type Variable")
        self.name = name

    def free_type_variable(self):
        return {self}

    def __str__(self):
        return self.name

    def subst(self, sub: dict):
        if self in sub.keys():
            return sub[self]
        return self

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

    def subst(self, sub: dict):
        lhs = self.t1.subst(sub)
        rhs = self.t2.subst(sub)
        return TArrow(lhs, rhs)

    def __hash__(self):
        return hash((self.t1, self.t2))

    def __eq__(self, other):
        return isinstance(other, TArrow) \
            and other.t1 == self.t1 and other.t2 == self.t2


class TCon(Type):
    def __init__(self, py_t):
        self.py_t = py_t

    def free_type_variable(self):
        return set()

    def __str__(self):
        if isinstance(self.py_t, type):
            return self.py_t.__name__
        return str(self.py_t)

    def subst(self, sub: dict):
        return self

    def __hash__(self):
        return hash(self.py_t)

    def __eq__(self, other):
        return isinstance(other, TCon) and other.py_t == self.py_t


class TTuple(Type):
    def __init__(self, *tuple_types):
        for some_tp in tuple_types:
            if not isinstance(some_tp, Type):
                raise Exception("Error Initialize Tuple Type")
        self.tuple_types = tuple(tuple_types)

    def __str__(self):
        return "({})".format(", ".join(map(str, self.tuple_types)))

    def free_type_variable(self):
        return reduce(
            lambda x, y: x | y,
            map(lambda x: x.free_type_variable(), self.tuple_types)
        )

    def subst(self, sub: dict):
        return TTuple(
            *[ttp.subst(sub) for ttp in self.tuple_types]
        )

    def __hash__(self):
        return hash(self.tuple_types)

    def __eq__(self, other):
        return isinstance(other, TTuple) \
            and self.tuple_types == other.tuple_types


class TList(Type):
    def __init__(self, type_of_list):
        if not isinstance(type_of_list, Type):
            raise Exception("Error Initialize List Type Operator")
        self.list_type = type_of_list

    def __str__(self):
        return "[{}]".format(str(self.list_type))

    def free_type_variable(self):
        return self.list_type.free_type_variable()

    def subst(self, sub: dict):
        return TList(self.list_type.subst(sub))

    def __hash__(self):
        return hash(self.list_type)

    def __eq__(self, other):
        return isinstance(other, TList) and other.list_type == self.list_type


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

    def subst(self, sub: dict):
        binder_updated = {k for k in self.binder if k not in sub.keys()}
        abstracter_updated = self.abstracter.subst(sub)
        return TypeOperator(binder_updated, abstracter_updated)

    def __str__(self):
        result = str(self.abstracter)
        if len(self.binder) > 0:
            result = "<{}>.".format(", ".join(map(str, self.binder))) + result
        return result


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

    def subst(self, sub: dict):
        return Context({
            expr: tp.subst(sub)
            for expr, tp in self.gamma.items()
        })

    def __contains__(self, item):
        return item in self.gamma

    def __getitem__(self, item):
        return self.gamma[item]
