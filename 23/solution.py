import sys
from collections import defaultdict
from functools import reduce

with open(sys.argv[1]) as f:
    networks = defaultdict(set)
    for r in f:
        computers = r.strip('\n').split('-')
        networks[computers[0]].add(computers[1])
        networks[computers[1]].add(computers[0])

    connected = set()
    for c1, n in networks.items():
        for c2 in n:
            if c1 == c2:
                continue
            for c3 in networks[c2]:
                if c3 == c2 or c3 == c1:
                    continue
                if c1 in networks[c3]:
                    connected.add(tuple(sorted((c1, c2, c3))))
    print('Part 1:', len(list(filter(lambda y: any(map(lambda x: x[0] == 't', y)), connected))))
    while True:
        new_connected = set()
        changed = False
        for n in connected:
            new_c = reduce(set.intersection, [networks[c] for c in n])
            if new_c:
                new_n = list(n)
                new_n.append(new_c.pop())
                new_connected.add(tuple(sorted(new_n)))
                changed = True
        if not changed:
            break
        connected = new_connected
    print('Part 2:', ','.join(connected.pop()))
