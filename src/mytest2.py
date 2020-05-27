import unittest
from mathematical import *


class MathTest(unittest.TestCase):
    def test_1(self):
        i = MathExp('a+5-b')
        i.to_RPN()
        self.assertEqual(i.evaluate(a=1, b=2), 4.0)

    def test_2(self):
        i = MathExp('12-(sin(3-a*b)+log(100,10))')
        i.to_RPN()
        self.assertEqual(i.evaluate(a=1, b=3,), 10.0)

    def test_3(self):
        i = MathExp('12-(cos((3-a)*b)+(func(c)+3))')
        i.to_RPN()
        self.assertEqual(i.evaluate(a=3, b=5, c=7, func=lambda x:x/2), 4.5)


if __name__ == '__main__':
    unittest.main()
