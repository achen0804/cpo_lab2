import unittest
from mathematical import *


class MathTest(unittest.TestCase):
    def test_1(self):
        i = MathExp('sin(0)+func(5)*(5-1)')
        i.to_RPN()
        self.assertEqual(i.evaluate(func=lambda x: x+1), 24.0)

    def test_add(self):
        i = MathExp('3+4+5+6')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 18.0)
        i = MathExp('3+8+9')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 20.0)

    def test_sub(self):
        i = MathExp('2+1+(8-2)')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 9.0)
        i = MathExp('19-8-4-2')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 5.0)
        i = MathExp('1-3-2')
        i.to_RPN()
        self.assertEqual(i.evaluate(), -4.0)

    def test_mul(self):
        i = MathExp('3*3*2')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 18.0)
        i = MathExp('(8-4)*func(5)')
        i.to_RPN()
        self.assertEqual(i.evaluate(func=lambda x: x-2), 12.0)

    def test_dev(self):
        i = MathExp('8/4/2')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 1.0)
        i = MathExp('18/(9-6)')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 6.0)

    def test_con(self):
        i = MathExp('(4+14-(2*3))/2')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 6.0)
        i = MathExp('3+7+6/3+4*4')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 28.0)

    def test_special(self):
        i = MathExp('cos(0)+func(5)+pow(2,2)')
        i.to_RPN()
        self.assertEqual(i.evaluate(func=lambda x:x*2), 15.0)
        i = MathExp('pow(3,2)+8/4')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 11.0)
        i = MathExp('pow(2,3)')
        i.to_RPN()
        self.assertEqual(i.evaluate(), 8.0)


if __name__ == '__main__':
    unittest.main()
