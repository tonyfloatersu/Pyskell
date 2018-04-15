from PyskellTypeSystem import TypeClass
from PyskellTypeSystem import is_builtin_type
from PyskellTypeSystem import add_instance
from PyskellTypeSystem import nt_to_tuple

from Syntax.Basic import TS
from Syntax.Basic import C
from Syntax.Basic import Instance
import operator


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


Instance(Show, str).where(show=str.__str__)
Instance(Show, int).where(show=int.__str__)
Instance(Show, float).where(show=tuple.__str__)
Instance(Show, long).where(show=long.__str__)
Instance(Show, complex).where(show=complex.__str__)
Instance(Show, bool).where(show=bool.__str__)
Instance(Show, list).where(show=list.__str__)
Instance(Show, tuple).where(show=tuple.__str__)
Instance(Show, set).where(show=set.__str__)
Instance(Show, dict).where(show=dict.__str__)


class Eq(TypeClass):
    @classmethod
    def make_instance(cls, _type, **args):
        if "eq" not in args:
            raise KeyError("No eq entry")

        def default_ne(self, other):
            return not args["eq"](self, other)

        __eq__ = args["eq"] ** (C / "a" >> "b" >> bool)
        __ne__ = (default_ne if "ne" not in args
                  else args["ne"]) ** (C / "a" >> "b" >> bool)
        add_instance(Eq, _type, {"eq": lambda x, y: __eq__(x, y),
                                 "ne": lambda x, y: __ne__(x, y)})
        if not is_builtin_type(_type):
            _type.__eq__ = lambda x, y: __eq__(x, y)
            _type.__ne__ = lambda x, y: __ne__(x, y)

    @classmethod
    def derive_instance(cls, _type):

        def __eq__(self, other):
            if self.__class__ == other.__class__:
                return self.__class__ == other.__class__ \
                       and nt_to_tuple(self) == nt_to_tuple(other)
            return False

        def __ne__(self, other):
            if self.__class__ != other.__class__:
                return True
            elif nt_to_tuple(self) != nt_to_tuple(other):
                return True
            else:
                return False

        Eq.make_instance(_type, eq=__eq__, ne=__ne__)


Instance(Eq, str).where(eq=str.__eq__, ne=str.__ne__)
Instance(Eq, float).where(eq=float.__eq__, ne=float.__ne__)
Instance(Eq, complex).where(eq=complex.__eq__, ne=complex.__ne__)
Instance(Eq, list).where(eq=list.__eq__, ne=list.__ne__)
Instance(Eq, tuple).where(eq=tuple.__eq__, ne=tuple.__ne__)
Instance(Eq, set).where(eq=set.__eq__, ne=set.__ne__)
Instance(Eq, dict).where(eq=dict.__eq__, ne=dict.__ne__)
Instance(Eq, type).where(eq=type.__eq__, ne=type.__ne__)
Instance(Eq, unicode).where(eq=unicode.__eq__, ne=unicode.__ne__)


class Ord(Eq):
    @classmethod
    def make_instance(cls, _type, **args):
        if "lt" not in args:
            raise TypeError("No Ord Entry")
        __lt__ = args["lt"] ** (C / "a" >> "a" >> bool)

        def default_le(x, y):
            return x.__lt__(y) or x.__eq__(y)

        __le__ = (default_le if "le" not in args
                  else args["le"]) ** (C / "a" >> "a" >> bool)

        def default_gt(x, y):
            return not x.__lt__(y) and not x.__eq__(y)

        __gt__ = (default_gt if "gt" not in args
                  else args["gt"]) ** (C / "a" >> "a" >> bool)

        def default_ge(x, y):
            return not x.__lt__(y) or x.__eq__(y)

        __ge__ = (default_ge if "ge" not in args
                  else args["ge"]) ** (C / "a" >> "a" >> bool)

        add_instance(Ord, _type, {"lt": lambda x, y: __lt__(x, y),
                                  "gt": lambda x, y: __gt__(x, y),
                                  "le": lambda x, y: __le__(x, y),
                                  "ge": lambda x, y: __ge__(x, y)})
        if not is_builtin_type(_type):
            _type.__lt__ = lambda x, y: __lt__(x, y)
            _type.__gt__ = lambda x, y: __gt__(x, y)
            _type.__le__ = lambda x, y: __le__(x, y)
            _type.__ge__ = lambda x, y: __ge__(x, y)

    @classmethod
    def derive_instance(cls, _type):
        def zip_adt_cmp(x, y, fn):
            if x.__ADT__slot__order__ == y.__ADT__slot__order__:
                if len(nt_to_tuple(x)) == 0:
                    return fn((), ())
                return fn(nt_to_tuple(x), nt_to_tuple(y))
            return fn(x.__ADT__slot__order__, y.__ADT__slot__order__)
        Ord.make_instance(_type,
                          lt=lambda x, y: zip_adt_cmp(x, y, operator.lt),
                          le=lambda x, y: zip_adt_cmp(x, y, operator.le),
                          gt=lambda x, y: zip_adt_cmp(x, y, operator.gt),
                          ge=lambda x, y: zip_adt_cmp(x, y, operator.ge))


Instance(Ord, str).where(lt=str.__lt__, le=str.__le__,
                         gt=str.__gt__, ge=str.__ge__)
Instance(Ord, float).where(lt=float.__lt__, le=float.__le__,
                           gt=float.__gt__, ge=float.__ge__)
Instance(Ord, complex).where(lt=complex.__lt__, le=complex.__le__,
                             gt=complex.__gt__, ge=complex.__ge__)
Instance(Ord, list).where(lt=list.__lt__, le=list.__le__,
                          gt=list.__gt__, ge=list.__ge__)
Instance(Ord, tuple).where(lt=tuple.__lt__, le=tuple.__le__,
                           gt=tuple.__gt__, ge=tuple.__ge__)
Instance(Ord, set).where(lt=set.__lt__, le=set.__le__,
                         gt=set.__gt__, ge=set.__ge__)
Instance(Ord, dict).where(lt=dict.__lt__, le=dict.__le__,
                          gt=dict.__gt__, ge=dict.__ge__)
Instance(Ord, unicode).where(lt=unicode.__lt__, le=unicode.__le__,
                             gt=unicode.__gt__, ge=unicode.__ge__)


class Bounded(TypeClass):
    @classmethod
    def make_instance(cls, _type, **args):
        if "minBound" not in args or "maxBound" not in args:
            raise KeyError("No Bound Entry")
        add_instance(Bounded, _type, {"minBound": args["minBound"],
                                      "maxBound": args["maxBound"]})

    @classmethod
    def derive_instance(cls, _type):
        for data_con in _type.__constructors__:
            if not isinstance(data_con, _type):
                raise TypeError("Cannot Derive Bounded for {}"
                                .format(data_con.__name__))
        Bounded.make_instance(_type,
                              minBound=_type.__constructors__[0],
                              maxBound=_type.__constructors__[-1])


@TS(C[(Bounded, "a")] / "a" >> ("a", "a"))
def bounds(sample):
    return Bounded[sample].minBound, Bounded[sample].maxBound
