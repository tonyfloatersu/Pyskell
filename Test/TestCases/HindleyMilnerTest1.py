from typing import Dict

from Pyskell.Language.HindleyMilner import \
    HAST, HApplication, HLambda, HLet, HVariable, \
    HType, TFunction, TVariable, TOperator, \
    expr_type_analyze, unify

import unittest


class HMTypeSystemTest(unittest.TestCase):
    def setUp(self):
        self.var1: HType = TVariable()
        self.var2: HType = TVariable()
        self.var3: HType = TVariable()
        self.var4: HType = TVariable()
        self.Pair: HType = TOperator("*", [self.var1, self.var2])
        self.Bool: HType = TOperator(bool, [])
        self.Integer: HType = TOperator(int, [])
        self.NoneT: HType = TOperator(None, [])

        self.env: Dict[HAST, HType] = {HVariable("pair"):  TFunction(self.var1, TFunction(self.var2, self.Pair)),
                                       HVariable(True):    self.Bool,
                                       HVariable(None):    self.NoneT,
                                       HVariable("id"):    TFunction(self.var4, self.var4),
                                       HVariable("cond"):  TFunction(self.Bool,
                                                                     TFunction(self.var3,
                                                                               TFunction(self.var3, self.var3))),
                                       HVariable("zero"):  TFunction(self.Integer, self.Bool),
                                       HVariable("pred"):  TFunction(self.Integer, self.Integer),
                                       HVariable("times"): TFunction(self.Integer,
                                                                     TFunction(self.Integer, self.Integer)),
                                       HVariable(4):       self.Integer,
                                       HVariable(123):     self.Integer,
                                       HVariable(1):       self.Integer}

        self.compose = HLambda(HVariable("f"),
                               HLambda(HVariable("g"),
                                       HLambda(HVariable("arg"),
                                               HApplication(HVariable("g"),
                                                            HApplication(HVariable("f"),
                                                                         HVariable("arg"))))))

        self.pair = HApplication(HApplication(HVariable("pair"),
                                              HApplication(HVariable("f"), HVariable(1))),
                                 HApplication(HVariable("f"), HVariable(True)))

    def inference_success(self, expr):
        _ = expr_type_analyze(expr, self.env, None)

    def inference_fail(self, expr):
        with self.assertRaises(TypeError):
            expr_type_analyze(expr, self.env, None)

    def type_unify_success(self, t_1, t_2):
        self.assertIsNone(unify(t_1, t_2))

    def type_unify_fail(self, t_1, t_2):
        with self.assertRaises(TypeError):
            unify(t_1, t_2)

    def expression_type_check_success(self, expr, tp):
        self.type_unify_success(expr_type_analyze(expr, self.env), tp)

    def expression_type_check_fail(self, expr, tp):
        with self.assertRaises(TypeError):
            self.expression_type_check_success(expr, tp)

    def test_hm_sys_type_inference(self):
        self.inference_fail(HApplication(HVariable("times"), HVariable(None)))
        self.inference_fail(HApplication(HVariable("times"), HVariable(True)))
        self.inference_fail(HApplication(HVariable("times"), HVariable("pred")))
        self.inference_fail(HApplication(HVariable("times"), HVariable("unknown_var")))
        # mono restriction
        self.inference_fail(
            HLambda(HVariable("x"),
                    HApplication(
                        HApplication(HVariable("pair"),
                                     HApplication(HVariable("x"), HVariable(True))),
                        HApplication(HVariable("x"), HVariable(4))))
        )
        self.inference_success(
            HLambda(HVariable("x"),
                    HApplication(HApplication(HVariable("pair"),
                                              HApplication(HVariable("x"),
                                                           HVariable(1))),
                                 HApplication(HVariable("x"), HVariable(123))))
        )
        # recursive type restriction
        self.inference_fail(
            HLambda(HVariable("x"),
                    HApplication(HVariable("x"), HVariable("x")))
        )

    def test_hm_sys_type_check(self):
        self.expression_type_check_success(HVariable(123), self.Integer)
        self.expression_type_check_success(HVariable(True), self.Bool)
        self.expression_type_check_fail(HVariable(True), self.Integer)
        self.expression_type_check_fail(HVariable(123), self.NoneT)
        self.expression_type_check_success(HApplication(HVariable("id"), HVariable(123)),
                                           self.Integer)
        self.expression_type_check_fail(HApplication(HVariable("id"), HVariable(123)),
                                        self.Bool)
        self.expression_type_check_success(HLambda(HVariable("x"), HVariable("x")),
                                           self.env[HVariable("id")])
        self.expression_type_check_success(HLambda(HVariable("x"), HVariable("x")),
                                           TFunction(TVariable(), TVariable()))
        self.expression_type_check_success(HVariable("pred"),
                                           TFunction(self.Integer, self.Integer))
        self.expression_type_check_success(HVariable("pred"),
                                           TFunction(TVariable(), TVariable()))
        self.expression_type_check_success(HApplication(HVariable("pred"), HVariable(123)),
                                           self.Integer)
        self.expression_type_check_success(self.compose,
                                           TFunction(TFunction(self.var1, self.var2),
                                                     TFunction(TFunction(self.var2, self.var3),
                                                       TFunction(self.var1, self.var3))))
        self.expression_type_check_success(HVariable("times"),
                                           TFunction(self.Integer,
                                                     TFunction(self.Integer, self.Integer)))
        self.expression_type_check_success(HApplication(HVariable("times"),
                                                   HVariable(123)),
                                           TFunction(self.Integer, self.Integer))
        self.expression_type_check_fail(HApplication(HVariable("times"), HVariable(4)),
                                        TFunction(self.Integer, self.NoneT))
        self.expression_type_check_success(HLambda(HVariable("x"), HVariable("x")),
                                           TFunction(self.var1, self.var1))
        self.expression_type_check_success(HLet(HVariable("f"), HLambda(HVariable("x"), HVariable("x")), self.pair),
                                           TOperator("*", [self.Integer, self.Bool]))
        self.type_unify_success(
            expr_type_analyze(
                HLambda(HVariable("x"),
                        HApplication(HApplication(HVariable("pair"), HVariable("x")),
                                     HVariable("x"))),
                self.env, None),
            TFunction(TVariable(), self.Pair))
        temp = TVariable()
        self.expression_type_check_success(HApplication(self.compose, HVariable("zero")),
                                           TFunction(TFunction(self.Bool, temp),
                                                 TFunction(self.Integer, temp)))
        self.expression_type_check_success(HLet(HVariable("a"), HVariable("times"),
                                               HApplication(HApplication(HVariable("a"),
                                                               HVariable(1)),
                                                       HVariable(4))),
                                           self.Integer)
        self.expression_type_check_success(HApplication(HVariable("id"),
                                                   HVariable("id")),
                                           TFunction(temp, temp))
        self.expression_type_check_success(HApplication(HApplication(self.compose,
                                                           HVariable("id")),
                                                   HVariable("id")),
                                           TFunction(temp, temp))
        t_tp_1, t_tp_2, t_tp_3 = TVariable(), TVariable(), TVariable()
        self.expression_type_check_success(self.compose,
                                           TFunction(TFunction(t_tp_1, t_tp_2),
                                                 TFunction(TFunction(t_tp_2, t_tp_3),
                                                       TFunction(t_tp_1, t_tp_3))))

        self.expression_type_check_success(HApplication(HApplication(HVariable("pair"),
                                                           HVariable(1)),
                                                   HVariable("True")),
                                           TOperator("*", [self.Integer,
                                                              self.Bool]))
        self.expression_type_check_success(HApplication(HApplication(HVariable("pair"),
                                                           HVariable(1)),
                                                   HVariable("True")),
                                           TOperator("*", [t_tp_1,
                                                              t_tp_2]))
        self.expression_type_check_fail(HApplication(HApplication(HVariable("times"),
                                                        HVariable(1)),
                                                HVariable(2)),
                                        self.Bool)
        self.expression_type_check_success(HLet(HVariable("g"), HLambda(HVariable("f"), HVariable(4)),
                                               HApplication(HVariable("g"),
                                                       HVariable("g"))),
                                           self.Integer)
        self.expression_type_check_success(HApplication(HApplication(self.compose,
                                                           HVariable("id")),
                                                   HApplication(HVariable("times"),
                                                           HVariable(1))),
                                           TFunction(self.Integer, self.Integer))
        self.expression_type_check_success(HApplication(HApplication(
            self.compose,
            HApplication(HVariable("times"),
                    HVariable(1))),
            HVariable("id")),
            TFunction(self.Integer, self.Integer))
        self.expression_type_check_success(
            HApplication(HLambda(HVariable("x"),
                           HLambda(HVariable("y"),
                                  HApplication(HApplication(HVariable("times"),
                                                  HVariable("x")),
                                          HVariable("y")))),
                    HVariable(1)),
            TFunction(self.Integer, self.Integer))
        self.expression_type_check_success(
            HApplication(HLambda(HVariable("y"),
                           HLambda(HVariable("x"),
                                  HApplication(HApplication(HVariable("times"),
                                                  HVariable("x")),
                                          HVariable("y")))),
                    HVariable(1)),
            TFunction(self.Integer, self.Integer))
        self.expression_type_check_success(
            HApplication(HApplication(HLambda(HVariable("x"),
                                   HLambda(HVariable("x"), HVariable("x"))),
                            HVariable("True")),
                    HVariable("None")),
            self.NoneT
        )
        self.expression_type_check_success(
            HLet(HVariable("a"), HVariable(1),
                HLet(HVariable("a"), HVariable("None"), HVariable("a"))),
            self.NoneT
        )
        self.expression_type_check_fail(
            HLet(HVariable("a"), HVariable(1),
                HLet(HVariable("a"), HVariable("None"), HVariable("b"))),
            self.NoneT
        )
        self.expression_type_check_success(
            HLet(HVariable("factorial"),
                HLambda(HVariable("n"),
                       HApplication(HApplication(HApplication(HVariable("cond"),
                                               HApplication(HVariable("zero"),
                                                       HVariable("n"))),
                                       HVariable(1)),
                               HApplication(HApplication(HVariable("times"),
                                               HVariable("n")),
                                       HApplication(HVariable("factorial"),
                                               HApplication(HVariable("pred"),
                                                       HVariable("n")))
                                       ))),
                HApplication(HVariable("factorial"), HVariable(4))
                ),
            self.Integer
        )
