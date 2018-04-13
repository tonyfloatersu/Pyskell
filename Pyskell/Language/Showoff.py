from TypeClasses import *
from Syntax import __
from EnumList import *
from PyskellTypeSystem import *
from HMTypeSystem import *


@TS(C / int >> bool >> str)
def some_func(int_var, bool_var):
    return str(int_var) + str(bool_var)


@TS(C / (C / "a" >> "b" >> "c") >> "b" >> "a" >> "c")
def flipper(fn, y, _x):
    return fn(_x, y)


print flipper % some_func % False * (__ + 1) % 1

print (__ + " retarded") * (__ + " are") % "you"

print (__ + 514) * (__ * 1000) % 114


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
def summer(var):
    return sum(var)


print summer % L[1, ..., 10]

print show % 1
print show % 1.1
print show % [1, 2, 3]
print show % L[1, 2, 3]
print show % "retarded"
print show % complex(1, 1)
print show % {1, 1, 4, 5, 1, 4}
print show % {"pattern 1": 1,
              "pattern 2": 2}

print type_of(show * ((__ + " verb test") ** (C / str >> str)))
