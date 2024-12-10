import sys

with open(sys.argv[1]) as f:
    grid = []
    for r in f:
        grid.append(list(map(int, r.strip('\n'))))
    dirs = [(-1, 0), (1, 0), (0,-1), (0,1)]
    def dfs(i, j, c):
        if c == 9:
            return [(i,j)]
        ret = set()
        for off_i, off_j in dirs:
            if 0 <= i+off_i < len(grid) and 0 <= j+off_j < len(grid[0]):
                n = grid[i+off_i][j+off_j]
                if n == c + 1:
                    for e in dfs(i+off_i, j+off_j,n):
                        ret.add(e)
        return ret
    def dfs2(i, j, c):
        if c == 9:
            return [[(i,j)]]
        ret = []
        for off_i, off_j in dirs:
            if 0 <= i+off_i < len(grid) and 0 <= j+off_j < len(grid[0]):
                n = grid[i+off_i][j+off_j]
                if n == c + 1:
                    paths = dfs2(i+off_i, j+off_j, n)
                    for path in paths:
                        path.append((i,j))
                        ret.append(path)

        return ret

    nines = 0
    nines2 = 0
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if c == 0:
                nines += len(dfs(i,j,0))
                nines2 += len(dfs2(i,j,0))
    print('Part 1:', nines)
    print('Part 2:', nines2)
