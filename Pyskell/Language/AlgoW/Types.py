from .Kinds import star, k_constraint, KindFunc, Kind
from abc import ABCMeta, abstractmethod
from .Infix import Infix


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

    @staticmethod
    @abstractmethod
    def __kind__():
        pass


"""
data Type  = TVar Tyvar | TCon Tycon | TAp Type Type | TGen Int
             deriving Eq

data Tyvar = Tyvar Id Kind
             deriving Eq

data Tycon = Tycon Id Kind
             deriving Eq
"""


class TypeVariable:
    def __init__(self, name, kind):
        if (not isinstance(name, str)) or (not isinstance(kind, Kind)):
            raise Exception("Error Initialize TypeVariable")
        self.name = name
        self.kind = kind


class TypeConstraint:
    def __init__(self, name, kind):
        if not isinstance(kind, Kind):
            raise Exception("Error Initialize TypeConstraint")
        self.name = name
        self.kind = kind


class TVariable(Type):
    def __init__(self, tpv):
        if not isinstance(tpv, TypeVariable):
            raise Exception("Error Initialize TVariable")
        self.tpv = tpv

    def free_type_variable(self):
        pass

    def __str__(self):
        pass

    def apply(self, sub):
        pass

    @staticmethod
    def __kind__():
        pass


class TConstraint(Type):
    def __init__(self, tco):
        if not isinstance(tco, TypeConstraint):
            raise Exception("Error Initialize TVariable")
        self.tco = tco

    def free_type_variable(self):
        pass

    def __str__(self):
        pass

    def apply(self, sub):
        pass

    @staticmethod
    def __kind__():
        pass
