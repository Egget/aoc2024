import sys
import re
import time

with open(sys.argv[1]) as f:
    robots = []
    for r in f:
        m = re.match(r'p=(-?[0-9]+),(-?[0-9]+) v=(-?[0-9]+),(-?[0-9]+)', r)
        robots.append(list(map(int, m.group(1,2,3,4))))
    xtiles = 101
    ytiles = 103

    def move(r, n):
        i = r[0]
        j = r[1]
        while n > 0:
            i = (i + r[2]) % xtiles
            j = (j + r[3]) % ytiles
            n -= 1
        return (i,j)
    pos = []
    for r in robots:
        pos.append(move(r,100))
    middlex = xtiles//2
    middley = ytiles//2
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for (x,y) in pos:
        if x < middlex:
            if y < middley:
                q1 += 1
            elif y > middley:
                q2 += 1
        elif x > middlex:
            if y < middley:
                q3 += 1
            elif y > middley:
                q4 += 1

    max_count = 0
    max_secs = 0
    for n in range(101*103):
        pos = set()
        for r in robots:
            (x,y) = move(r, 1)
            r[0] = x
            r[1] = y
            pos.add((x,y))
        if len(pos) > max_count:
            max_count = len(pos)
            max_secs = n+1

    print('Part 1:', q1*q2*q3*q4)
    print('Part 2:', max_secs)
