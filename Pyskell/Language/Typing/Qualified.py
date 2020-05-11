from __future__ import annotations
from typing import List
from .Types import *
from functools import reduce
from operator import or_


class Predicate(Type):
    def __init__(self, class_name: str, t: Type):
        self.Type = t
        self.class_name = class_name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.class_name == other.class_name and self.Type == other.Type

    def apply(self, sub):
        return Predicate(self.class_name, self.Type.apply(sub))

    def free_type_variable(self):
        return self.Type.free_type_variable()

    def __hash__(self):
        return hash((self.Type, self.class_name))

    def __kind__(self):
        pass


class Qualified:
    def __init__(self, predicates: List[Predicate], t: Type):
        self.predicates = predicates
        self.Type = t

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return set(self.predicates) == set(other.predicates) and \
            self.Type == other.Type

    def apply(self, sub):
        n_predicates = [i.apply(sub) for i in self.predicates]
        return Qualified(n_predicates, self.Type.apply(sub))

    def free_type_variable(self):
        return reduce(or_, self.predicates) | self.Type.free_type_variable()
