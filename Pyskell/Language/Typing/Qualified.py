from .Types import *


class Predicate(Type):
    def __init__(self, class_name, t):
        if not isinstance(t, Type):
            raise Exception("Initialize Predicate Error")
        self.Type = t
        self.class_name = class_name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.class_name == other.class_name and self.Type == other.Type

    def apply(self, sub):
        pass

    def free_type_variable(self):
        pass

    def __kind__(self):
        pass


class Qualified(Type):
    def __init__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        pass

    def apply(self, sub):
        pass

    def free_type_variable(self):
        pass

    def __kind__(self):
        pass
