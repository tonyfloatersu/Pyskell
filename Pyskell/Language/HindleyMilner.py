from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Set


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
        self.name_ord = None
        self.constraints = set() if constraints is None else constraints
        self.instance = None

    def __lazy_assign(self) -> None:
        if self.name_ord is None:
            self.name_ord = TVariable.var_id
            TVariable.var_id += 1

    @property
    def __name__(self) -> str:
        self.__lazy_assign()
        return 'a' + str(self.name_ord)

    def __repr__(self) -> str:
        self.__lazy_assign()
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


def prune(t: HType):
    if isinstance(t, TVariable) and t.instance is not None:
        temp = prune(t.instance)
        t.instance = temp
        return t.instance
    return t


def fresh(t: HType, non_generic: Set[TVariable]) -> HType:
    memorization: Dict[TVariable, TVariable] = dict()

    def fresh_rec(_t: HType) -> HType:
        tp = prune(_t)
        if isinstance(tp, TVariable):
            if tp not in non_generic:
                if tp not in memorization:
                    memorization[tp] = TVariable()
                return memorization[tp]
            return tp
        elif isinstance(tp, TFunction):
            return TFunction(fresh_rec(tp.types[0]), fresh_rec(tp.types[1]))
        elif isinstance(tp, TList):
            return TList(fresh_rec(tp.types[0]))
        elif isinstance(tp, TTuple):
            return TTuple([fresh_rec(i) for i in tp.types])
        elif isinstance(tp, TOperator):
            return TOperator(tp.name, [fresh_rec(i) for i in tp.types])
        return tp

    return fresh_rec(t)


def type_from_env(name: HAST, gamma_env: Dict[HAST, HType],
                  non_generic: Set[TVariable]) -> HType:
    assert name in gamma_env
    return fresh(gamma_env[name], non_generic)


def expr_type_analyze(expr: HAST, gamma_env: Dict[HAST, HType],
                      non_generic: Set[TVariable] = None) -> HType:

    non_generic = set() if non_generic is None else non_generic

    def fun_var(_expr: HAST) -> HType:
        assert isinstance(_expr, HVariable)
        return type_from_env(_expr.name, gamma_env, non_generic)

    def fun_app(_expr: HAST) -> HType:
        assert isinstance(_expr, HApplication)
        fun_type = type_from_env(_expr.func, gamma_env, non_generic)
        arg_type = type_from_env(_expr.arg, gamma_env, non_generic)
        # TODO unify
        return TVariable()

    def fun_lam(_expr: HAST) -> HType:
        assert isinstance(_expr, HLambda)
        arg_type = TVariable()
        new_non_generic = non_generic.copy()
        new_non_generic.add(arg_type)
        new_gamma_env = gamma_env.copy()
        new_gamma_env[_expr.v] = arg_type
        body_type = expr_type_analyze(_expr.defs, new_gamma_env, non_generic)
        return TFunction(arg_type, body_type)

    def fun_let(_expr: HAST) -> HType:
        assert isinstance(_expr, HLet)
        # TODO
        return TVariable()

    switch_case = {
        HVariable.__name__: fun_var,
        HApplication.__name__: fun_app,
        HLambda.__name__: fun_lam,
        HLet.__name__: fun_let
    }

    return switch_case[type(expr).__name__](expr)
