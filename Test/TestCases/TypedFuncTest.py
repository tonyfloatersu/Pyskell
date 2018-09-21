from Pyskell.Language import __
from Pyskell.Language import *

import unittest


class TypedFuncTest(unittest.TestCase):
    def test_typed_func(self):
        @TS(C / int >> bool >> str)
        def some_func(int_var, bool_var):
            return str(int_var) + str(bool_var)

        @TS(C / (C / "a" >> "b" >> "c") >> "b" >> "a" >> "c")
        def flipper(fn, y, _x):
            return fn(_x, y)

        self.assertEqual(flipper % some_func % False * (__ + 1) % 1, "2False")

        @TS(C[(Show, "a"), (Show, "b")] / "a" >> "b" >> str)
        def show_2(var1, var2):
            return show(var1) + show(var2)

        self.assertEqual(show_2 % 1 * show % 12, "112")

        self.assertEqual(
            str(type_of(
                show * ((__ + " verb test") ** (C / str >> str)))),
            "(str -> str)")
