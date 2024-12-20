import sys
from heapq import heappush,heappop

with open(sys.argv[1]) as f:
    grid = []
    for i, r in enumerate(f):
        row = []
        if 'S' in r:
            start = (i, r.index('S'))
        row.extend(r.strip('\n'))
        grid.append(row)
    d = [(1,0), (0,1), (-1,0), (0,-1)]
    def on_track(i, j):
        return 0 <= i < len(grid) and 0 <= j < len(grid[i])

    def get_neighbours(pos):
        ret = []
        i, j = pos
        for i_off, j_off in d:
            if on_track(i+i_off, j+j_off) and (cheat or grid[i+i_off][j+j_off] != '#'):
                ret.append((i+i_off, j+j_off))
        return ret

    scores = dict()
    q = []
    heappush(q, (0, start))
    while q:
        while q:
            score, pos = heappop(q)
            if pos not in scores:
                break
        scores[pos] = score
        for new_pos in get_neighbours(pos):
            if new_pos not in scores:
                heappush(q, (score+1, new_pos))

    def cheat(pos, score, dist):
        def distance(pos1, pos2):
            (x1,y1) = pos1
            (x2,y2) = pos2
            return abs(x1-x2) + abs(y1-y2)
        cheats = 0
        positions = set()
        i, j = pos
        for i_off in range(dist+1):
            for j_off in range(dist+1 - i_off):
                positions.add((i+i_off, j+j_off))
                positions.add((i-i_off, j+j_off))
                positions.add((i+i_off, j-j_off))
                positions.add((i-i_off, j-j_off))
        positions.remove(pos)
        for p in positions:
            if p in scores and scores[p] - score - distance(pos, p) > 99:
                cheats += 1
        return cheats
    s = 0
    s2 = 0
    for pos, score in scores.items():
        s += cheat(pos, score, 2)
        s2 += cheat(pos, score, 20)
    print('Part 1:', s)
    print('Part 2:', s2)
