import sys
import math
import re
from sympy.solvers.diophantine import diophantine
from sympy import symbols

with open(sys.argv[1]) as f:
    btns = []
    while f:
        a = f.readline()
        if a == '':
            break
        b = f.readline()
        p = f.readline()
        f.readline()
        btn_re = r'Button .: X\+(\d+), Y\+(\d+)'
        prize_re = r'Prize: X=(\d+), Y=(\d+)'
        ma = re.match(btn_re, a)
        mb = re.match(btn_re, b)
        mp = re.match(prize_re, p)
        btns.append({
            'AX': int(ma.group(1)),
            'AY': int(ma.group(2)),
            'BX': int(mb.group(1)),
            'BY': int(mb.group(2)),
            'PX': int(mp.group(1)),
            'PY': int(mp.group(2))
        })
    total = 0
    total2 = 0
    for b in btns:
        for target_offset in (0, 10000000000000):
            solutions = set()
            x, y = symbols("x, y", integer=True)
            eq1 = b['AX']*x + b['BX']*y - b['PX'] - target_offset
            eq2 = b['AY']*x + b['BY']*y - b['PY'] - target_offset
            sol = diophantine(eq1)
            if sol:
                [xt, yt], = sol
                eq3 = eq2.subs({x:xt, y:yt})
                t1, = eq3.free_symbols
                sol = diophantine(eq3, y, syms=[t1])
                if sol:
                    [t1s], = sol
                    rep = {t1:t1s}
                    a_presses = xt.subs(rep)
                    b_presses = yt.subs(rep)
                    if target_offset > 0:
                        total2 += a_presses*3 + b_presses
                    else:
                        total += a_presses*3 + b_presses
    print('Part 1:',total)
    print('Part 2:',total2)
