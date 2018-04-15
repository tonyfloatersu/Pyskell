import unittest
from Pyskell.Language.Syntax import *
from Pyskell.Language.TypeClasses import *
from Pyskell.Language.EnumList import L, Enum
from Pyskell.Language.Syntax.QuickLambda import __


class ADTTest(unittest.TestCase):
    def test_adt(self):
        Unit, V1, V2, V3 = data.Unit == d.V1 | d.V2 | d.V3 \
                                      & deriving(Eq, Ord, Enum, Bounded)
        self.assertEqual(V1, V1)
        self.assertEqual(V2, V2)
        self.assertEqual(V3, V3)
        self.assertNotEqual(V1, V2)
        self.assertNotEqual(V1, V3)
        self.assertNotEqual(V2, V3)

        Instance(Show, Unit).where(
            show=lambda _x: ~(Guard(_x) | g(__ == V1) >> "a"
                              | g(__ == V2) >> "b"
                              | otherwise >> "c")
        )

        self.assertEqual("a", show % V1)
        self.assertEqual("b", show % V2)
        self.assertEqual("c", show % V3)
        boundaries = bounds(V1)
        self.assertEqual(V1, boundaries[0])
        self.assertEqual(V3, boundaries[-1])
        adt_list = L[boundaries[0], ..., boundaries[-1]]
        self.assertEqual(3, len(adt_list))
        self.assertTrue(V1 < V3)
        self.assertFalse(V2 > V2)
        self.assertFalse(V2 > V3)
