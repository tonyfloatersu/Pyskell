import itertools
import collections
from HMTypeSystem import *
from PyskellTypeSystem import *
from TypeClasses import *
from Syntax import C, TS
from Syntax import Instance
from Syntax import Syntax


class Enum(TypeClass):
    @classmethod
    def make_instance(cls, _type, **args):
        if "toEnum" not in args or "fromEnum" not in args:
            raise KeyError("No Enum Entry")

        _toEnum = args["toEnum"]
        _fromEnum = args["fromEnum"]

        def _succ(a):
            return _toEnum(_fromEnum(a) + 1)

        def _pred(a):
            return _toEnum(_fromEnum(a) - 1)

        def _enumFromThen(srt, sec):
            marker = _fromEnum(srt)
            step_len = _fromEnum(sec) - marker
            while True:
                yield _toEnum(marker)
                marker += step_len

        def _enumFrom(srt):
            return _enumFromThen(srt, _succ(srt))

        def _enumFromThenTo(srt, sec, end):
            if srt == end:
                yield srt
                return
            elif sec >= srt > end or sec <= srt < end:
                return
            marker, end_mark = _fromEnum(srt), _fromEnum(end)
            step_len = _fromEnum(sec) - marker
            while (srt < end and marker <= end_mark) or \
                  (srt > end and marker >= end_mark):
                yield _toEnum(marker)
                marker += step_len
            return

        def _enumFromTo(srt, end):
            sec = _succ(srt) if srt < end else _pred(srt)
            return _enumFromThenTo(srt, sec, end)

        add_instance(Enum, _type, {"toEnum": _toEnum,
                                   "fromEnum": _fromEnum,
                                   "succ": _succ,
                                   "pred": _pred,
                                   "enumFromThen": _enumFromThen,
                                   "enumFrom": _enumFrom,
                                   "enumFromThenTo": _enumFromThenTo,
                                   "enumFromTo": _enumFromTo})

    @classmethod
    def derive_instance(cls, _type):
        for data_con in _type.__constructors__:
            if not isinstance(data_con, _type):
                raise TypeError("Cannot Derive Enum for {}"
                                .format(data_con.__name__))
        Enum.make_instance(_type,
                           fromEnum=lambda x: _type.__constructors__.index(x),
                           toEnum=lambda x: _type.__constructors__[x])


@TS(C / "a" >> int)
def fromEnum(a):
    return Enum[a].fromEnum(a)


@TS(C / "a" >> "a")
def succ(a):
    return Enum[a].succ(a)


@TS(C / "a" >> "a")
def pred(a):
    return Enum[a].pred(a)


