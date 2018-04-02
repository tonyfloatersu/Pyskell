"""
it's a function's world...
but it would be nothing
without types
We are going to use some hack methods for
"""
from TypeSignature import *
from functools import partial


class TypedFunction(OriginType):
    def __init__(self, func, func_args, func_type):
        self.fn = func
        self.fn_args = func_args
        self.fn_type = func_type
        self.__doc__ = func.__doc__

    def __type__(self):
        return self.fn_type

    def __call__(self, *args):
        eval_type_env = {id(self): self.fn_type}
        eval_type_env.update({id(arg): type_of(arg) for arg in args})
        func_apply = Variable(id(self))
        for arg in args:
            if isinstance(arg, Undefined):
                return arg
            func_apply = FuncApp(func_apply, Variable(id(arg)))
        result_type = analyze(func_apply, eval_type_env)
        if len(self.fn_args) == len(args) + 1:
            eval_res = self.fn(*args)
            unify_type(result_type, type_of(eval_res))
            return eval_res
        return TypedFunction(partial(self.fn, *args),
                             self.fn_args[len(args):], result_type)

    def __sub__(self, other):
        """(b -> c) -> (a -> b) -> (a -> c)"""
        pass

    def __mod__(self, other):
        """(a -> b) -> a -> b"""
        return self.__call__(other)
