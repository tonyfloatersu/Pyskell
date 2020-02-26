from __future__ import annotations
from .Types import TVariable


class Substitution(dict):
    """
    Dict Mapping from TypeVariable -> Type
    """
    def compose(self, oth: 'Substitution'):
        return Substitution(
            {k: v.apply(self) for k, v in oth.items()}.items() | self.items()
        )

    def __str__(self):
        return "{{{}}}".format(
            ", ".join(
                ["{0} : {1}".format(str(k), str(v)) for k, v in self.items()]
            )
        )

    def merge(self, other: Substitution):
        key_intersect = set(self.keys()).intersection(set(other.keys()))
        if all(map(
                lambda v: TVariable(v).apply(self) == TVariable(v).apply(other),
                list(key_intersect))):
            return Substitution(self.items() | other.items())
        raise Exception("Merge Failed")
