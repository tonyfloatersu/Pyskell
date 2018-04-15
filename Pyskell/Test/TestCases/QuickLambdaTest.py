import unittest
from Pyskell.Language.Syntax.QuickLambda import __
from Pyskell.Language.TypeClasses import show
from Pyskell.Language.Syntax import *


class TestQuickLambda(unittest.TestCase):
    def test_ql(self):

        @TS(C / int >> int)
        def p1(v):
            return v + 1

        self.assertTrue("answer is 42", ("answer is " + __) * show * (__ * 6) * p1 % 6)
        self.assertEqual(114514, (__ + 514) * (__ * 1000) % 114)
        self.assertEqual("you are retarded",
                         (__ + " retarded") * (__ + " are") % "you")
        self.assertEqual(1, (__ - 5)(6))
        self.assertTrue((__ > 100) % 101)
        self.assertTrue((__ == 4) % 4)
        self.assertFalse((__ == 4) % 5)
        self.assertTrue((__ != 4) % 5)
        self.assertFalse((__ != 4) % 4)
        self.assertTrue((100 < __) % 101)
        self.assertTrue((4 == __) % 4)
        self.assertFalse((4 == __) % 5)
        self.assertTrue((4 != __) % 5)
        self.assertFalse((4 != __) % 4)
        self.assertEqual(100, (__ + __)(1, 99))
        self.assertEqual(1, (__ - __)(200, 199))
        self.assertEqual(399, (__ * __)(19, 21))
        self.assertEqual(128, (__ / __)(512, 4))
        self.assertEqual(12, ((__ * 4) * (__ + 2) * (1 + __))(0))
        self.assertEqual(2, (__ + 1) * (__ / 2) * (2 - __) % 0)
        self.assertEqual(4, (__ + 1) * (__ * 3) % 1)
