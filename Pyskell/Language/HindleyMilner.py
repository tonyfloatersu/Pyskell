from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set


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
        self.instance: Optional[HType] = None

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


def prune(t: HType) -> HType:
    if isinstance(t, TVariable) and t.instance is not None:
        t.instance = prune(t.instance)
        return t.instance
    return t


def occurs_in(pruned_t: HType, t2: HType) -> bool:
    pruned_t2 = prune(t2)
    if pruned_t2 == pruned_t:
        return True
    elif isinstance(pruned_t2, TOperator):
        return any(occurs_in(pruned_t, t) for t in pruned_t2.types)
    return False


def fresh(t: HType, non_generic: Set[TVariable]) -> HType:
    memorization: Dict[TVariable, TVariable] = dict()

    def fresh_rec(_t: HType) -> HType:
        tp = prune(_t)
        if isinstance(tp, TVariable):
            if not any(occurs_in(tp, non_gt) for non_gt in non_generic):
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
    if name not in gamma_env:
        raise TypeError("{} not in gamma_env".format(name))
    return fresh(gamma_env[name], non_generic)


def unify_type_variable(ptv1: TVariable, pt2: HType) -> None:
    if ptv1 == pt2:
        return

    if occurs_in(ptv1, pt2):
        raise TypeError("Recursive Unification")
    if isinstance(pt2, TVariable):
        ptv1.constraints |= pt2.constraints
        pt2.constraints |= ptv1.constraints
    ptv1.instance = pt2


def unify(t1: HType, t2: HType) -> None:
    pt1, pt2 = prune(t1), prune(t2)
    if isinstance(pt1, TVariable):
        unify_type_variable(pt1, pt2)
    elif isinstance(pt2, TVariable) and isinstance(pt1, TOperator):
        unify_type_variable(pt2, pt1)
    else:
        assert isinstance(pt1, TOperator) and isinstance(pt2, TOperator)
        # TODO poly higher-kind type
        if len(pt1.types) != len(pt2.types) or pt1.name != pt2.name:
            raise TypeError("Unable to match type {} and {}".format(pt1, pt2))
        for pt1t, pt2t in zip(pt1.types, pt2.types):
            unify(pt1t, pt2t)


def expr_type_analyze(expr: HAST, gamma_env: Dict[HAST, HType],
                      non_generic: Set[TVariable] = None) -> HType:

    non_generic = set() if non_generic is None else non_generic

    def rep_env_non_gen(_gamma_env: Dict[HAST, HType],
                        _non_generic: Set[TVariable],
                        _expr: HAST, _expr_tv: TVariable):
        new_non_generic = _non_generic.copy()
        new_gamma_env = _gamma_env.copy()
        new_non_generic.add(_expr_tv)
        new_gamma_env[_expr] = _expr_tv
        return new_non_generic, new_gamma_env

    def fun_var(_expr: HAST) -> HType:
        assert isinstance(_expr, HVariable)
        return type_from_env(_expr.name, gamma_env, non_generic)

    def fun_app(_expr: HAST) -> HType:
        assert isinstance(_expr, HApplication)
        fun_type = type_from_env(_expr.func, gamma_env, non_generic)
        arg_type = type_from_env(_expr.arg, gamma_env, non_generic)
        result_t = TVariable()
        unify(TFunction(arg_type, result_t), fun_type)
        return result_t

    def fun_lam(_expr: HAST) -> HType:
        assert isinstance(_expr, HLambda)
        arg_type = TVariable()
        new_non_generic, new_env = \
            rep_env_non_gen(gamma_env, non_generic, _expr.v, arg_type)
        body_type = expr_type_analyze(_expr.defs, new_env, new_non_generic)
        return TFunction(arg_type, body_type)

    def fun_let(_expr: HAST) -> HType:
        assert isinstance(_expr, HLet)
        arg_type = TVariable()
        new_non_generic, new_env = \
            rep_env_non_gen(gamma_env, non_generic, _expr.var, arg_type)
        defs_t = expr_type_analyze(_expr.defs, new_env, new_non_generic)
        unify(arg_type, defs_t)
        return expr_type_analyze(_expr.expr, new_env, non_generic)

    switch_case = {
        HVariable.__name__: fun_var,
        HApplication.__name__: fun_app,
        HLambda.__name__: fun_lam,
        HLet.__name__: fun_let
    }

    return switch_case[type(expr).__name__](expr)
