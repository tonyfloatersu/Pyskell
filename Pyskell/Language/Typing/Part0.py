from __future__ import annotations
from functools import reduce
from operator import or_
from typing import List
import abc


class Kind(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return str(self) == str(other)


class Star(Kind):
    def __init__(self):
        pass

    def __str__(self):
        return "*"


class KFun(Kind):
    def __init__(self, k0, k1):
        self.k0 = k0
        self.k1 = k1

    def __str__(self):
        return "{} -> {}".format(
            str(self.k0) if not isinstance(self.k0, KFun)
            else "({})".format(str(self.k0)),
            str(self.k1)
        )


class KConstraint(Kind):
    def __init__(self):
        pass

    def __str__(self):
        return "Constraint"


class Type(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def free_type_variable(self):
        pass

    @abc.abstractmethod
    def apply(self, sub):
        pass

    @abc.abstractmethod
    def __kind__(self):
        pass


def _kind(something):
    if not hasattr(something, "__kind__"):
        raise "{} does not have __kind__() attr".format(str(something))
    return something.__kind__()


class TyVar:
    def __init__(self, name: str, kind: Kind):
        self.name = name
        self.kind = kind

    def __eq__(self, other):
        return isinstance(other, TyVar) \
            and self.name == other.name and self.kind == other.kind

    def __kind__(self):
        return self.kind

    def __hash__(self):
        return hash((self.name, self.kind))


class TyCon:
    def __init__(self, name: str, kind: Kind):
        self.name = name
        self.kind = kind

    def __eq__(self, other):
        return isinstance(other, TyCon) \
            and self.name == other.name and self.kind == other.kind

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
    def __init__(self, t0, t1):
        self.t0 = t0
        self.t1 = t1

    def free_type_variable(self):
        return self.t0.free_type_variable() | self.t1.free_type_variable()

    def apply(self, sub):
        return TApplication(self.t0.apply(sub),
                            self.t1.apply(sub))

    def __kind__(self):
        if not isinstance(_kind(self.t0), KFun):
            raise Exception("t0 has kind {}".format(str(_kind(self.t0))))
        return _kind(self.t0).k1

    def __eq__(self, other):
        return isinstance(other, TApplication) \
            and self.t0 == other.t0 and self.t1 == other.t1

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
        raise Exception("Kind in Type Generalized Undefined")

    def __eq__(self, other):
        return isinstance(other, TGeneralized) and other.gen_id == self.gen_id


class Substitution(dict):
    def compose(self, oth: Substitution):
        return Substitution(
            {k: v.apply(self) for k, v in oth.items()}.items() | self.items()
        )

    def __str__(self):
        return "{{{}}}".format(
            ", ".join(
                ["{0} : {1}".format(str(k), str(v)) for k, v in self.items()]
            )
        )

    def merge(self, other: Substitution):
        key_intersect = set(self.keys()).intersection(set(other.keys()))
        if all(map(
                lambda v: TVariable(v).apply(self) == TVariable(v).apply(other),
                list(key_intersect))):
            return Substitution(self.items() | other.items())
        raise Exception("Merge Failed")


class Predicate(Type):
    def __init__(self, class_name: str, t: Type):
        self.Type = t
        self.class_name = class_name

    def __eq__(self, other):
        return isinstance(other, Predicate) \
            and self.class_name == other.class_name and self.Type == other.Type

    def apply(self, sub):
        return Predicate(self.class_name, self.Type.apply(sub))

    def free_type_variable(self):
        return self.Type.free_type_variable()

    def __hash__(self):
        return hash((self.Type, self.class_name))

    def __kind__(self):
        raise Exception("Kind in Predicate")


class Qualified(Type):
    def __init__(self, predicates: List[Predicate], t: Type):
        self.predicates = predicates
        self.Type = t

    def __eq__(self, other):
        return isinstance(other, Qualified) \
            and set(self.predicates) == set(other.predicates) \
            and self.Type == other.Type

    def apply(self, sub):
        n_predicates = [i.apply(sub) for i in self.predicates]
        return Qualified(n_predicates, self.Type.apply(sub))

    def free_type_variable(self):
        return self.Type.free_type_variable() | reduce(or_, self.predicates)

    def __kind__(self):
        raise Exception("Kind in Qualified")


def most_generalized_unifier(t0: Type, t1: Type) -> Substitution:
    if isinstance(t0, TApplication) and isinstance(t1, TApplication):
        s0 = most_generalized_unifier(t0.t0, t1.t0)
        s1 = most_generalized_unifier(t0.t1.apply(s0), t1.t1.apply(s0))
        return s1.compose(s0)
    elif isinstance(t0, TVariable):
        return var_bind(t0.tpv, t1)
    elif isinstance(t1, TVariable):
        return var_bind(t1.tpv, t0)
    elif isinstance(t0, TConstructor) and isinstance(t1, TConstructor):
        if t0.tco == t1.tco:
            return Substitution()
    elif isinstance(t0, Predicate) and isinstance(t1, Predicate):
        if t0.class_name == t1.class_name:
            return most_generalized_unifier(t0.Type, t1.Type)
    raise Exception("Fail in Unification")


def var_bind(u, t):
    if t == TVariable(u):
        return Substitution()
    elif u in t.free_type_variable():
        raise Exception("Occur in Type Check Fail")
    elif _kind(u) != _kind(t):
        raise Exception("Kind Check Match Fail")
    else:
        return Substitution({u: t})


def match(u: Type, t: Type) -> Substitution:
    if isinstance(u, TApplication) and isinstance(t, TApplication):
        s0 = most_generalized_unifier(u.t0, t.t0)
        s1 = most_generalized_unifier(u.t1, t.t1)
        return s1.merge(s0)
    elif isinstance(u, TVariable):
        if _kind(u.tpv) == _kind(t):
            return Substitution({u: t})
    elif isinstance(u, TConstructor) and isinstance(t, TConstructor):
        if u.tco == t.tco:
            return Substitution()
    elif isinstance(u, Predicate) and isinstance(t, Predicate):
        if u.class_name == t.class_name:
            return most_generalized_unifier(u.Type, t.Type)
    raise Exception("Fail to match")
