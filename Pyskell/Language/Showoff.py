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

l1 = L[1, ...]
l2 = L[[1]]

print l1 != l2


l3 = L[1, 2, ...]
for i in l3:
    if i > 10:
        break
    print i
