"""
My variant: 1
Mathematical expression:
Input language – str like a + 2 - sin(-0.3)*(b - c).
Should support user-specific functions.
Visualization as dataflow by GraphViz DOT
"""
from collections import OrderedDict, namedtuple
import copy

from math import *

# event = namedtuple('Event', 'clock str val')
source_event = namedtuple('SourceEvent', 'in_port out_port str latency')

operators = ['+', '-', '*', '/', '(', ')', 'sin', 'cos', 'tan', 'log', 'pow', 'func']
unary_op = ['sin', 'cos']
op_levels = dict()
op_levels['+'] = 1
op_levels['-'] = 1
op_levels['*'] = 2
op_levels['/'] = 2
op_levels['('] = 0

func = lambda x, y: max(x, y)


class Interpreter(object):
    """
    1. run computational process description (see execute method);
    require a list of events, which should trigger process;
    limit on a processed event number because discrete event with cycle link has an infinite number of events;
    2. trace computational process steps (state_history, event_history);
    3. check computational process result;
    4. visualize computational process description (visualize).
    """
    def __init__(self, name='eval_interpreter'):
        self.name = name
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.state_history = []  # state dict
        self.event_history = []
        self.nodes = []

    def input_port(self, name, latency=1):
        """input: string formula"""
        self.inputs[name] = latency

    def output_port(self, name, latency=1):
        """output: value of input formula"""
        self.outputs[name] = latency

    def to_RPN(self, str_f):
        """convert formular(string) to RPN(nodes)"""
        str_f = str_f.replace(' ', '')
        op_stack = list()
        self.nodes = []  # reset nodes
        flag1 = 0
        flag2 = 0
        for i in str_f:
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
                    op_stack.append(i)
                    flag2 = 1
                else:
                    op_stack[-1] = op_stack[-1] + i
                continue
            if i == ',':
                continue
            if len(op_stack) == 0:
                op_stack.append(i)
                continue
            if i == '(':
                if flag2 == 1 and op_stack[-1] in unary_op:
                    self.nodes.append('0')
                op_stack.append(i)
                continue
            if i == ')':
                while op_stack[-1] != '(':
                    self.nodes.append(op_stack.pop(-1))
                op_stack.pop(-1)
                if flag2 == 1:
                    self.nodes.append(op_stack.pop(-1))
                    flag2 = 0
                continue
            while len(op_stack) != 0 and op_levels[op_stack[-1]] >= op_levels[i]:
                self.nodes.append(op_stack.pop(-1))
            op_stack.append(i)
        while len(op_stack) != 0:
            self.nodes.append(op_stack.pop(-1))

    def generate_tree(self):
        """
        convert PRN to Abstract Syntax Tree
        return: root of AST
        """
        node_stack = list()
        for i in self.nodes:
            if i not in operators:  # if i>='0' and i<='9':
                cur = CalculateTreeNode(para=i)
                node_stack.append(cur)
            elif i in unary_op:
                cur = CalculateTreeNode(para=i)
                cur.left = CalculateTreeNode(para='0')
                cur.right = node_stack.pop(-1)
                node_stack.append(cur)
            else:
                cur = CalculateTreeNode(para=i)
                cur.right = node_stack.pop(-1)
                cur.left = node_stack.pop(-1)
                node_stack.append(cur)
        return node_stack.pop(-1)

    def _state_initialize(self):
        env = {}
        for var in self.inputs:
            env[var] = ''
        return env

    def calculate(self, root):
        """calculate the value of node"""
        if root.para not in operators:
            return int(root.para)
        left_v = self.calculate(root.left)
        right_v = self.calculate(root.right)
        if root.para == '+':
            self.event_history.append('{}+{}->{}'.format(left_v, right_v,left_v + right_v))
            return left_v + right_v
        elif root.para == '-':
            self.event_history.append('{}-{}->{}'.format(left_v, right_v, left_v-right_v))
            return left_v - right_v
        elif root.para == '*':
            self.event_history.append('{}*{}->{}'.format(left_v, right_v, left_v*right_v))
            return left_v * right_v
        elif root.para == '/':
            self.event_history.append('{}/{}->{}'.format(left_v, right_v, left_v/right_v))
            return left_v / right_v
        elif root.para == 'sin':
            self.event_history.append('sin({})->{}'.format(right_v, sin(right_v)))
            return sin(right_v)
        elif root.para == 'cos':
            self.event_history.append('cos({})->{}'.format(right_v, cos(right_v)))
            return cos(right_v)
        elif root.para == 'tan':
            self.event_history.append('tan({})->{}'.format(right_v, tan(right_v)))
            return tan(right_v)
        elif root.para == 'log':
            self.event_history.append('log({})->{}'.format(right_v, log(left_v,right_v)))
            return log(left_v, right_v)
        elif root.para == 'pow':
            self.event_history.append('pow({},{})->{}'.format(left_v, right_v, pow(left_v, right_v)))
            return pow(left_v, right_v)
        else:
            self.event_history.append('func({},{})->{}'.format(left_v, right_v, func(left_v, right_v)))
            return func(left_v, right_v)

    def execute(self, *source_events, limit=100):
        state = self._state_initialize()
        clock = 0
        self.state_history = [(clock, copy.copy(state))]

        for se in source_events:
            if limit == 0:
                print('limit reached')
            limit -= 1
            source_latency = clock + se.latency + self.inputs.get(se.in_port, 0)
            state[se.in_port] = se.str
            self.event_history.append('input se str:{}'.format(se.str))
            self.state_history.append((source_latency, copy.copy(state)))
            if se.out_port in self.outputs:
                target_latency = self.outputs[se.out_port]
                # self.event_history.append((clock, se.var, se.str))
                self.to_RPN(se.str)
                #  print(self.nodes)
                root = self.generate_tree()
                result = self.calculate(root)
                clock = source_latency + target_latency
                state[se.out_port] = result
                self.state_history.append((clock, copy.copy(state)))
                self.event_history.append('output {} -> {}'.format(se.str, result))

    def check_result(self, *source_event):
        self.execute(*source_event)
        for se in source_event:
            if se.out_port in self.outputs:
                port = se.out_port
                # print('{} -> {}'.format(se.str, self.state_history[-1][-1].get[se.out_port, 0]))
                print('{} -> {}'.format(se.str, self.state_history[-1][-1].get(port, 0)))

    #  have not test
    def visualize(self, post_s):
        res = list()
        res.append('digraph G {')
        #res.append(' rankdir=LR;')

        for v in self.inputs:
            res.append(' {}[shape=rarrow];'.format(v))
        for v in self.outputs:
            res.append(' {}[shape=rarrow];'.format(v))
        for i, n in enumerate(post_s):
            res.append(' n_{}[label="{}"];'.format(i, post_s[i]))

        inter_stack = list()
        for i, n in enumerate(post_s):
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
        return "\n".join(res)


class CalculateTreeNode(object):
    def __init__(self, left=None, right=None, para=None):
        self.left = left
        self.right = right
        self.para = para


"""
test
"""
i = Interpreter('eval_interpreter')
i.input_port('A', latency=1)
i.output_port('B', latency=1)
'''
i.execute(
    source_event('A', 'B', '2+1-(8/2)', 0),
    source_event('A', 'B', 'sin(0)+func(4,5)*(5-1)', 5),

)

print('event history:')
print(i.event_history)
print('state history:')
print(i.state_history)
print(i.state_history[-1][-1].get('B', 0))
'''

i.check_result(
    source_event('A', 'B', '2+1-(8/2)', 0),
    source_event('A', 'B', 'sin(0)+func(4,5)*(5-1)', 5),
)



