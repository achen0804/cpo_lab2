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


1. Input data validation in aspect-oriented style with unit tests.
2. Add support for custom function with arity more than 1 (`sum(1, 2)`) and remove the restriction on custom function name and number.
3. Add negative tests (running with wrong expression should raise readable error messages).
"""

from math import *

operators = ['+', '-', '*', '/', '(', ')', ',']
op_levels = dict()
op_levels['+'] = 1
op_levels['-'] = 1
op_levels['*'] = 2
op_levels['/'] = 2
op_levels['('] = 0


def negative_test(f):
    def test(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError:
            print('Wrong Expression! Please check the expression!')
    return test


class MathExp(object):
    def __init__(self, exp='0'):
        self.exp = exp
        self.nodes = []
        self.values = dict()

    def to_RPN(self):
        """convert formular(string) to RPN(nodes)"""
        str_f = self.exp.replace(' ', '')
        op_stack = list()
        s = ''
        flag1 = 0
        flag2 = 0
        for index, i in enumerate(str_f):
            if flag2 == 1:
                if i not in operators:
                    s += i
                    continue
                else:
                    if len(s) == 1:
                        self.nodes.append(s)
                    else:
                        op_stack.append(s)
                    flag2 = 0

            if ((i >= '0') and (i <= '9')) or i == '.':
                if flag1 == 0:
                    self.nodes.append(i)
                    flag1 = 1
                else:
                    self.nodes[-1] = self.nodes[-1] + i
                continue
            flag1 = 0

            if (i >= 'a') and (i <= 'z'):
                s = i
                flag2 = 1
                continue

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
                #if len(op_stack) == 0:
                #    raise ValueError
                op_stack.pop(-1)
                # pop special operators
                if (len(op_stack) != 0) and (op_stack[-1] not in operators):
                    self.nodes.append(op_stack.pop(-1))
                continue

            while len(op_stack) != 0 and op_levels[op_stack[-1]] >= op_levels[i]:
                self.nodes.append(op_stack.pop(-1))
            op_stack.append(i)

        if flag2 == 1:
            self.nodes.append(s)

        while len(op_stack) != 0:
            self.nodes.append(op_stack.pop(-1))

    @negative_test
    def visualize(self):
        """dot pic.dot -T png -o pic.png"""
        res = list()
        res.append('digraph G {')
        res.append(' rankdir=BT;')

        for i, n in enumerate(self.nodes):
            res.append(' n_{}[label="{}"];'.format(i, n))

        index = len(self.nodes)

        inter_stack = list()
        for i, n in enumerate(self.nodes):
            if n in ['sin', 'cos', 'tan']:
                cur = inter_stack.pop(-1)
                res.append('{} -> n_{};'.format(cur, i))
                inter_stack.append('n_{}'.format(i))
            elif n in operators or i in ['log', 'pow']:
                cur1 = inter_stack.pop(-1)
                cur2 = inter_stack.pop(-1)
                res.append('{} -> n_{};'.format(cur1, i))
                res.append('{} -> n_{};'.format(cur2, i))
                inter_stack.append('n_{}'.format(i))
            elif n not in self.values.keys():
                inter_stack.append('n_{}'.format(i))
            elif len(n) == 1:
                res.append(' n_{}[label="{}"];'.format(index, self.values[n]))
                res.append('n_{} -> n_{};'.format(index, i))
                index += 1
                inter_stack.append('n_{}'.format(i))
            else:
                f = self.values[n]
                args_nums = f.__code__.co_argcount
                for j in range(args_nums):
                    cur = inter_stack.pop(-1)
                    res.append('{} -> n_{};'.format(cur, i))
                inter_stack.append('n_{}'.format(i))
        res.append('}')
        file = open('pic.dot', 'w')
        file.write("\n".join(res))
        print("\n".join(res))

    @negative_test
    def evaluate(self, **kwargs):
        inter_stack = list()
        self.values = kwargs
        for i in self.nodes:
            if i == 'sin':
                inter_stack.append(sin(inter_stack.pop(-1)))
            elif i == 'cos':
                inter_stack.append(cos(inter_stack.pop(-1)))
            elif i == 'tan':
                inter_stack.append(tan(inter_stack.pop(-1)))
            elif i == '+':
                right = inter_stack.pop(-1)
                left = inter_stack.pop(-1)
                inter_stack.append(left + right)
            elif i == '-':
                right = inter_stack.pop(-1)
                left = inter_stack.pop(-1)
                inter_stack.append(left - right)
            elif i == '*':
                right = inter_stack.pop(-1)
                left = inter_stack.pop(-1)
                inter_stack.append(left * right)
            elif i == '/':
                right = inter_stack.pop(-1)
                left = inter_stack.pop(-1)
                inter_stack.append(left / right)
            elif i == 'log':
                right = inter_stack.pop(-1)
                left = inter_stack.pop(-1)
                inter_stack.append(log(left, right))
            elif i == 'pow':
                right = inter_stack.pop(-1)
                left = inter_stack.pop(-1)
                inter_stack.append(pow(left, right))
            elif i not in self.values.keys():
                inter_stack.append(float(i))
            elif len(i) == 1:
                inter_stack.append(self.values[i])
            else:
                f = self.values[i]
                args_nums = f.__code__.co_argcount

                dic = dict()
                for j in range(args_nums):
                    dic[j] = inter_stack.pop(-1)
                v = f(*dic.values())
                inter_stack.append(v)

        return inter_stack.pop(-1)

