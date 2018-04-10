import operator
from Basic import Syntax
from Basic import C
from Basic import TS


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

    wrapped = section_analysis.__func__

    flipper = lambda fn: lambda x, y: fn(y, x)

    __add__ = wrapped(operator.add)
    __radd__ = wrapped(flipper(operator.add))
    __sub__ = wrapped(operator.sub)
    __rsub__ = wrapped(flipper(operator.sub))
    __div__ = wrapped(operator.div)
    __rdiv__ = wrapped(flipper(operator.div))
    __mul__ = wrapped(operator.mul)
    __rmul__ = wrapped(flipper(operator.mul))
    __truediv__ = wrapped(operator.truediv)
    __rtruediv__ = wrapped(flipper(operator.truediv))
    __floordiv__ = wrapped(operator.floordiv)
    __rfloordiv__ = wrapped(flipper(operator.floordiv))
    __mod__ = wrapped(operator.mod)
    __rmod__ = wrapped(flipper(operator.mod))
    __divmod__ = wrapped(divmod)
    __rdivmod__ = wrapped(flipper(divmod))
    __pow__ = wrapped(operator.pow)
    __rpow__ = wrapped(flipper(operator.pow))
    __lshift__ = wrapped(operator.lshift)
    __rlshift__ = wrapped(flipper(operator.lshift))
    __rshift__ = wrapped(operator.rshift)
    __rrshift__ = wrapped(flipper(operator.rshift))
    __or__ = wrapped(operator.or_)
    __ror__ = wrapped(flipper(operator.or_))
    __and__ = wrapped(operator.and_)
    __rand__ = wrapped(flipper(operator.and_))
    __xor__ = wrapped(operator.xor)
    __rxor__ = wrapped(flipper(operator.xor))

    __eq__ = wrapped(operator.eq)
    __ne__ = wrapped(operator.ne)
    __gt__ = wrapped(operator.gt)
    __lt__ = wrapped(operator.lt)
    __ge__ = wrapped(operator.ge)
    __le__ = wrapped(operator.le)


__ = QuickLambda("Quick Lambda Error")
