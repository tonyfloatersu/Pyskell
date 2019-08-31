from .Kinds import Kind, KindFunc
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
    if not hasattr(something, "__kind__"):
        raise "{} does not have __kind__() attr".format(str(something))
    return something.__kind__()


class TypeVariable:
    def __init__(self, name, kind):
        if (not isinstance(name, str)) or (not isinstance(kind, Kind)):
            raise Exception("Error Initialize {}"
                            .format(self.__class__.__name__))
        self.name = name
        self.kind = kind

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.name == other.name) and (self.kind == other.kind)

    def __kind__(self):
        return self.kind


class TypeConstructor:
    def __init__(self, name, kind):
        if not isinstance(kind, Kind):
            raise Exception("Error Initialize {}"
                            .format(self.__class__.__name__))
        self.name = name
        self.kind = kind

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.name == other.name) and (self.kind == other.kind)

    def __kind__(self):
        return self.kind


class TVariable(Type):
    def __init__(self, tpv):
        if not isinstance(tpv, TypeVariable):
            raise Exception("Error Initialize {}"
                            .format(self.__class__.__name__))
        self.tpv = tpv

    def free_type_variable(self):
        return {self.tpv}

    def apply(self, sub):
        return sub[self.tpv] if self.tpv in sub.keys() else self

    def __kind__(self):
        return _kind(self.tpv)


class TConstructor(Type):
    def __init__(self, tco):
        if not isinstance(tco, TypeConstructor):
            raise Exception("Error Initialize {}"
                            .format(self.__class__.__name__))
        self.tco = tco

    def free_type_variable(self):
        return set()

    def apply(self, sub):
        return set()

    def __kind__(self):
        return _kind(self.tco)


class TApplication(Type):
    def __init__(self, t0, t1):
        if (not isinstance(t0, Type)) or (not isinstance(t1, Type)):
            raise Exception("Error Initialize {}"
                            .format(self.__class__.__name__))
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


class TGeneralized(Type):
    def __init__(self, gen_id):
        if not isinstance(gen_id, int):
            raise Exception("Error Initialize {}"
                            .format(self.__class__.__name__))
        self.gen_id = gen_id

    def free_type_variable(self):
        return set()

    def apply(self, sub):
        return self

    def __kind__(self):
        raise Exception("Kind in Type Generalized")


class Infix:
    def __init__(self, f):
        self.f = f

    def __or__(self, other):
        return self.f(other)

    def __ror__(self, other):
        return Infix(lambda x: self.f(other, x))

    def __call__(self, v1, v2):
        return self.f(v1, v2)
