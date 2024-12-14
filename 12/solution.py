import sys

with open(sys.argv[1]) as f:
    grid = []
    for r in f:
        grid.append(r.strip('\n'))

    directions = [(-1,0),(0,1),(1,0),(0,-1)]
    regions = dict()

    def region(i, j, visited, c):
        visited.add((i,j))
        for i_off, j_off in directions:
            i_ = i+i_off
            j_ = j+j_off
            if 0 <= i_ < len(grid) and 0 <= j_ < len(grid) and (i_,j_) not in visited and grid[i_][j_] == c:
                region(i_, j_, visited, c)
    def walls(i, j, h, c, cells):
        w = 0
        start_i = i
        start_j = j
        hand = h
        move = (h + 1) % 4
        hand_start = directions[hand]
        move_start = directions[move]
        while True:
            cells.add((i,j,hand))
            i_move, j_move = directions[move]
            i_hand, j_hand = directions[hand]
            if 0 <= i+i_hand < len(grid) and 0 <= j+j_hand < len(grid) and  grid[i+i_hand][j+j_hand] == c:
                # Can turn left
                w += 1
                i += i_hand
                j += j_hand
                hand = (hand - 1) % 4
                move = (move - 1) % 4
            elif 0 <= i+i_move < len(grid) and 0 <= j+j_move < len(grid) and  grid[i+i_move][j+j_move] == c:
                # Can move forward
                i += i_move
                j += j_move
            else:
                # Turn right
                w += 1
                hand = (hand + 1) % 4
                move = (move + 1) % 4
            if i == start_i and j == start_j and directions[hand] == hand_start and directions[move] == move_start:
                break
        return w

    done = set()
    s = 0
    s2 = 0
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if (i,j) not in done:
                reg = set()
                region(i, j, reg, c)
                area = len(reg)
                wall_cells = set()
                ws = 0
                fences = 0
                for x, y in reg:
                    done.add((x,y))
                    for d, (x_off, y_off) in enumerate(directions):
                        if not( 0 <= x+x_off < len(grid) and 0 <= y+y_off < len(grid) and  grid[x+x_off][y+y_off] == c):
                            fences += 1
                            wall_cells.add((x,y,d))
                while len(wall_cells) > 0:
                    x, y, direction = list(wall_cells)[0]
                    visited = set()
                    ws += walls(x,y,direction,c,visited)


                    for coord in visited:
                        if coord in wall_cells:
                            wall_cells.remove(coord)
                s += area * fences
                s2 += area * ws

    print('Part 1:',s)
    print('Part 2:', s2)
