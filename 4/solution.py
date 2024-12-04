import sys

directions = {
    'N': (-1, 0),
    'NW': (-1, -1),
    'NE': (-1, 1),
    'E': (0, 1),
    'SE': (1, 1),
    'SW': (1, -1),
    'S': (1, 0),
    'W': (0, -1),
}
target = 'XMAS'

def search(i, j, grid, d, c):
    if c < 3:
        off_i, off_j = directions[d]
        if -1 < i+off_i < len(grid) and -1 < j+off_j < len(grid[i]) and grid[i+off_i][j+off_j] == target[c+1]:
            return search(i+off_i, j+off_j, grid, d, c+1)
        else:
            return 0
    else:
        return 1

with open(sys.argv[1]) as f:
    grid = []
    for row in f:
        grid.append(row)
    s = 0
    for i, r in enumerate(grid):
        for j, char in enumerate(r):
            if char == target[0]:
                for d in directions.keys():
                    s += search(i, j, grid, d, 0)
    print('Part 1: ', s)

    s = 0
    for i, r in enumerate(grid):
        for j, char in enumerate(r):
            if char == target[2]:
                hits = 0
                for ds in [('NE', 'SW'), ('NW', 'SE')]:
                    chars = []
                    for d in ds:
                        off_i, off_j = directions[d]
                        if -1 < i+off_i < len(grid) and -1 < j+off_j < len(grid[i]):
                            chars.append(grid[i+off_i][j+off_j])
                    print(sorted(chars))
                    if sorted(chars) == ['M', 'S']:
                        print('hit')
                        hits += 1
                if hits == 2:
                    s += 1

    print('Part 2: ', s)
