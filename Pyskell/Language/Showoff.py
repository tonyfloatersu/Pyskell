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

print (__ + "var") * (__ + "abc") % "char"
