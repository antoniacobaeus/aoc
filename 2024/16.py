from enum import Enum
import time
from itertools import combinations
import math
import re
from heapq import heappush, heappop
from collections import defaultdict, deque

def get_input():
    with open("input/2024/16.txt", "r") as f:
        return f.read()

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)


    def __lt__(self, other):
        return self.value < other.value

    def from_char(c):
        match c:
            case ">":
                return Dir.east
            case "v":
                return Dir.south
            case "<":
                return Dir.west
            case "^":
                return Dir.north

    def turn(self, clockwise=True):
        match self:
            case Dir.north:
                dir = Dir.east
            case Dir.east:
                dir = Dir.south
            case Dir.south:
                dir = Dir.west
            case Dir.west:
                dir = Dir.north
        return dir if clockwise else dir.opposite()
    
    def opposite(self):
        match self:
            case Dir.north:
                return Dir.south
            case Dir.south:
                return Dir.north
            case Dir.east:
                return Dir.west
            case Dir.west:
                return Dir.east

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

    heappush(Q, (0, start, Dir.east))
    prev = defaultdict(list)
    dist = defaultdict(lambda: math.inf)

    while Q:
        d, (x, y), curr_dir = heappop(Q)

        new_dirs = [curr_dir, curr_dir.turn(), curr_dir.turn(False)]
        for dir in new_dirs:
            dx, dy = dir.value
            nx = x + dx
            ny = y + dy

            if not on_grid(grid, nx, ny) or grid[ny][nx]:
                continue

            alt = d + 1 if dir == curr_dir else d + 1001
            if alt < dist[(nx, ny, dir)]:
                prev[(nx, ny, dir)].clear()
                prev[(nx, ny, dir)].append((x, y, curr_dir))
                dist[(nx, ny, dir)] = alt
                heappush(
                    Q,
                    (
                        alt,
                        (nx, ny),
                        dir
                    )
                )
            elif alt == dist[(nx, ny, dir)]:
                prev[(nx, ny, dir)].append((x, y, curr_dir))

    return dist, prev

def print_prev(grid, positions, start, end):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) == start:
                print("S", end="")
            elif (x, y) == end:
                print("E", end="")
            elif (x, y) in ((x, y) for x, y, _ in positions):
                print("O", end="")
            else:
                print("#" if grid[y][x] else ".", end="")
        print()

def backtrack(paths, path, prev, curr):
    if (curr not in prev):
        paths.append(path[:])
        return 

    for p in prev[curr]:
        path.append(curr)
        backtrack(paths, path, prev, p)
        path.pop()

def part1(): 
    grid, start, end = parse_input()
    dist, prev = dijkstra(grid, start, end)
    paths_to_end = list(dist[x, y, dir] for x, y, dir in dist if (x, y) == end)
    return min(paths_to_end)

def part2():
    grid, start, end = parse_input()
    dist, prev = dijkstra(grid, start, end)
    paths_to_end = list((x, y, dir) for x, y, dir in dist if (x, y) == end)
    min_path = min(paths_to_end, key=lambda x: dist[x])

    paths = []
    backtrack(paths, [], prev, min_path)
    res = set()
    for path in paths:
        res |= set((x, y) for x, y, _ in path)
    return len(res) + 1


if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
