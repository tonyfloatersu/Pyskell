from Pyskell.Language.HMTypeSystem import *
import unittest


class HMTypeSystemTest(unittest.TestCase):
    def setUp(self):
        self.var1 = TypeVariable()
        self.var2 = TypeVariable()
        self.var3 = TypeVariable()
        self.var4 = TypeVariable()
        self.Pair = TypeOperator("*", (self.var1, self.var2))
        self.Bool = TypeOperator("bool", [])
        self.Integer = TypeOperator("int", [])
        self.NoneT = TypeOperator("None", [])

        self.env = {"pair": Arrow(self.var1, Arrow(self.var2, self.Pair)),
                    "True":  self.Bool,
                    "None":  self.NoneT,
                    "id":    Arrow(self.var4, self.var4),
                    "cond":  Arrow(self.Bool,
                                   Arrow(self.var3,
                                         Arrow(self.var3, self.var3))),
                    "zero":  Arrow(self.Integer, self.Bool),
                    "pred":  Arrow(self.Integer, self.Integer),
                    "times": Arrow(self.Integer,
                                   Arrow(self.Integer, self.Integer)),
                    "4":     self.Integer,
                    "123":   self.Integer,
                    "1":     self.Integer}

        self.compose = Lambda("f",
                              Lambda("g",
                                     Lambda("arg",
                                            FuncApp(Variable("g"),
                                                    FuncApp(Variable("f"),
                                                            Variable("arg"))))))

        self.pair = FuncApp(FuncApp(Variable("pair"),
                            FuncApp(Variable("f"), Variable("1"))),
                            FuncApp(Variable("f"), Variable("True")))

    def inference_success(self, expr):
        _ = analyze(expr, self.env)

    def inference_fail(self, expr):
        with self.assertRaises(InferenceError):
            analyze(expr, self.env)

    def type_unify_success(self, t_1, t_2):
        self.assertIsNone(unify_type(t_1, t_2))

    def type_unify_fail(self, t_1, t_2):
        with self.assertRaises(InferenceError):
            unify_type(t_1, t_2)

    def expression_type_check_success(self, expr, tp):
        self.type_unify_success(analyze(expr, self.env), tp)

    def expression_type_check_fail(self, expr, tp):
        with self.assertRaises(InferenceError):
            self.expression_type_check_success(expr, tp)

    def test_hm_sys_type_inference(self):
        self.inference_fail(FuncApp(Variable("times"), Variable("None")))
        self.inference_fail(FuncApp(Variable("times"), Variable("True")))
        self.inference_fail(FuncApp(Variable("times"), Variable("pred")))
        self.inference_fail(FuncApp(Variable("times"), Variable("unknown_var")))
        # mono restriction
        self.inference_fail(
            Lambda("x",
                   FuncApp(
                       FuncApp(Variable("pair"),
                               FuncApp(Variable("x"), Variable("True"))),
                       FuncApp(Variable("x"), Variable("4"))
                   )
                   )
        )
        self.inference_success(Lambda("x",
                               FuncApp(FuncApp(Variable("pair"),
                                               FuncApp(Variable("x"),
                                                       Variable("1"))),
                                       FuncApp(Variable("x"), Variable("123"))))
                               )
        # recursive type restriction
        self.inference_fail(
            Lambda("x",
                   FuncApp(Variable("x"),
                           Variable("x"))
                   )
        )

    def test_hm_sys_type_check(self):
        self.expression_type_check_success(Variable("123"), self.Integer)
        self.expression_type_check_success(Variable("True"), self.Bool)
        self.expression_type_check_fail(Variable("True"), self.Integer)
        self.expression_type_check_fail(Variable("123"), self.NoneT)
        self.expression_type_check_success(FuncApp(Variable("id"),
                                                   Variable("123")),
                                           self.Integer)
        self.expression_type_check_fail(FuncApp(Variable("id"),
                                                Variable("123")),
                                        self.Bool)
        self.expression_type_check_success(Lambda("x", Variable("x")),
                                           self.env["id"])
        self.expression_type_check_success(Lambda("x", Variable("x")),
                                           Arrow(TypeVariable(),
                                                 TypeVariable()))
        self.expression_type_check_success(Variable("pred"),
                                           Arrow(self.Integer, self.Integer))
        self.expression_type_check_success(Variable("pred"),
                                           Arrow(TypeVariable(),
                                                 TypeVariable()))
        self.expression_type_check_success(FuncApp(Variable("pred"),
                                                   Variable("123")),
                                           self.Integer)
        self.expression_type_check_success(self.compose,
                                           Arrow(Arrow(self.var1, self.var2),
                                                 Arrow(Arrow(self.var2,
                                                             self.var3),
                                                       Arrow(self.var1,
                                                             self.var3))))
        self.expression_type_check_success(Variable("times"),
                                           Arrow(self.Integer,
                                                 Arrow(self.Integer,
                                                       self.Integer)))
        self.expression_type_check_success(FuncApp(Variable("times"),
                                                   Variable("123")),
                                           Arrow(self.Integer, self.Integer))
        self.expression_type_check_fail(FuncApp(Variable("times"),
                                                Variable("4")),
                                        Arrow(self.Integer, self.NoneT))
        self.expression_type_check_success(Lambda("x", Variable("x")),
                                           Arrow(self.var1, self.var1))
        self.expression_type_check_success(Let("f", Lambda("x", Variable("x")),
                                               self.pair),
                                           TypeOperator("*", [self.Integer,
                                                              self.Bool]))
        self.type_unify_success(analyze(
            Lambda("x",
                   FuncApp(
                       FuncApp(Variable("pair"),
                               Variable("x")),
                       Variable("x"))),
            self.env),
            Arrow(TypeVariable(), self.Pair))
        temp = TypeVariable()
        self.expression_type_check_success(FuncApp(self.compose,
                                                   Variable("zero")),
                                           Arrow(Arrow(self.Bool, temp),
                                                 Arrow(self.Integer, temp)))
        self.expression_type_check_success(Let("a", Variable("times"),
                                               FuncApp(FuncApp(Variable("a"),
                                                               Variable("1")),
                                                       Variable("4"))),
                                           self.Integer)
        self.expression_type_check_success(FuncApp(Variable("id"),
                                                   Variable("id")),
                                           Arrow(temp, temp))
        self.expression_type_check_success(FuncApp(FuncApp(self.compose,
                                                           Variable("id")),
                                                   Variable("id")),
                                           Arrow(temp, temp))
        t_tp_1, t_tp_2, t_tp_3 = TypeVariable(), TypeVariable(), TypeVariable()
        self.expression_type_check_success(self.compose,
                                           Arrow(Arrow(t_tp_1, t_tp_2),
                                                 Arrow(Arrow(t_tp_2, t_tp_3),
                                                       Arrow(t_tp_1, t_tp_3))))

        self.expression_type_check_success(FuncApp(FuncApp(Variable("pair"),
                                                           Variable("1")),
                                                   Variable("True")),
                                           TypeOperator("*", [self.Integer,
                                                              self.Bool]))
        self.expression_type_check_success(FuncApp(FuncApp(Variable("pair"),
                                                           Variable("1")),
                                                   Variable("True")),
                                           TypeOperator("*", [t_tp_1,
                                                              t_tp_2]))
        self.expression_type_check_fail(FuncApp(FuncApp(Variable("times"),
                                                        Variable("1")),
                                                Variable("2")),
                                        self.Bool)
        self.expression_type_check_success(Let("g", Lambda("f", Variable("4")),
                                               FuncApp(Variable("g"),
                                                       Variable("g"))),
                                           self.Integer)
        self.expression_type_check_success(FuncApp(FuncApp(self.compose,
                                                           Variable("id")),
                                                   FuncApp(Variable("times"),
                                                           Variable("1"))),
                                           Arrow(self.Integer, self.Integer))
        self.expression_type_check_success(FuncApp(FuncApp(
            self.compose,
            FuncApp(Variable("times"),
                    Variable("1"))),
            Variable("id")),
            Arrow(self.Integer, self.Integer))
        self.expression_type_check_success(
            FuncApp(Lambda("x",
                           Lambda("y",
                                  FuncApp(FuncApp(Variable("times"),
                                                  Variable("x")),
                                          Variable("y")))),
                    Variable("1")),
            Arrow(self.Integer, self.Integer))
        self.expression_type_check_success(
            FuncApp(Lambda("y",
                           Lambda("x",
                                  FuncApp(FuncApp(Variable("times"),
                                                  Variable("x")),
                                          Variable("y")))),
                    Variable("1")),
            Arrow(self.Integer, self.Integer))
        self.expression_type_check_success(
            FuncApp(FuncApp(Lambda("x",
                                   Lambda("x", Variable("x"))),
                            Variable("True")),
                    Variable("None")),
            self.NoneT
        )
        self.expression_type_check_success(
            Let("a", Variable("1"),
                Let("a", Variable("None"), Variable("a"))),
            self.NoneT
        )
        self.expression_type_check_fail(
            Let("a", Variable("1"),
                Let("a", Variable("None"), Variable("b"))),
            self.NoneT
        )
        self.expression_type_check_success(
            Let("factorial",
                Lambda("n",
                       FuncApp(FuncApp(FuncApp(Variable("cond"),
                                               FuncApp(Variable("zero"),
                                                       Variable("n"))),
                                       Variable("1")),
                               FuncApp(FuncApp(Variable("times"),
                                               Variable("n")),
                                       FuncApp(Variable("factorial"),
                                               FuncApp(Variable("pred"),
                                                       Variable("n")))
                                       ))),
                FuncApp(Variable("factorial"), Variable("4"))
                ),
            self.Integer
        )
