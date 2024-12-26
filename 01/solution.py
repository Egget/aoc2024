import sys
import bisect

with open(sys.argv[1]) as f:
    list1 = []
    list2 = []
    for l in f:
        a, b = tuple(l.split('  '))
        list1.append(int(a))
        list2.append(int(b))
    s = 0
    list1 = sorted(list1)
    list2 = sorted(list2)
    for a, b in zip(list1, list2):
        s += abs(a - b)

    print('Part 1: ', s)

    p = 0

    for e in list1:
        i1 = bisect.bisect_right(list2,e)
        i2 = bisect.bisect_left(list2,e,hi=i1)
        p += e * (i1-i2)

    print('Part 2: ', p)
