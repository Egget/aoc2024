import sys
from heapq import heappush,heappop

with open(sys.argv[1]) as f:
    grid = []
    processed = dict()
    q = []
    end = (0,0)
    for i, r in enumerate(f):
        row = []
        for j, c in enumerate(r.strip('\n')):
            if c == 'S':
                heappush(q, (0,((i,j),1)))
            elif c == 'E':
                end = (i,j)
            row.append(c)
        grid.append(row)
    curr_d = 1
    score = 0
    pos = (0,0)
    d = [(1,0), (0,1), (-1,0), (0,-1)]
    def get_neighbours(pos, direction):
        ret = []
        i, j = pos
        for (i_off, j_off), new_dir, new_score in [
                ((0,0), (direction-1)%4, 1000),
                (d[direction], direction, 1),
                ((0,0), (direction+1)%4, 1000)]:
            if grid[i+i_off][j+j_off] != '#':
                ret.append(((i+i_off,j+j_off), new_dir, new_score))
        return ret

    while q:
        while q:
            score, (pos, curr_d) = heappop(q)
            if (pos, curr_d) not in processed:
                break
        processed[(pos, curr_d)] = score
        if pos == end:
            break
        for new_pos, new_dir, new_score in get_neighbours(pos, curr_d):
            if (new_pos,new_dir) not in processed:
                heappush(q, (score+new_score, (new_pos, new_dir)))
    print('Part 1:', score)

    visited = set()
    def backtrack(pos, curr_d, score):
        visited.add(pos)
        i,j = pos
        for direction, _ in enumerate(d):
            if (pos, direction) in processed and processed[(pos, direction)] == score - 1000:
                backtrack(pos, direction, processed[(pos, direction)])
        neighbour = i - d[curr_d][0], j - d[curr_d][1]
        if (neighbour, curr_d) in processed and processed[(neighbour, curr_d)] == score - 1:
            backtrack(neighbour, curr_d, processed[(neighbour, curr_d)])
    backtrack(pos, curr_d, score)
    print('Part 2:', len(visited))
