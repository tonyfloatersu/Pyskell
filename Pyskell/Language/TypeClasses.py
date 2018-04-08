from PyskellTypeSystem import TypeClass
from PyskellTypeSystem import is_builtin_type
from PyskellTypeSystem import add_instance

from Syntax.Basic import TS
from Syntax.Basic import C
from Syntax.Basic import Instance
from Syntax.Pattern import nt_to_tuple


class Show(TypeClass):
    @classmethod
    def make_instance(cls, _type, **kwargs):
        if "show" not in kwargs:
            raise KeyError("No show entry")
        _show = kwargs["show"]
        __show__ = _show ** (C / "a" >> str)
        add_instance(Show, _type, {"show": lambda x: __show__(x)})
        if not is_builtin_type(_type):
            _type.__repr__ = show
            _type.__str__ = show

    @classmethod
    def derive_instance(cls, _type):
        def local_show(obj_self):
            if not hasattr(obj_self.__class__, "_fields"):
                raise TypeError("Fail to derive show.")
            if obj_self.__class__._fields.__len__() == 0:
                return obj_self.__class__.__name__
            nt_tuple = nt_to_tuple(obj_self)
            if len(nt_tuple) == 1:
                temp_str = "({})".format(Show[nt_tuple[0]].show(nt_tuple[0]))
            else:
                temp_str = Show[nt_tuple].show(nt_tuple)
            return "{}{}".format(obj_self.__class__.__name__, temp_str)
        Show.make_instance(_type, show=local_show)


@TS(C / "a" >> str)
def show(o):
    return Show[o].show(o)


Instance(Show, str).where(show=str.__repr__)
Instance(Show, int).where(show=int.__str__)
Instance(Show, float).where(show=tuple.__str__)
Instance(Show, long).where(show=long.__str__)
Instance(Show, complex).where(show=complex.__str__)
Instance(Show, bool).where(show=bool.__str__)
Instance(Show, list).where(show=list.__str__)
Instance(Show, tuple).where(show=tuple.__str__)
Instance(Show, set).where(show=set.__str__)
Instance(Show, dict).where(show=dict.__str__)
