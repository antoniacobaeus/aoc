from enum import Enum
import time

def get_input():
    with open("input/2024/10.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();

    m = []
    for line in data.strip().split("\n"):
        m.append(list(map(int, line.strip())))

    return m

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

def on_grid(grid, x, y):
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)

def bfs(grid, sx, sy, multi_paths=False):
    seen = set()
    queue = [(sx, sy)]

    r = 0
    while (queue):
        x, y = queue.pop()
        if (not multi_paths and (x, y) in seen):
            continue
        seen.add((x, y))
        v = grid[y][x]
        if (v == 9):
            r += 1
            continue
        for dir in Dir:
            dx, dy = dir.value
            nx = x + dx
            ny = y + dy
            if (on_grid(grid, nx, ny) and grid[ny][nx] - v == 1):
                queue.append((x + dx, y + dy))
    return r, seen

def part1(): 
    m = parse_input()

    r = 0
    for y in range(len(m)):
        for x in range(len(m[y])): 
            if (m[y][x] == 0):
                r += bfs(m, x, y)[0]
    return r


def part2():
    m = parse_input()

    r = 0
    for y in range(len(m)):
        for x in range(len(m[y])): 
            if (m[y][x] == 0):
                r += bfs(m, x, y, True)[0]
    return r

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
