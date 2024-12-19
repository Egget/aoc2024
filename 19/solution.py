import sys

def find_towels(ts, p, c, ml):
    if not p:
        return 1
    if p in c:
        return c[p]
    s = 0
    l = min(len(p), ml)
    for i in range(l):
        if p not in c:
            c[p] = 0
        if p[:(l-i)] in ts:
            s += find_towels(ts, p[(l-i):], c, ml)
    c[p] = s
    return s

with open(sys.argv[1]) as f:
    towels = set(f.readline().strip('\n').split(', '))
    patterns = f.read().split('\n')[1:-1]
    ml = 0
    for t in towels:
        if len(t) > ml:
            ml = len(t)
    s = 0
    s2 = 0
    cache = dict()
    for p in patterns:
        r = find_towels(towels, p, cache, ml)
        if r > 0:
            s += 1
            s2 += r
    print('Part 1:', s)
    print('Part 2:', s2)
