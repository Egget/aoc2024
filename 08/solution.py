import sys
from itertools import permutations

with open(sys.argv[1]) as f:
    grid = []
    for r in f:
        grid.append(r.strip('\n'))

    antennas = {}
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if c != '.':
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((i,j))

    def calc_antinodes(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        x_delta = x1 - x2
        y_delta = y1 - y2
        return ((x1 + x_delta, y1 + y_delta), (x2 - x_delta, y2 - y_delta))

    def calc_antinodes_p2(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        x_delta = x1 - x2
        y_delta = y1 - y2
        x = x1
        y = y1
        pts = set()
        while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            pts.add((x,y))
            x += x_delta
            y += y_delta
        x = x2
        y = y2
        while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            pts.add((x,y))
            x -= x_delta
            y -= y_delta
        return pts

    antinodes = set()
    antinodes2 = set()
    for _, v in antennas.items():
        for p1, p2 in list(permutations(v, 2)):
            for x, y in calc_antinodes(p1, p2):
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                    antinodes.add((x,y))
            for p in calc_antinodes_p2(p1, p2):
                antinodes2.add(p)

    print('Part 1: ', len(antinodes))
    print('Part 2: ', len(antinodes2))
