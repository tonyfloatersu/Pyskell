from __future__ import annotations
from .Kinds import Kind, KindFunc, star, k_constraint
from abc import ABCMeta, abstractmethod


class Type(metaclass=ABCMeta):
    @abstractmethod
    def free_type_variable(self):
        pass

    @abstractmethod
    def apply(self, sub):
        pass

    @abstractmethod
    def __kind__(self):
        pass


def _kind(something):
    """
    Immitation of `:k` in Haskell GHCi
    """
    if not hasattr(something, "__kind__"):
        raise "{} does not have __kind__() attr".format(str(something))
    return something.__kind__()


class TyVar:
    def __init__(self, name: str, kind: Kind):
        self.name = name
        self.kind = kind

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.name == other.name) and (self.kind == other.kind)

    def __kind__(self) -> Kind:
        return self.kind

    def __hash__(self):
        return hash((self.name, self.kind))


class TyCon:
    def __init__(self, name: str, kind: Kind):
        self.name = name
        self.kind = kind

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.name == other.name) and (self.kind == other.kind)

    def __kind__(self):
        return self.kind

    def __hash__(self):
        return hash((self.name, self.kind))


class TVariable(Type):
    def __init__(self, tpv: TyVar):
        self.tpv = tpv

    def free_type_variable(self):
        return {self.tpv}

    def apply(self, sub):
        return sub[self.tpv] if self.tpv in sub.keys() else self

    def __kind__(self):
        return _kind(self.tpv)

    def __eq__(self, other):
        if not isinstance(other, TVariable):
            return False
        return self.tpv == other.tpv

    def __hash__(self):
        return hash(self.tpv)


class TConstructor(Type):
    def __init__(self, tco: TyCon):
        self.tco = tco

    def free_type_variable(self):
        return set()

    def apply(self, sub):
        return set()

    def __kind__(self):
        return _kind(self.tco)

    def __eq__(self, other):
        if not isinstance(other, TConstructor):
            return False
        return self.tco == other.tco

    def __hash__(self):
        return hash(self.tco)


class TApplication(Type):
    def __init__(self, t0: Type, t1: Type):
        self.t0 = t0
        self.t1 = t1

    def free_type_variable(self):
        return self.t0.free_type_variable() | self.t1.free_type_variable()

    def apply(self, sub):
        return TApplication(self.t0.apply(sub),
                            self.t1.apply(sub))

    def __kind__(self):
        if not isinstance(_kind(self.t0), KindFunc):
            raise Exception("t0 has kind {}".format(str(_kind(self.t0))))
        return _kind(self.t0).k1

    def __eq__(self, other):
        if not isinstance(other, TApplication):
            return False
        return (self.t0 == other.t0) and (self.t1 == other.t1)

    def __hash__(self):
        return hash((self.t0, self.t1))


class TGeneralized(Type):
    def __init__(self, gen_id: int):
        self.gen_id = gen_id

    def free_type_variable(self):
        return set()

    def apply(self, sub):
        return self

    def __kind__(self):
        raise Exception("Kind in Type Generalized")


def t_app(a, b):
    if (not isinstance(a, Type)) or (not isinstance(b, Type)):
        raise Exception("Type Application Error with No Type Arg")
    if not isinstance(_kind(a), KindFunc):
        raise Exception("Type Application Error with Constructor no arity")
    if a.__kind__().k0 != b.__kind__():
        raise Exception("Type Application Error with App Arg Kind Conflict")
    return TApplication(a, b)


# BELOW ARE SOME EXAMPLES, MAYBE THEY WILL BE USED


class Rank0TypeConstructor(TyCon):
    def __init__(self, name):
        super(Rank0TypeConstructor, self).__init__(name, star)


class Rank1TypeConstructor(TyCon):
    def __init__(self, name, arg_num):
        new_kind = star
        for _ in range(0, arg_num):
            new_kind = KindFunc(star, new_kind)
        super(Rank1TypeConstructor, self).__init__(name, new_kind)


class ListTypeConstructor(Rank1TypeConstructor):
    def __init__(self):
        super(ListTypeConstructor, self).__init__(list, 1)


def t_list(a):
    if not isinstance(a, Type):
        raise Exception("List Type Initialize Error with No Type Arg")
    return t_app(TConstructor(ListTypeConstructor()), a)


class ArrowTypeConstructor(Rank1TypeConstructor):
    def __init__(self):
        super(ArrowTypeConstructor, self).__init__("->", 2)


def t_arr(a, b):
    if (not isinstance(a, Type)) or (not isinstance(b, Type)):
        raise Exception("Arrow Type Initialize Error with No Type Arg")
    return t_app(t_app(TConstructor(ArrowTypeConstructor()), a), b)


class TupleTypeConstructor(Rank1TypeConstructor):
    def __init__(self, num):
        if num < 2:
            raise Exception("Tuple Type Construct smaller than 2")
        super(TupleTypeConstructor, self).__init__(tuple, num)


def t_tuple(*args):
    t_con = TConstructor(TupleTypeConstructor(len(args)))
    for arg in args:
        t_con = t_app(t_con, arg)
    return t_con


"""
k constraint will be used if type class are applied
"""
