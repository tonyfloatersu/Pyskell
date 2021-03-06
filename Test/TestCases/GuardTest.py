from Pyskell.Language import __
from Pyskell.Language import *
import unittest


class GuardTest(unittest.TestCase):
    def test_guard(self):
        self.assertEqual("fit", ~(Guard(L[1, ..., 5]) | g(lambda x: len(x) > 100) >> "rua"
                                                      | otherwise >> "fit"))

        self.assertEqual(~(Guard(100) | g(__ < 20) >> "a"
                                      | g(__ < 90) >> "b"
                                      | g(__ < 150) >> "c"
                                      | otherwise >> "d"), 'c')
