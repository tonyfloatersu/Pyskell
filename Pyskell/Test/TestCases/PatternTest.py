import unittest
from Pyskell.Language.Syntax.Pattern import *
from Pyskell.Language.EnumList import L


class CaseTest(unittest.TestCase):
    def test_case(self):
        self.assertEqual(3, ~(CaseOf((2, 3)) | pb((2, pb.v2)) >> va.v2
                                             | pb(2) >> -2
                                             | pb(pb.var) >> va.var))
        self.assertEqual(1, ~(CaseOf("a") | pb("a") >> 1))
        self.assertEqual("a", ~(CaseOf("a") | pb(pb.x) >> va.x))
        self.assertEqual(1, ~(CaseOf(2.0) | pb(2.0) >> ~(CaseOf("a") | pb("e") >> 3
                                                                     | pb("a") >> 1)
                                          | pb(2.0) >> 0))
        self.assertEqual([[3, 4]], ~(CaseOf([1, 2, [3, 4]]) | pb(1 ^ (2 ^ pb.x)) >> va.x
                                                            | pb(pb.v) >> False))
        self.assertEqual(1, ~(CaseOf([1, 2]) | pb([1, 2]) >> 1
                                             | pb((1, 2)) >> 2))
        self.assertEqual(2, ~(CaseOf((1, 2, 3)) | pb(1 ^ (2 ^ pb.x)) >> 2
                                                | pb(2 ^ pb.y) >> 1))
        self.assertEqual(2, ~(CaseOf(L[[]]) | pb(pb.v0 ^ pb.v1) >> 1
                                            | pb(pb.v2) >> 2))
        self.assertEqual(1, ~(CaseOf("a") | pb(pb._) >> 1
                                          | pb("a") >> 2))
        self.assertEqual(2, ~(CaseOf((1, 2, 3)) | pb((2, 1, 3)) >> 1
                                                | pb((1, pb.x, 3)) >> va.x
                                                | pb((1, 2, 3)) >> 3))
        self.assertEqual(1, ~(CaseOf([1, 2, 3, 4]) | pb(pb.a ^ (pb.b ^ pb.c)) >> 1
                                                   | pb(pb.d) >> 2))
        self.assertEqual(L[3, 2, 1],
                         ~(CaseOf(L[3, 2, 1, 0])
                           | pb(pb.a ^ (pb.b ^ pb.c)) >> L[va.a, va.b, va.c[0]]
                           | pb(pb.x) >> False))
        self.assertEqual((2, 1), ~(CaseOf((1, 2)) | pb((pb.a, pb.b)) >> (va.b, va.a)
                                                  | pb(pb.x) >> va.x))
        self.assertEqual(1, ~(CaseOf(L[1, ...]) | pb(pb.h ^ pb.l) >> va.h
                                                | pb(pb.x) >> L[[]]))
