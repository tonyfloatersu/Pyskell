import unittest
from Pyskell.Language import __
from Pyskell.Language import *


class ADTTest(unittest.TestCase):
    def test_adt(self):

        @AlgebraDT(deriving=(Eq, Ord, Enum, Bounded, Show))
        class Unit(HigherKT()):
            V1: gT / td("Unit")
            V2: gT / td("Unit")
            V3: gT / td("Unit")
        V1, V2, V3 = Unit.repertoire

        self.assertEqual(show % V1, "V1")
        self.assertEqual(show % V2, "V2")
        self.assertEqual(show % V3, "V3")

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
