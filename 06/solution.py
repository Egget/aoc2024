import sys

with open(sys.argv[1]) as f:
    grid = []
    i = 0
    j = 0
    start_i = 0
    start_j = 0
    for r in f:
        row = []
        j = 0
        for c in r.strip('\n'):
            row.append(c)
            if c == '^':
                start_i = i
                start_j = j
            j += 1
        grid.append(row)
        i += 1
    i = start_i
    j = start_j

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    s = set()
    not_loops = set()
    s2 = set()

    def step(i, j, d):
        if not (0 <= i + directions[d][0] < len(grid) and 0 <= j + directions[d][1] < len(grid[0])):
            return None
        elif grid[i + directions[d][0]][j + directions[d][1]] == '#' or grid[i + directions[d][0]][j + directions[d][1]] == 'O':
            return i, j, (d + 1) % len(directions)
        else:
            return i + directions[d][0], j + directions[d][1], d

    def find_loop(i, j, d):
        if grid[i + directions[d][0]][j + directions[d][1]] != '.':
            return False
        loop = set()
        curr = i, j, d
        loop.add(curr)
        grid[i + directions[d][0]][j + directions[d][1]] = '#'
        while new := step(*curr):
            if new in loop:
                grid[i + directions[d][0]][j + directions[d][1]] = '.'
                return True
            else:
                loop.add(new)
                curr = new
        grid[i + directions[d][0]][j + directions[d][1]] = '.'
        return False

    curr = i, j, 0
    s.add((i,j))
    while new := step(*curr):
        s.add(new[:2])
        if new[:2] not in not_loops:
            if find_loop(*curr):
                s2.add(new[:2])
            else:
                not_loops.add(new[:2])
        curr = new
    print('Part 1: ', len(s))
    print('Part 2: ', len(s2))
