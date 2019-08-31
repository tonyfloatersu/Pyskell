from .Types import *
from .Kinds import star, k_constraint, KindFunc


class Rank0TypeConstructor(TypeConstructor):
    def __init__(self, name):
        super(Rank0TypeConstructor, self).__init__(name, star)


class Rank1TypeConstructor(TypeConstructor):
    def __init__(self, name, arg_num):
        new_kind = star
        for _ in range(0, arg_num):
            new_kind = KindFunc(star, new_kind)
        super(Rank1TypeConstructor, self).__init__(name, new_kind)


class ListTypeConstructor(Rank1TypeConstructor):
    def __init__(self):
        super(ListTypeConstructor, self).__init__(list, 1)


def t_list(a):
    if not isinstance(a, Type):
        raise Exception("List Type Initialize Error with No Type Arg")
    return t_app(TConstructor(ListTypeConstructor()), a)


class ArrowTypeConstructor(Rank1TypeConstructor):
    def __init__(self):
        super(ArrowTypeConstructor, self).__init__("->", 2)


def t_arr(a, b):
    if (not isinstance(a, Type)) or (not isinstance(b, Type)):
        raise Exception("Arrow Type Initialize Error with No Type Arg")
    return t_app(t_app(TConstructor(ArrowTypeConstructor()), a), b)


class TupleTypeConstructor(Rank1TypeConstructor):
    def __init__(self, num):
        if num < 2:
            raise Exception("Tuple Type Construct smaller than 2")
        super(TupleTypeConstructor, self).__init__(tuple, num)


def t_tuple(*args):
    t_con = TConstructor(TupleTypeConstructor(len(args)))
    for arg in args:
        t_con = t_app(t_con, arg)
    return t_con


"""
k constraint will be used if type class are applied
"""
