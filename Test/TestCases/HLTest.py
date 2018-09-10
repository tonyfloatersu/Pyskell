import unittest
from Pyskell.Language.EnumList import L
from Pyskell.Language.TypeClasses import *


class HLTest(unittest.TestCase):
    def test_haskell_list(self):
        l1 = L[1, 2, ...]
        l2 = L[[1]]

        self.assertTrue(l1 > l2)
        self.assertFalse(l1 < l2)

        l3 = L[1, 3, ...]
        for i in L[1, 3, ...]:
            if i > 20:
                break
            self.assertTrue(i % 2 == 1)
        self.assertEqual(29, l3[14])

        self.assertTrue(show % (3 ^ (2 ^ l2)), "L[3, 2, 1]")

        self.assertTrue(l2 != l3)

        @TS(C / [int] >> int)
        def summer(_var):
            return sum(_var)

        self.assertEqual(summer % L[1, ..., 10], 55)
