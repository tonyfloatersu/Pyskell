from Pyskell.Language.AlgoW.SyntaxExpr import *
import unittest


class SyntaxExprTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ev1 = EVariable("var1")
        self.ev2 = EVariable("var2")
        self.ev3 = EVariable("var1")

        self.op0 = EOp(Add, ELiteral(1919), EVariable("var1"))
        self.op0_ = EOp(Add, ELiteral(1919), EVariable("var1"))
        self.op1 = EOp(Mul, EVariable("var2"), EVariable("a0"))

        self.lit0 = ELiteral(123)
        self.lit1 = ELiteral("homotopy")

    def test_syntax_expression(self):
        self.assertEqual(self.ev1, self.ev3)
        self.assertNotEqual(self.ev1, self.ev2)
        self.assertEqual(self.op0, self.op0_)
        self.assertNotEqual(self.op0, self.ev1)
        self.assertNotEqual(self.op0, self.ev2)
        self.assertNotEqual(self.lit0, self.lit1)
        self.assertNotEqual(self.lit0, self.ev1)
