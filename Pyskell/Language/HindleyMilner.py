from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class HType(ABC):
    @property
    @abstractmethod
    def __name__(self) -> str: ...

    @abstractmethod
    def __repr__(self) -> str:
        return self.__name__


def show_type(something):
    if isinstance(something, str):
        return something
    return something.__name__


class TVariable(HType):
    var_id = 0

    def __init__(self, constraints={}):
        self.name_ord = TVariable.var_id
        self.name_id = 'a' + str(TVariable.var_id)
        TVariable.var_id += 1
        self.constraints = constraints
        self.instance = None

    @property
    def __name__(self) -> str:
        return self.name_id

    def __repr__(self) -> str:
        return "TypeVariable({})".format(self.name_ord)


class TOperator(HType):
    def __init__(self, name, types: List[HType]):
        self.name = name
        self.types = types

    @property
    def __name__(self) -> str:
        if len(self.types) == 0:
            return show_type(self.name)
        return "({0} {1})".format(show_type(self.name),
                                  ' '.join(*map(show_type, self.types)))


class TFunction(TOperator):
    def __init__(self, from_T: HType, to_T: HType) -> None:
        super().__init__("->", [from_T, to_T])

    @property
    def __name__(self) -> str:
        return "({1} {0} {2})".format(show_type(self.name),
                                      show_type(self.types[0]),
                                      show_type(self.types[1]))


class TList(TOperator):
    def __init__(self, in_T: HType):
        super().__init__("[]", [in_T])

    @property
    def __name__(self) -> str:
        return "[{}]".format(show_type(self.types[0]))


class TTuple(TOperator):
    def __init__(self, in_Ts: List[HType]):
        super().__init__("()", in_Ts)

    @property
    def __name__(self) -> str:
        return "({})".format(", ".join(*map(show_type, self.types)))
