import unittest
from mathematical import *


class MathTest(unittest.TestCase):
    def test(self):
        i = Interpreter('eval_interpreter')
        i.input_port('A', latency=1)
        i.output_port('B', latency=1)
        def test_1(self):

            self.assertEqual(i.check_result(source_event('A', 'B', 'sin(0)+func(4,5)*(5-1)', 5)), [20.0])

        def test_add(self):

            self.assertEqual(i.check_result(source_event('A', 'B', '3+4+5+6', 0),
                                        source_event('A', 'B', '3+8+9', 5)), [18.0, 20.0])

        def test_sub(self):

            self.assertEqual(i.check_result(source_event('A', 'B', '2+1+(8-2)', 0),
                                        source_event('A', 'B', '19-8-4-2', 5),
                                        source_event('A', 'B', '1-3-2', 10)), [9.0, 5.0, -4.0])

        def test_mul(self):

            self.assertEqual(i.check_result(source_event('A', 'B', '3*3*2', 0),
                                        source_event('A', 'B', '(8-4)*func(5,6)', 5)), [18.0, 24.0])

        def test_dev(self):

            self.assertEqual(i.check_result(source_event('A', 'B', '8/4/2', 0)), [1.0])
            self.assertEqual(i.check_result(source_event('A', 'B', '18/(9-6)', 5)), [6.0])

        def test_con(self):

            self.assertEqual(i.check_result(source_event('A', 'B', '(4+14-(2*3))/2', 0)), [6.0])
            self.assertEqual(i.check_result(source_event('A', 'B', '(3+7+6/3+4*4)', 5)), [28.0])

        def test_special(self):

            self.assertEqual(i.check_result(source_event('A', 'B', 'cos(0)+func(5,7)+pow(2,2)', 0)), [12.0])
            self.assertEqual(i.check_result(source_event('A', 'B', 'pow(3,2)+8/4', 4)), [11.0])
            self.assertEqual(i.check_result(source_event('A','B','pow(2,3)',3)),[8.0])


if __name__ == '__main__':
    unittest.main()
