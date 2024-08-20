from main import *
import unittest

class TestFractionMethods(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(Fraction(3, 7), Fraction(9, 21))
        self.assertNotEqual(Fraction(1, 3), Fraction(2, 4))

    def test_reduced(self):
        q = Fraction(12, 18)
        self.assertEqual(q.reduced(), Fraction(2, 3))
    
    def test_reduce_at_init(self):
        q = Fraction(18, 6, reduce = True)
        self.assertEqual(q.numerator, 3)
        self.assertEqual(q.denominator, 1)

    def test_from_string(self):
        self.assertEqual(Fraction(31,534), Fraction.from_string("31/534"))
        self.assertEqual(Fraction(3, 24), Fraction.from_string(" 3 /    24"))
        self.assertEqual(Fraction(5433, 100), Fraction.from_string("54.33"))
        self.assertEqual(Fraction(8, 1), Fraction.from_string("8"))

if __name__ == "__main__":
    unittest.main()