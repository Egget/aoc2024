import sys
import re
from itertools import permutations

def find_all_seqs(seq):
    parts = seq.split('A')
    permutations_by_group = [
        set(permutations(part)) for part in parts
    ]
    results = []

    def backtrack(current, idx):
        if idx == len(permutations_by_group):
            result = 'A'.join(current)
            results.append(result)
            return

        for perm in permutations_by_group[idx]:
            backtrack(current + [''.join(perm)], idx + 1)
    backtrack([], 0)
    return results

with open(sys.argv[1]) as f:
    number = [['7','8','9'], ['4','5','6'], ['1','2','3'],['#','0','A']]
    direction = [['#','^','A'],['<','v','>']]
    moves = dict()
    codes = []
    for r in f:
        codes.append(r.strip('\n'))

    def check(x, y, keys):
        return 0 <= x < len(keys) and 0 <= y < len(keys[0]) and keys[x][y] != '#'

    def check_path(seq, keytype):
        if keytype == 'number':
            keys = number
            cx, cy = (3,2)
        else:
            keys = direction
            cx, cy = (0,2)
        for s in seq:
            if s == 'v':
                cx += 1
            elif s == '^':
                cx -= 1
            elif s == '<':
                cy -= 1
            elif s == '>':
                cy += 1
            if not check(cx, cy, keys):
                return False
        return True

    def split_seq(seq):
        ret = []
        s = ''
        for c in seq:
            if c != 'A':
                s += c
            else:
                s += c
                ret.append(s)
                s = ''
        return ret

    def find_shortest(seq, depth):
        if depth == 0:
            return len(seq)
        if (seq, depth) in cache:
            return cache[(seq, depth)]
        ret = None
        for s in find_all_seqs(find(seq, 'direction')):
            if not check_path(s, 'direction'):
                continue
            l = 0
            for a in split_seq(s):
                l += find_shortest(a, depth - 1)
            if not ret:
                ret = l
            ret = min(ret, l)
        cache[(seq, depth)] = ret
        return ret

    def find(seq, keytype):
        if keytype == 'number':
            keys = number
            cx, cy = (3,2)
        else:
            keys = direction
            cx, cy = (0,2)
        new_seq = ''
        for s in seq:
            curr = (cx, cy)
            for i, r in enumerate(keys):
                for j, k in enumerate(r):
                    if k == s:
                        ex = i
                        ey = j
            curr_seq = ''
            nx = ex - cx
            ny = ey - cy
            if nx > 0:
                curr_seq += 'v'*nx
            elif nx < 0:
                curr_seq += '^'*(nx*-1)
            if ny > 0:
                curr_seq += '>'*ny
            elif ny < 0:
                curr_seq += '<'*(ny*-1)
            new_seq += curr_seq + 'A'
            cx = ex
            cy = ey
        return new_seq
    cache = dict()

    total = 0
    for code in codes:
        number_seq = find(code, 'number')
        shortest = None
        for s1 in find_all_seqs(number_seq):
            if not check_path(s1, 'number'):
                continue
            l = 0
            for s2 in split_seq(s1):
                l += find_shortest(s2, 2)
            if not shortest:
                shortest = l
            shortest = min(shortest, l)
        n = int(re.match(r'^0*(\d*)A$', code).group(1))
        total += n * shortest
    print('Part 1:', total)

    total = 0
    for code in codes:
        number_seq = find(code, 'number')
        shortest = None
        for s1 in find_all_seqs(number_seq):
            if not check_path(s1, 'number'):
                continue
            l = 0
            for s2 in split_seq(s1):
                l += find_shortest(s2, 25)
            if not shortest:
                shortest = l
            shortest = min(shortest, l)
        n = int(re.match(r'^0*(\d*)A$', code).group(1))
        total += n * shortest
    print('Part 2:', total)
