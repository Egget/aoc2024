import sys
import heapq

def a_star(grid_width, grid_height, obstacles, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def is_valid(coord):
        x, y = coord
        return 0 <= x < grid_width and 0 <= y < grid_height and coord not in obstacles

    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            return g_score[current]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbour = (current[0] + dx, current[1] + dy)
            if is_valid(neighbour):
                tentative_g_score = g_score[current] + 1
                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + heuristic(neighbour, end)
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))

    return -1

with open(sys.argv[1]) as f:
    obstacles = list(map(lambda s: tuple(map(int, s.split(','))), f.read().split('\n')[:-1]))
    print('Part 1: ', a_star(71,71,set(obstacles[:1024]), (0,0), (70,70)))

    s = 1024

    while a_star(71,71,set(obstacles[:s]), (0,0), (70,70)) > 0:
        s += 1

    print('Part 2:', obstacles[s-1])
