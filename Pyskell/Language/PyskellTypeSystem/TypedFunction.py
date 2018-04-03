"""
it's a function's world...
but it would be nothing
without types
We are going to use some hack methods for
identify the function identify in environment
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

    def __mul__(self, other):
        """(b -> c) -> (a -> b) -> (a -> c)"""
        if not isinstance(other, TypedFunction):
            return other.__rmul__(self)

        else:
            eval_env = {id(self): self.fn_type, id(other): other.fn_type}
            compose_type = Lambda("arg",
                                  FuncApp(Variable(id(self)),
                                          FuncApp(Variable(id(other)),
                                                  Variable("arg")
                                                  )
                                          )
                                  )
            new_fn_type = analyze(compose_type, eval_env)
            new_fn_arg = [other.fn_args[0]] + self.fn_args[1:]
            return TypedFunction(lambda x: self.fn(other.fn(x)),
                                 new_fn_arg, new_fn_type)

    def __mod__(self, other):
        """(a -> b) -> a -> b"""
        return self.__call__(other)
