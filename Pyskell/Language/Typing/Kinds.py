class Kind:
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for k, v in other.__dict__.items():
            if k not in self.__dict__ or self.__dict__[k] != v:
                return False
        return True


class Star(Kind):
    def __init__(self):
        pass

    def __str__(self):
        return "*"

    def __hash__(self):
        return hash(id(self))


class KindFunc(Kind):
    def __init__(self, k0: Kind, k1: Kind):
        self.k0 = k0
        self.k1 = k1

    def __str__(self):
        return "{} -> {}".format(
            str(self.k0) if not isinstance(self.k0, KindFunc)
            else "({})".format(str(self.k0)),
            str(self.k1)
        )

    def __hash__(self):
        return hash((self.k0, self.k1))


class KindConstraint(Kind):
    def __init__(self):
        pass

    def __str__(self):
        return "Constraint"

    def __hash__(self):
        return hash(id(self))


star = Star()
k_constraint = KindConstraint()
