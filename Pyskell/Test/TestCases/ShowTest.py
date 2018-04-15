import unittest
from Pyskell.Language.TypeClasses import *
from Pyskell.Language.EnumList import L


class ShowTest(unittest.TestCase):
    def setUp(self):
        self.int_test = 1
        self.float_test = 1.1
        self.string_test = "some string"
        self.list_test = [1, 2, 3]
        self.set_test = {1, 1, 4, 5, 1, 4}
        self.complex_test = complex(12, 34)
        self.dict_test = {'p1': 1, 'p2': 2}
        self.haskell_list_test = L[1, 2, 3]

    def test_show(self):
        self.assertEqual(str(self.int_test), show % self.int_test)
        self.assertEqual(str(self.float_test), show % self.float_test)
        self.assertEqual(str(self.string_test), show % self.string_test)
        self.assertEqual(str(self.list_test), show % self.list_test)
        self.assertEqual(str(self.set_test), show % self.set_test)
        self.assertEqual(str(self.complex_test), show % self.complex_test)
        self.assertEqual(str(self.dict_test), show % self.dict_test)
        self.assertEqual("L[1, 2, 3]", show % self.haskell_list_test)
