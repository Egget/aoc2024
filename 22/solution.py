import sys
from collections import defaultdict

def evolve(n):
    r = n << 6
    n ^= r
    n &= 16777215
    r = n >> 5
    n ^= r
    n &= 16777215
    r = n << 11
    n ^= r
    return n & 16777215

with open(sys.argv[1]) as f:
    s = 0
    changes = defaultdict(list)
    for r in f:
        if r.strip('\n') == '':
            continue
        n = int(r.strip('\n'))
        i = 2000
        window = []
        seen = set()
        while i > 0:
            n = evolve(n)
            i -= 1
            window.append(n%10)
            if len(window) < 5:
                continue
            p = window.pop(0)
            c = (p - window[0], window[0] - window[1], window[1] - window[2], window[2] - window[3])
            if c not in seen:
                changes[c].append(window[3])
            seen.add(c)
        s += n
    print('Part 1:',s)
    bananas = 0
    for c, l in changes.items():
        sl = sum(l)
        if sl > bananas:
            bananas = sl
    print('Part 2:', bananas)
