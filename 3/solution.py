import sys
import re

with open(sys.argv[1]) as f:
    string = f.read()
    s = 0
    for a, b in re.findall(r'mul\((\d+),(\d+)\)', string):
        s += int(a) * int(b)
    print('Part 1: ', s)

    s = 0
    go = True
    for a in re.findall(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", string):
        if a[3] == "don't()":
            go = False
        elif a[2] == 'do()':
            go = True
        else:
            if go:
                s += int(a[0]) * int(a[1])
    print('Part 2: ', s)