class HaskellList(OriginType, collections.Sequence):
    def __init__(self, head=None, tail=None):
        self.__head = []
        self.__tail = itertools.chain([])
        self.__is_fully_evaluated = True

        if head is not None and len(head) > 0:
            for sample, tester in zip(itertools.repeat(head[0]), head):
                unify_type(type_of(sample), type_of(tester))
            self.__head.extend(head)
        if tail is not None:
            self.__tail = itertools.chain(self.__tail, tail)
            self.__is_fully_evaluated = False

    def __next(self):
        if self.__is_fully_evaluated:
            raise StopIteration
        else:
            try:
                next_tail_item = next(self.__tail)
                if len(self.__head) > 0:
                    unify_type(type_of(next_tail_item),
                               type_of(self.__head[0]))
                self.__head.append(next_tail_item)
            except StopIteration:
                self.__is_fully_evaluated = True

    def __evaluate_self(self):
        while not self.__is_fully_evaluated:
            self.__next()

    def __type__(self):
        if self.__is_fully_evaluated:
            if len(self.__head) == 0:
                return ListType(TypeVariable())
            else:
                return ListType(type_of(self.__head[0]))
        elif len(self.__head) == 0:
            self.__next()
            return self.__type__()
        return ListType(type_of(self.__head[0]))

    def __rxor__(self, other):
        unify_type(self.__type__(), ListType(type_of(other)))
        if self.__is_fully_evaluated:
            return HaskellList(head=[other] + self.__head)
        else:
            return HaskellList(head=[other] + self.__head,
                               tail=self.__tail)

    def __str__(self):
        if len(self.__head) == 0 and self.__is_fully_evaluated:
            return "L[[]]"
        elif len(self.__head) == 1 and self.__is_fully_evaluated:
            return "L[[{}]]".format(show(self.__head[0]))
        line = ", ".join(show(i) for i in self.__head)
        return "L[{}]".format(line) if self.__is_fully_evaluated\
            else "L[{} ...]".format(line)

    def __getitem__(self, item):
        if isinstance(item, slice):
            index = item.stop if item.stop is not None else item.start
        else:
            index = item
        if index >= 0:
            while index + 1 > len(self.__head):
                try:
                    self.__next()
                except StopIteration:
                    break
        else:
            self.__evaluate_self()
        if isinstance(item, slice):
            if item.stop is None and not self.__is_fully_evaluated:
                return HaskellList(head=self.__head[item],
                                   tail=self.__tail)
            else:
                return HaskellList(head=self.__head[item])
        else:
            return self.__head[index]

    def __len__(self):
        self.__evaluate_self()
        return len(self.__head)

    def __iter__(self):
        for i in self.__head:
            yield i
        for j in self.__tail:
            self.__head.append(j)
            yield j

    def __contains__(self, item):
        for i in iter(self):
            if i == item:
                return True
        return False

    def __cmp__(self, other):
        if not isinstance(other, HaskellList):
            raise TypeError("{} is not Haskell List".format(other))
        if self.__is_fully_evaluated and other.__is_fully_evaluated:
            return cmp(self.__head, other.__head)
        elif len(self.__head) >= len(other.__head):
            exist_comp_res = map(lambda (x, y): cmp(x, y),
                                 zip(self.__head[:len(other.__head)],
                                     other.__head))
            for i in exist_comp_res:
                if i != 0:
                    return i
            while len(self.__head) > len(other.__head):
                if other.__is_fully_evaluated:
                    return 1
                other.__next()
                node_res = cmp(self.__head[len(other.__head) - 1],
                               other.__head[-1])
                if node_res != 0:
                    return node_res
            # tail part
            while not self.__is_fully_evaluated or \
                    not other.__is_fully_evaluated:
                if not self.__is_fully_evaluated:
                    self.__next()
                if not other.__is_fully_evaluated:
                    other.__next()
                length_comp = cmp(len(self.__head), len(other.__head))
                if length_comp != 0:
                    return length_comp
                if len(self.__head) > 0:
                    head_tail_comp = cmp(self.__head[-1],
                                         other.__head[-1])
                    if head_tail_comp != 0:
                        return head_tail_comp
        elif len(self.__head) < len(other.__head):
            return -other.__cmp__(self)
        return 0

    def __eq__(self, other):
        return cmp(self, other) == 0

    def __le__(self, other):
        return cmp(self, other) in (0, -1)

    def __lt__(self, other):
        return cmp(self, other) == -1

    def __gt__(self, other):
        return cmp(self, other) == 1

    def __ge__(self, other):
        return cmp(self, other) in (1, 0)


Instance(Show, HaskellList).where(show=HaskellList.__str__)
Instance(Eq, HaskellList).where(eq=HaskellList.__eq__)
Instance(Ord, HaskellList).where(lt=HaskellList.__lt__,
                                 gt=HaskellList.__gt__,
                                 le=HaskellList.__le__,
                                 ge=HaskellList.__ge__)
Instance(Enum, int).where(fromEnum=int, toEnum=int)
Instance(Enum, float).where(fromEnum=int, toEnum=float)


@TS(C / "a" >> "a")
def pred(a):
    return Enum[a].pred(a)


@TS(C / "a" >> "a" >> ["a"])
def enumFromThen(srt, snd):
    return L[Enum[srt].enumFromThen(srt, snd)]


@TS(C / "a" >> ["a"])
def enumFrom(srt):
    return L[Enum[srt].enumFrom(srt)]


@TS(C / "a" >> "a" >> "a" >> ["a"])
def enumFromThenTo(srt, snd, end):
    return L[Enum[srt].enumFromThenTo(srt, snd, end)]


@TS(C / "a" >> "a" >> ["a"])
def enumFromTo(srt, end):
    return L[Enum[srt].enumFromTo(srt, end)]


class GenerateHL(Syntax):
    def __getitem__(self, item):
        if isinstance(item, tuple) and len(item) <= 4 and Ellipsis in item:
            if len(item) == 2 and item[1] == Ellipsis:
                return enumFrom(item[0])
            elif len(item) == 3 and item[2] == Ellipsis:
                return enumFromThen(item[0], item[1])
            elif len(item) == 3 and item[1] == Ellipsis:
                return enumFromTo(item[0], item[2])
            elif len(item) == 4 and item[2] == Ellipsis:
                return enumFromThenTo(item[0], item[1], item[3])
            raise SyntaxError("Error in HL Constructor")
        elif hasattr(item, "next") or hasattr(item, "__next__"):
            return HaskellList(tail=item)
        return HaskellList(head=item)


L = GenerateHL("HL Constructor Error")
