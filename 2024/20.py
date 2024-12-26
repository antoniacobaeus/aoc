from enum import Enum
import time
import math
from heapq import heappush, heappop
from collections import defaultdict 

def get_input():
    with open("input/2024/20.txt", "r") as f:
        return f.read()

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

def parse_input():
    data = get_input();
    grid = []
    start, end = None, None
    for y, line in enumerate(data.splitlines()):
        if line.find("E") != -1:
            end = line.index("E"), y
        if line.find("S") != -1:
            start = line.index("S"), y
        grid.append(list(1 if l == "#" else 0 for l in line))
    return grid, start, end

def on_grid(grid, x, y):
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)

def dijkstra(grid, start, end):
    Q = []

    heappush(Q, (0, start))
    prev = defaultdict(list)
    dist = defaultdict(lambda: math.inf)
    dist[start] = 0

    while Q:
        d, (x, y) = heappop(Q)

        for dir in Dir:
            dx, dy = dir.value
            nx = x + dx
            ny = y + dy

            if not on_grid(grid, nx, ny) or grid[ny][nx]:
                continue

            alt = d + 1
            if alt < dist[(nx, ny)]:
                dist[(nx, ny)] = alt
                heappush(
                    Q,
                    (
                        alt,
                        (nx, ny)
                    )
                )
    return dist

def solve(grid, start, end, dist_to_start, dist_to_end, radius):
    dist = []
    for x, y in dist_to_end:
        for nx, ny in dist_to_start:
            d = abs(nx-x) + abs(ny-y)
            if d <= radius:
                dist.append(d + dist_to_end[(x, y)] + dist_to_start[(nx, ny)])
    return dist

def part1(): 
    grid, start, end = parse_input()
    max_skips = 2
    dist_to_end = dijkstra(grid, end, start)
    best_no_cheat = dist_to_end[start]
    dist_to_start = dijkstra(grid, start, end)
    dist_skips = solve(grid, start, end, dist_to_start, dist_to_end, max_skips)

    return len(list(filter(lambda d: best_no_cheat - d >= 100, dist_skips)))

def part2():
    grid, start, end = parse_input()
    max_skips = 20
    dist_to_end = dijkstra(grid, end, start)
    best_no_cheat = dist_to_end[start]
    dist_to_start = dijkstra(grid, start, end)
    dist_skips = solve(grid, start, end, dist_to_start, dist_to_end, max_skips)

    return len(list(filter(lambda d: best_no_cheat - d >= 100, dist_skips)))

if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
