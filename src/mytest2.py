import unittest
from mathematical import *


class MathTest(unittest.TestCase):
    def test_1(self):
        """a+5-b"""
        i = MathExp('a+5-b')
        i.to_RPN()
        self.assertEqual(i.evaluate(a=1, b=2), 4.0)

    def test_2(self):
        """12-(sin(3-a*b)+log(100,10))"""
        i = MathExp('12-(sin(3-a*b)+log(100,10))')
        i.to_RPN()
        self.assertEqual(i.evaluate(a=1, b=3), 10.0)

    def test_3(self):
        """12-(cos((3-a)*b)+(func(c)+3))"""
        i = MathExp('12-(cos((3-a)*b)+(func(c)+3))')
        i.to_RPN()
        self.assertEqual(i.evaluate(a=3, b=5, c=7, func=lambda x:x/2), 4.5)

    def test_4(self):
        """func1(a,b)+func2(x,y,z)"""
        i = MathExp('func1(a,b)+func2(x,y,z)')
        i.to_RPN()
        f1 = lambda x, y: x+y
        f2 = lambda x, y, z: max(x, y, z)
        self.assertEqual(i.evaluate(a=1, b=2, x=3, y=4, z=5,func1=f1,func2=f2), 8.0)

    def test_5(self):
        """func((2+1)"""
        i = MathExp('func((2+1)')
        i.to_RPN()
        i.evaluate(func=lambda x,y:x+y)




if __name__ == '__main__':
    unittest.main()
