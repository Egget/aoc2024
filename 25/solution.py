import sys

def heights(kl):
    h = [0, 0, 0, 0, 0]
    for i, c in enumerate(kl[5:len(kl)-5]):
        if c == '#':
            h[i%5] += 1
    return tuple(h)

with open(sys.argv[1]) as f:
    locks = []
    keys = []
    for kl in f.read().strip().split('\n\n'):
        kl = kl.replace('\n', '')
        if kl.startswith('#####'):
            locks.append(heights(kl))
        else:
            keys.append(heights(kl))
    s = 0
    for key in keys:
        for lock in locks:
            if all(map(lambda kl: kl[0] + kl[1] < 6, zip(key, lock))):
                s += 1
    print('Part 1:', s)
