from PyskellTypeSystem import TypeClass
from PyskellTypeSystem import is_builtin_type
from PyskellTypeSystem import add_instance

from Syntax.Basic import TS
from Syntax.Basic import T_C
from Syntax.Basic import Instance


class Show(TypeClass):
    @classmethod
    def make_instance(cls, _type, **kwargs):
        if "show" not in kwargs:
            raise KeyError("No show entry")
        show = kwargs["show"]
        __show__ = show ** (T_C / "a" >> str)
        add_instance(Show, _type, {"show": lambda x: __show__(x)})
        if not is_builtin_type(_type):
            _type.__repr__ = show
            _type.__str__ = show

    @classmethod
    def derive_instance(cls, _type):
        def local_show(self):
            pass
        Show.make_instance(_type, show=local_show)


@TS(T_C / "a" >> str)
def show(o):
    return Show[o].show(o)
