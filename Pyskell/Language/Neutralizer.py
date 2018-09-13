__magic_methods__ = ["__{}__".format(s) for s in {
    "len", "getitem", "setitem", "delitem", "iter", "reversed", "contains",
    "missing", "delattr", "call", "enter", "exit", "eq", "ne", "gt", "lt",
    "ge", "le", "pos", "neg", "abs", "invert", "round", "floor", "ceil",
    "trunc", "add", "sub", "mul", "div", "truediv", "floordiv", "mod",
    "divmod", "pow", "lshift", "rshift", "or", "and", "xor", "radd", "rsub",
    "rmul", "rdiv", "rtruediv", "rfloordiv", "rmod", "rdivmod", "rpow",
    "rlshift", "rrshift", "ror", "rand", "rxor", "isub", "imul", "ifloordiv",
    "idiv", "imod", "idivmod", "irpow", "ilshift", "irshift", "ior", "iand",
    "ixor", "nonzero"}]


def replace_magic_methods(some_class, fn):
    for attr in __magic_methods__:
        setattr(some_class, attr, fn)
    return
