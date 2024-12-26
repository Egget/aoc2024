import sys
import re
from operator import and_, or_, xor
from itertools import combinations

bits = dict()
w_bits = set()
zbits = list()
xbits = list()
ybits = list()

def check_full_add(xbit, c_in, zbit, zbit1):
    ab = None
    abc = None
    aba = None
    for c in xbit.children:
        if c.op == xor:
            if check_bit(c.t) == 'add':
                ab = c.t
            else:
                w_bits.add(c.t.name)
        elif c.op == and_:
            if check_bit(c.t) == 'carry':
                aba = c.t
            else:
                w_bits.add(c.t.name)
    if c_in:
        for c in c_in.children:
            if c.op == xor:
                if c.t != zbit:
                    w_bits.add(c.t.name)
            elif c.op == and_:
                if check_bit(c.t) == 'carry':
                    abc = c.t
                else:
                    w_bits.add(c.t.name)
    if ab:
        for c in ab.children:
            if c.op == xor:
                if c.t != zbit:
                    w_bits.add(c.t.name)
            elif c.op == and_:
                if abc and abc != c.t:
                    if abc.find_path(zbit1):
                        w_bits.add(c.t.name)
                    else:
                        w_bits.add(abc.name)
                        abc = c.t
    if aba:
        c = aba.children[0]
        if c.op == or_:
            if check_bit(c.t) == 'add':
                c_out = c.t
            else:
                w_bits.add(c.t.name)
    if abc:
        c = abc.children[0]
        if c.op == or_:
            if c_out and c_out != c.t:
                if c_out.find_path(zbit1):
                    w_bits.add(c.t.name)
                else:
                    w_bits.add(c_out.name)
                    c_out = c.t
            else:
                c_out = c.t
    return c_out

def check_bit(bit):
    gate_types = list(map(lambda c: c.op, bit.children))
    if len(gate_types) == 2:
        return 'add'
    elif len(gate_types) == 1:
        return 'carry'
    else:
        return None

class Bit:
    def __init__(self, name):
        self.name = name
        if self.name.startswith('z'):
            zbits.append(self)
        elif self.name.startswith('x'):
            xbits.append(self)
        elif self.name.startswith('y'):
            ybits.append(self)
        self.val = None
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parent = parent

    def set_val(self, val):
        self.val = val
        for g in self.children:
            g.calc()

    def find_path(self, target):
        rets = []
        if self == target:
            return [[self.parent]]
        for g in self.children:
            if ret := g.t.find_path(target):
                if self.parent:
                    for r in ret:
                        r.append(self.parent)
                rets.extend(ret)
        if rets:
            return rets
        return None

    def __str__(self):
        return self.name

class Gate:
    def __init__(self, a, b, t, op):
        self.op = op
        if a in bits:
            self.a = bits[a]
        else:
            self.a = Bit(a)
            bits[a] = self.a
        self.a.add_child(self)
        if b in bits:
            self.b = bits[b]
        else:
            self.b = Bit(b)
            bits[b] = self.b
        self.b.add_child(self)
        if t in bits:
            self.t = bits[t]
        else:
            self.t = Bit(t)
            bits[t] = self.t
        self.t.add_parent(self)
        self.op = op

    def __str__(self):
        if self.op == and_:
            op_str = 'AND'
        elif self.op == or_:
            op_str = 'OR'
        else:
            op_str = 'XOR'
        return f'{self.a} {op_str} {self.b} -> {self.t}'
    def __repr__(self):
        return self.__str__()

    def calc(self):
        if self.a.val != None and self.b.val != None:
            self.t.set_val(self.op(self.a.val, self.b.val))

with open(sys.argv[1]) as f:
    l = f.read().split('\n\n')
    gates = []
    for r in l[1].strip('\n').split('\n'):
        m = re.match(r'(...) (AND|OR|XOR) (...) -> (...)', r)
        a = m.group(1)
        b = m.group(3)
        t = m.group(4)
        if m.group(2) == 'AND':
            op = and_
        elif m.group(2) == 'OR':
            op = or_
        elif m.group(2) == 'XOR':
            op = xor
        gates.append(Gate(a, b, t, op))
    for r in l[0].split('\n'):
        b = r.strip('\n').split(': ')
        bits[b[0]].set_val(int(b[1]))
    s = ''.join(map(lambda z: str(z.val), sorted(zbits, key=lambda b: b.name, reverse=True)))
    print('Part 1:',int(s, 2))
    c_in = bits['gtb']  # Inspected first adder by eye (x00 ^ y00 -> z00, x00 & y00 -> gtb)
    for xb, (zb, z1b) in zip(sorted(xbits, key=lambda b: b.name)[1:], zip(sorted(zbits, key=lambda b: b.name)[1:45], sorted(zbits, key=lambda b: b.name)[2:])):
        c_in = check_full_add(xb, c_in, zb, z1b)
    print('Part 2: ',','.join(sorted(w_bits)[:-1]))  # Last zbit always marked as wrong (OR-gate)
