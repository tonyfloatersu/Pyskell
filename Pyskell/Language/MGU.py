from .Types import *
from .Types import _kind
from .Subst import Substitution
from .Qualified import Predicate


class __MostGeneralizeUnifier:
    def __init__(self):
        pass

    def most_generalized_unifier(self, t0: Type, t1: Type) -> Substitution:
        if isinstance(t0, TApplication) and isinstance(t1, TApplication):
            s0 = self.most_generalized_unifier(t0.t0, t1.t0)
            s1 = self.most_generalized_unifier(t0.t1.apply(s0), t1.t1.apply(s0))
            return s1.compose(s0)
        elif isinstance(t0, TVariable):
            return self.var_bind(t0.tpv, t1)
        elif isinstance(t1, TVariable):
            return self.var_bind(t1.tpv, t0)
        elif isinstance(t0, TConstructor) and isinstance(t1, TConstructor):
            if t0.tco == t1.tco:
                return Substitution()
        elif isinstance(t0, Predicate) and isinstance(t1, Predicate):
            if t0.class_name == t1.class_name:
                return self.most_generalized_unifier(t0.Type, t1.Type)
        raise Exception("Fail in Unification")

    @staticmethod
    def var_bind(u, t):
        if t == TVariable(u):
            return Substitution()
        elif u in t.free_type_variable():
            raise Exception("Occur in Type Check Fail")
        elif _kind(u) != _kind(t):
            raise Exception("Kind Check Match Fail")
        else:
            return Substitution({u: t})

    def match(self, u: Type, t: Type) -> Substitution:
        if isinstance(u, TApplication) and isinstance(t, TApplication):
            s0 = self.most_generalized_unifier(u.t0, t.t0)
            s1 = self.most_generalized_unifier(u.t1, t.t1)
            return s1.merge(s0)
        elif isinstance(u, TVariable):
            if u.tpv.__kind__() == t.__kind__():
                return Substitution({u: t})
        elif isinstance(u, TConstructor) and isinstance(t, TConstructor):
            if u.tco == t.tco:
                return Substitution()
        elif isinstance(u, Predicate) and isinstance(t, Predicate):
            if u.class_name == t.class_name:
                return self.most_generalized_unifier(u.Type, t.Type)
        raise Exception("Fail to match")


glob_mgu = __MostGeneralizeUnifier()
