import sys
import re
import functools

with open(sys.argv[1]) as f:
    rules = {}
    s = 0
    s2 = 0
    for r in f:
        if m := re.match(r'^(\d+)\|(\d+)\n$', r):
            x = int(m.group(1))
            y = int(m.group(2))
            if x not in rules:
                rules[x] = set()
            rules[x].add(y)
        elif len(r) > 3:
            l = list(map(int, r.strip('\n').split(',')))
            ok = True
            checked = set()
            for e in l:
                if e in rules:
                    for rule in rules[e]:
                        if rule in checked:
                            ok = False
                checked.add(e)
            if ok:
                s += l[len(l)//2]
            else:
                def compare(e1, e2):
                    if e1 == e2:
                        return 0
                    if e1 in rules:
                        if e2 in rules[e1]:
                            return -1
                    if e2 in rules:
                        if e1 in rules[e2]:
                            return 1
                s2 += sorted(l, key=functools.cmp_to_key(compare))[len(l)//2]
    print('Part 1: ', s)
    print('Part 2: ', s2)
