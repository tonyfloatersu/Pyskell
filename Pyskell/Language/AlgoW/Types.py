from .Kinds import Kind, KindFunc
from abc import ABCMeta, abstractmethod


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
        return self.tpv

    def __str__(self):
        return self.tpv.name

    def apply(self, sub):
        pass

    def __kind__(self):
        return _kind(self.tpv)


class TConstraint(Type):
    def __init__(self, tco):
        if not isinstance(tco, TypeConstructor):
            raise Exception("Error Initialize {}"
                            .format(self.__class__.__name__))
        self.tco = tco

    def free_type_variable(self):
        pass

    def __str__(self):
        pass

    def apply(self, sub):
        pass

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
        pass

    def __str__(self):
        pass

    def apply(self, sub):
        pass

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
        pass

    def __str__(self):
        pass

    def apply(self, sub):
        pass

    def __kind__(self):
        pass
