import sys
from operator import mul, add
import math

def conc(a, b):
    return a * 10**(1+math.floor(math.log10(b))) + b

def test(target, eq, ops):
    sums = set()
    sums.add(eq[0])
    for n in eq[1:]:
        new_sums = set()
        for s in sums:
            for op in ops:
                a = op(s, n)
                if a <= target:
                    new_sums.add(a)
        sums = new_sums
    return target in sums

with open(sys.argv[1]) as f:
    tot1 = 0
    tot2 = 0
    for equation in f:
        l = equation.strip('\n').split(':')
        target = int(l[0])
        eq = list(map(int, l[1].split(' ')[1:]))
        if test(target, eq, [mul, add]):
            tot1 += target
        elif test(target, eq, [mul, add, conc]):
            tot2 += target
    print('Part 1: ', tot1)
    print('Part 2: ', tot1 + tot2)
