from Pyskell.Language.TypeClasses import *
from Pyskell.Language.Syntax import __
from Pyskell.Language.EnumList import *
from Pyskell.Language.PyskellTypeSystem import *
from Pyskell.Language.Syntax.Pattern import *
from Pyskell.Language.Syntax.Guard import *
from Pyskell.Language.Syntax.ADTs import *
from Pyskell.Language.EnumList import *


@TS(C / int >> bool >> str)
def some_func(int_var, bool_var):
    return str(int_var) + str(bool_var)


@TS(C / (C / "a" >> "b" >> "c") >> "b" >> "a" >> "c")
def flipper(fn, y, _x):
    return fn(_x, y)


print flipper % some_func % False * (__ + 1) % 1


@TS(C[(Show, "a"), (Show, "b")] / "a" >> "b" >> str)
def show_2(var1, var2):
    return show(var1) + show(var2)


print show_2 % 1 * show % 12


@TS(C / int >> int)
def p1(v):
    return v + 1


print ("answer is " + __) * show * (__ * 6) * p1 % 6

l1 = L[1, 2, ...]
l2 = L[[1]]

print l1 > l2
print l1 < l2


l3 = L[1, 3, ...]
for i in L[1, 3, ...]:
    if i > 20:
        break
    print i

print show % (3 ^ (2 ^ l2))

print l2 != l3


@TS(C / [int] >> int)
def summer(_var):
    return sum(_var)


print summer % L[1, ..., 10]


print type_of(show * ((__ + " verb test") ** (C / str >> str)))


print ~(Guard(L[1, ..., 5]) | g(lambda x: len(x) > 100) >> "rua"
                            | otherwise >> "fit")


Unit, V1, V2, V3 = data.Unit == d.V1 | d.V2 | d.V3 & deriving(Eq, Ord, Enum, Bounded)
print V1 == V1


Instance(Show, Unit).where(
    show=lambda _x: ~(Guard(_x) | g(__ == V1) >> "a"
                                | g(__ == V2) >> "b"
                                | otherwise >> "c")
)

"""
Instance(Show, Unit).where(
    show=lambda x: ~(CaseOf(x) | pb(V1) >> "a"
                               | pb(V2) >> "b"
                               | pb(V3) >> "c")
)
"""

print show % V3
print V1 < V3
print fromEnum(V3)
v1, v2 = bounds(V1)
print show % v1, show % v2
some_list = L[v1, ..., v2]
for i in some_list:
    print show % i

print show % some_list
