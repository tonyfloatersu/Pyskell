from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class HType(ABC):
    @property
    @abstractmethod
    def __name__(self) -> str: ...

    def __repr__(self) -> str: return self.__name__


def show_type(something):
    if isinstance(something, str):
        return something
    return something.__name__


class TVariable(HType):
    var_id = 0

    def __init__(self, constraints=None):
        self.name_ord = TVariable.var_id
        TVariable.var_id += 1
        self.constraints = set() if constraints is None else constraints
        self.instance = None

    @property
    def __name__(self) -> str: return 'a' + str(self.name_ord)

    def __repr__(self) -> str: return "TypeVariable({})".format(self.name_ord)


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
    def __init__(self, from_t: HType, to_t: HType):
        super().__init__("->", [from_t, to_t])

    @property
    def __name__(self) -> str:
        return "({1} {0} {2})".format(show_type(self.name),
                                      show_type(self.types[0]),
                                      show_type(self.types[1]))


class TList(TOperator):
    def __init__(self, in_t: HType): super().__init__("[]", [in_t])

    @property
    def __name__(self) -> str:
        return "[{}]".format(show_type(self.types[0]))


class TTuple(TOperator):
    def __init__(self, in_ts: List[HType]): super().__init__("()", in_ts)

    @property
    def __name__(self) -> str:
        return "({})".format(", ".join(*map(show_type, self.types)))


class HAST(object):
    def __repr__(self) -> str: ...


class HVariable(HAST):
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str: return str(self.name)


class HLambda(HAST):
    def __init__(self, v: HAST, defs: HAST):
        self.v = v
        self.defs = defs

    def __repr__(self) -> str: return "(\\{0} -> {1})".format(self.v, self.defs)


class HApplication(HAST):
    def __init__(self, func: HAST, arg: HAST):
        self.func = func
        self.arg = arg

    def __repr__(self) -> str: return "({0} {1})".format(self.func, self.arg)


class HLet(HAST):
    def __init__(self, var: HAST, defs: HAST, expr: HAST):
        self.var = var
        self.defs = defs
        self.expr = expr

    def __repr__(self) -> str:
        return "(let {0} = {1} in {2})".format(self.var, self.defs, self.expr)


class MostGeneralUnifier:
    def __init__(self) -> None:
        pass
