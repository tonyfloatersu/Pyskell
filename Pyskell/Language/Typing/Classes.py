from __future__ import annotations
from .Qualified import *


class InstanceDeclaration:
    def __init__(self, qual: Qualified, pred: Predicate):
        self.qual = qual
        self.pred = pred


class TypeClassData:
    def __init__(self, superclass: List[str], insts: InstanceDeclaration):
        self.superclass = superclass
        self.inst = insts
