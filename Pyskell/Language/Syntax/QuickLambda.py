import operator
from .Basic import Syntax
from .Basic import C
from .Basic import TS


class QuickLambda(Syntax):
    def __init__(self, ql_err_msg):
        super(QuickLambda, self).__init__(ql_err_msg)

    @staticmethod
    def section_analysis(fn):
        def wrapper(_, y):
            if isinstance(y, QuickLambda):
                @TS(C / "a" >> "b" >> "c")
                def func_2(a, b):
                    return fn(a, b)
                return func_2

            @TS(C / "a" >> "b")
            def func_1(a):
                return fn(a, y)
            return func_1
        return wrapper

    wrapper = section_analysis.__func__

    @staticmethod
    def flip(f):
        return lambda x, y: f(y, x)

    flipper = flip.__func__

    __add__ = wrapper(operator.add)
    __sub__ = wrapper(operator.sub)
    __mul__ = wrapper(operator.mul)
    __truediv__ = wrapper(operator.truediv)
    __floordiv__ = wrapper(operator.floordiv)
    __mod__ = wrapper(operator.mod)
    __divmod__ = wrapper(divmod)
    __pow__ = wrapper(operator.pow)
    __lshift__ = wrapper(operator.lshift)
    __rshift__ = wrapper(operator.rshift)
    __or__ = wrapper(operator.or_)
    __and__ = wrapper(operator.and_)
    __xor__ = wrapper(operator.xor)

    __eq__ = wrapper(operator.eq)
    __ne__ = wrapper(operator.ne)
    __gt__ = wrapper(operator.gt)
    __lt__ = wrapper(operator.lt)
    __ge__ = wrapper(operator.ge)
    __le__ = wrapper(operator.le)

    __radd__ = wrapper(flipper(operator.add))
    __rsub__ = wrapper(flipper(operator.sub))
    __rmul__ = wrapper(flipper(operator.mul))
    __rtruediv__ = wrapper(flipper(operator.truediv))
    __rfloordiv__ = wrapper(flipper(operator.floordiv))
    __rmod__ = wrapper(flipper(operator.mod))
    __rdivmod__ = wrapper(flipper(divmod))
    __rpow__ = wrapper(flipper(operator.pow))
    __rlshift__ = wrapper(flipper(operator.lshift))
    __rrshift__ = wrapper(flipper(operator.rshift))
    __ror__ = wrapper(flipper(operator.or_))
    __rand__ = wrapper(flipper(operator.and_))
    __rxor__ = wrapper(flipper(operator.xor))


__ = QuickLambda("Quick Lambda Error")
