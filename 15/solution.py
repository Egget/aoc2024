import sys

with open(sys.argv[1]) as f:
    grid = []
    grid2 = []
    moves = []
    r_i = 0
    r_j = 0
    for i, r in enumerate(f):
        if r[0] == '#':
            row = []
            row.extend(r.strip('\n'))
            row2 = []
            for c in r:
                if c == '.':
                    row2.extend('..')
                elif c == '#':
                    row2.extend('##')
                elif c == 'O':
                    row2.extend('[]')
                elif c == '@':
                    row2.extend('@.')
            if '@' in row:
                r_i = i
                r_j = row.index('@')
                r_i2 = i
                r_j2 = row2.index('@')
            grid.append(row)
            grid2.append(row2)
        else:
            moves.extend(r.strip('\n'))
    d = {
        '^': (-1, 0),
        '<': (0, -1),
        '>': (0, 1),
        'v': (1, 0),
    }
    def move(i, j, m, grid=grid):
        i_off, j_off = d[m]
        i_next = i + i_off
        j_next = j + j_off
        curr = grid[i][j]
        nxt = grid[i_next][j_next]
        moved = False
        if nxt == '#':
            moved = False
        elif nxt == 'O':
            moved, _, _ = move(i + i_off, j + j_off, m, grid)
        elif nxt == '.':
            moved = True
        elif nxt == '[':
            if m in ('v', '^'):
                i_2, j_2 = d['>']
                if move2(i_next,j_next,i_next+i_2,j_next+j_2,m,dry_run = True):
                    moved = move2(i_next,j_next,i_next+i_2,j_next+j_2,m)
                else:
                    moved = False
            else:
                moved, _, _ = move(i + i_off, j + j_off, m, grid)
        elif nxt == ']':
            if m in ('v', '^'):
                i_2, j_2 = d['<']
                if move2(i_next+i_2,j_next+j_2,i_next,j_next,m,dry_run = True):
                    moved = move2(i_next+i_2,j_next+j_2,i_next,j_next,m)
                else:
                    moved = False
            else:
                moved, _, _ = move(i + i_off, j + j_off, m, grid)
        if moved:
            grid[i_next][j_next] = curr
            grid[i][j] = '.'
            return True, i_next, j_next
        return False, i, j

    def move2(il,jl,ir,jr,m,dry_run=False):
        i_off, j_off = d[m]
        il_next = il + i_off
        jl_next = jl + j_off
        ir_next = ir + i_off
        jr_next = jr + j_off
        currl = grid2[il][jl]
        currr = grid2[ir][jr]
        nxtl = grid2[il_next][jl_next]
        nxtr = grid2[ir_next][jr_next]
        moved = False
        if nxtl == '#' or nxtr == '#':
            moved = False
        elif nxtl == '[':
            moved = move2(il_next,jl_next,ir_next,jr_next,m,dry_run)
        elif nxtl == ']' and nxtr == '[':
            i_2, j_2 = d['<']
            i_3, j_3 = d['>']
            movedl = move2(il_next+i_2,jl_next+j_2,il_next,jl_next,m,dry_run)
            movedr = move2(ir_next,jr_next,ir_next+i_3,jr_next+j_3,m,dry_run)
            moved = movedr and movedl
        elif nxtl == ']':
            i_2, j_2 = d['<']
            moved = move2(il_next+i_2,jl_next+j_2,il_next,jl_next,m,dry_run)
        elif nxtr == '[':
            i_3, j_3 = d['>']
            moved = move2(ir_next,jr_next,ir_next+i_3,jr_next+j_3,m,dry_run)
        else:
            moved = True
        if moved and not dry_run:
            grid2[il_next][jl_next] = currl
            grid2[ir_next][jr_next] = currr
            grid2[il][jl] = '.'
            grid2[ir][jr] = '.'
        return moved


    for m in moves:
        _, new_i, new_j = move(r_i, r_j, m)
        r_i = new_i
        r_j = new_j
    total = 0
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if c == 'O':
                total += 100*i + j
    print('Part 1:', total)
    for m in moves:
        _, new_i, new_j = move(r_i2, r_j2, m,grid=grid2)
        r_i2 = new_i
        r_j2 = new_j
    total = 0
    for i, r in enumerate(grid2):
        for j, c in enumerate(r):
            if c == '[':
                total += 100*i + j
    print('Part 2:', total)
