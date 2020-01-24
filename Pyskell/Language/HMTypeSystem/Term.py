import abc
import typing


class Term(abc.ABC):
    @abc.abstractmethod
    def free_var(self) -> typing.Set['Var']:
        raise NotImplementedError("free variable not implemented")

    @abc.abstractmethod
    def subst(self, v: 'Var', t: 'Term') -> 'Term':
        raise NotImplementedError("subst method not implemented")


class Var(Term):
    def free_var(self) -> typing.Set['Var']:
        return {self}

    def subst(self, v: 'Var', t: 'Term') -> 'Term':
        return t if v == self else self


class Cons(Term):
    def free_var(self) -> typing.Set['Var']:
        pass

    def subst(self, v: 'Var', t: 'Term') -> 'Term':
        pass


class Mu(Term):
    def free_var(self) -> typing.Set['Var']:
        pass

    def subst(self, v: 'Var', t: 'Term') -> 'Term':
        pass


class TermOps:
    pass
