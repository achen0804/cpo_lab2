"""
My variant: 1
Mathematical expression:
Input language – str like a + 2 - sin(-0.3)*(b - c).
Should support user-specific functions.
Visualization as dataflow by GraphViz DOT

1. Why you define some tests inside another test (e.g., test_1)?
2. You need to improve your API. I would like to see something like `MathExp` class with the following behavior:
e = MathExp("12-3+w")
e.evaluate(w=1)  # return 10
e.evaluate(w=2)  # return 11

e2 = MathExp("f(1)")
e.evaluate(f=lambda x: x + 1)  # return 2

If you want to support multiple results – do it by dict.

3. Refactor your code. Improve naming and tests (more variables, functions, brackets…).
"""
from math import *

operators = ['+', '-', '*', '/', '(', ')', 'sin', 'cos', 'tan', 'log', 'pow', 'func']
unary_op = ['sin', 'cos', 'tan', 'func']
special_op = ['sin', 'cos', 'tan', 'log', 'pow', 'func']
op_levels = dict()
op_levels['+'] = 1
op_levels['-'] = 1
op_levels['*'] = 2
op_levels['/'] = 2
op_levels['('] = 0
op_levels['sin'] = 3
op_levels['cos'] = 3
op_levels['tan'] = 3
op_levels['log'] = 3
op_levels['pow'] = 3
op_levels['func'] = 3


class MathExp(object):
    def __init__(self, exp='0'):
        self.exp = exp
        self.nodes = []

    def to_RPN(self):
        """convert formular(string) to RPN(nodes)"""
        str_f = self.exp.replace(' ', '')
        op_stack = list()
        s = ''
        flag1 = 0
        flag2 = 0
        for index, i in enumerate(str_f):
            if ((i >= '0') and (i <= '9')) or i == '.':
                if flag1 == 0:
                    self.nodes.append(i)
                    flag1 = 1
                else:
                    self.nodes[-1] = self.nodes[-1] + i
                continue
            flag1 = 0

            if (i >= 'a') and (i <= 'z'):
                if flag2 == 0:
                    s = i
                    flag2 = 1
                else:
                    s += i
                if s in operators:
                    op_stack.append(s)
                    flag2 = 0
                if index+1 == len(str_f):
                    self.nodes.append(s)
                continue
            if flag2 != 0:
                self.nodes.append(s)
                flag2 = 0

            if i == ',':
                continue

            if len(op_stack) == 0:
                op_stack.append(i)
                continue

            if i == '(':
                op_stack.append(i)
                continue

            if i == ')':
                while op_stack[-1] != '(':
                    self.nodes.append(op_stack.pop(-1))
                op_stack.pop(-1)
                if (len(op_stack) != 0) and (op_stack[-1] in unary_op):
                    self.nodes.append(op_stack.pop(-1))
                continue

            while len(op_stack) != 0 and op_levels[op_stack[-1]] >= op_levels[i]:
                self.nodes.append(op_stack.pop(-1))
            op_stack.append(i)

        while len(op_stack) != 0:
            self.nodes.append(op_stack.pop(-1))

    def visualize(self):
        """dot pic.dot -T png -o pic.png"""
        res = list()
        res.append('digraph G {')
        res.append(' rankdir=BT;')

        for i, n in enumerate(self.nodes):
            res.append(' n_{}[label="{}"];'.format(i, n))

        inter_stack = list()
        for i, n in enumerate(self.nodes):
            if n not in operators:
                inter_stack.append('n_{}'.format(i))
            elif n in unary_op:
                cur = inter_stack.pop(-1)
                res.append('{} -> n_{};'.format(cur, i))
                inter_stack.append('n_{}'.format(i))
            else:
                cur1 = inter_stack.pop(-1)
                cur2 = inter_stack.pop(-1)
                res.append('{} -> n_{};'.format(cur1, i))
                res.append('{} -> n_{};'.format(cur2, i))
                inter_stack.append('n_{}'.format(i))

        res.append('}')
        file = open('pic.dot','w')
        file.write("\n".join(res))
        print("\n".join(res))

    def evaluate(self, **kwargs):
        inter_stack = list()
        values = kwargs
        for i in self.nodes:
            if i not in operators:
                if i in values.keys():
                    inter_stack.append(values[i])
                else:
                    inter_stack.append(float(i))
            elif i in unary_op:
                cur = inter_stack.pop(-1)
                if i == 'sin':
                    inter_stack.append(sin(cur))
                elif i == 'cos':
                    inter_stack.append(cos(cur))
                elif i == 'tan':
                    inter_stack.append(tan(cur))
                elif i == 'func':
                    inter_stack.append(values[i](cur))
            else:
                right = inter_stack.pop(-1)
                left = inter_stack.pop(-1)
                if i == '+':
                    inter_stack.append(left+right)
                elif i == '-':
                    inter_stack.append(left-right)
                elif i == '*':
                    inter_stack.append(left*right)
                elif i == '/':
                    inter_stack.append(left/right)
                elif i == 'log':
                    inter_stack.append(log(left, right))
                else:
                    inter_stack.append(pow(left, right))
        return inter_stack.pop(-1)

