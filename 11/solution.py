import sys
import math

with open(sys.argv[1]) as f:
    stones = list(map(int, f.readline().strip('\n').split(' ')))

    m = dict()
    def calc(e):
        if e == 0:
            return [1]
        else:
            n = 1+math.floor(math.log10(e))
            if n % 2 == 0:
                x = 10**(n/2)
                e1 = math.floor(e//x)
                e2 = math.floor(e%x)
                return [e1, e2]
            else:
                return [e*2024]

    def blink(e, i):
        if i == 0:
            return 1
        elif (e, i) in m:
            return m[(e,i)]
        else:
            s = 0
            for x in calc(e):
                s += blink(x, i-1)
            m[(e,i)] = s
            return s

    print('Part 1:', sum(map(lambda x: blink(x, 25), stones)))
    print('Part 2:', sum(map(lambda x: blink(x, 75), stones)))

