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
    def apply(self, sub):
        pass


class Substitution(dict):
    def compose(self, oth: 'Substitution'):
        return Substitution(
            self.items() | {k: v.apply(self) for k, v in oth.items()}.items()
        )

    def __str__(self):
        return "{{{}}}".format(
            ", ".join(
                ["{0} : {1}".format(str(k), str(v)) for k, v in self.items()]
            )
        )


class TVariable(Type):
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Error Initialize Type Variable")
        self.name = name

    def free_type_variable(self):
        return {self}

    def __str__(self):
        return self.name

    def apply(self, sub: Substitution):
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
        return "{} -> {}".format(
            str(self.t1) if not isinstance(self.t1, TArrow)
            else "({})".format(str(self.t1)),
            str(self.t2)
        )

    def apply(self, sub: Substitution):
        lhs = self.t1.apply(sub)
        rhs = self.t2.apply(sub)
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

    def apply(self, sub: Substitution):
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

    def apply(self, sub: Substitution):
        return TTuple(
            *[ttp.apply(sub) for ttp in self.tuple_types]
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

    def apply(self, sub: Substitution):
        return TList(self.list_type.apply(sub))

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

    def apply(self, sub: Substitution):
        binder_updated = {k for k in self.binder if k not in sub.keys()}
        abstracter_updated = self.abstracter.apply(sub)
        return TypeOperator(binder_updated, abstracter_updated)

    def __str__(self):
        result = str(self.abstracter)
        if len(self.binder) > 0:
            result = "<{}>.".format(", ".join(map(str, self.binder))) + result
        return result

    def instantiation(self):
        return self.abstracter.apply(
            Substitution({
                var: TVariable(glob_infer.new_type_var_name())
                for var in self.binder
            })
        )


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

    def apply(self, sub: Substitution):
        return Context({
            expr: tp.apply(sub)
            for expr, tp in self.gamma.items()
        })

    def __contains__(self, item):
        return item in self.gamma

    def __getitem__(self, item):
        return self.gamma[item]

    def generalization(self, tp):
        if not isinstance(tp, Type):
            raise Exception("Error in Generalization of Type")
        return TypeOperator(
            tp.free_type_variable() - self.free_type_variables(), tp
        )


class Inference:
    def __init__(self):
        self.__next_type_var_id = 0

    def new_type_var_name(self):
        name = 't' + str(self.__next_type_var_id)
        self.__next_type_var_id += 1
        return name

    def unify(self, t0: Type, t1: Type):
        if isinstance(t0, TArrow) and isinstance(t1, TArrow):
            unify_lhs = self.unify(t0.t1, t1.t1)
            unify_rhs = self.unify(t0.t2.apply(unify_lhs),
                                   t1.t2.apply(unify_lhs))
            return unify_rhs.compose(unify_lhs)
        elif isinstance(t0, TVariable):
            return self.bind(t0.name, t1)
        elif isinstance(t1, TVariable):
            return self.bind(t1.name, t0)
        elif isinstance(t0, TCon) and isinstance(t1, TCon) \
                and t0.py_t == t1.py_t:
            return Substitution()
        elif isinstance(t0, TList) and isinstance(t1, TList):
            return self.unify(t0.list_type, t1.list_type)
        elif isinstance(t0, TTuple) and isinstance(t1, TTuple) \
                and len(t0.tuple_types) == len(t1.tuple_types):
            sub_l = self.unify(t0.tuple_types[0], t1.tuple_types[0])
            if len(t0.tuple_types) == 1:
                return sub_l
            t0_tail = TTuple(*(t0.tuple_types[1:]))
            t1_tail = TTuple(*(t1.tuple_types[1:]))
            sub_r = self.unify(t0_tail, t1_tail)
            return sub_r.compose(sub_l)
        raise Exception("Error Unifying {} and {}".format(str(t0), str(t1)))

    @staticmethod
    def bind(name, tp):
        if tp == TVariable(name):
            return Substitution()
        elif TVariable(name) in tp.free_type_variable():
            raise Exception("Infinite type caused by {} and {}"
                            .format(name, str(tp)))
        else:
            return Substitution({TVariable(name): tp})


glob_infer = Inference()
