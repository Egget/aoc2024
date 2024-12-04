import sys

def check_row(r):
    i = 0
    safe = True
    while i < len(r) - 1:
        if i == 0:
            diff = r[i] - r[i+1]
        if check_levels(diff, r[i], r[i+1]):
            safe = False
            break
        i += 1
    return safe, i

def check_levels(diff, l1, l2):
    new_diff = l1 - l2
    return abs(new_diff) > 3 or diff*new_diff <= 0

with open(sys.argv[1]) as f:
    s = 0
    for l in f:
        r = list(map(int, l.split(' ')))
        safe, _  = check_row(r)
        if safe:
            s += 1
    print('Part 1 ', s)

with open(sys.argv[1]) as f:
    s = 0
    for l in f:
        r = list(map(int, l.split(' ')))
        safe, i = check_row(r)
        if not safe:
#            r1 = r.copy()
            r2 = r.copy()
            r3 = r.copy()
#            del r1[i]
            del r2[i+1]
            del r3[0]
#            safe1, _ = check_row(r1)
            safe2, _ = check_row(r2)
            safe3, _ = check_row(r3)
            if safe2 or safe3:
                s += 1
        else:
            s += 1
    print('Part 2 ', s)
