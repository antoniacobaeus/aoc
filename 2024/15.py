from enum import Enum
import time
from itertools import combinations
import math
import re
from copy import deepcopy

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

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

def get_input():
    with open("input/2024/15.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    grid_data, dirs_data = data.split("\n\n")
    grid = []
    for y, line in enumerate(grid_data.splitlines()):
        if line.find("@") != -1:
            start = line.index("@"), y
        grid.append(list(line.replace("@", ".")))
    dirs = []
    for line in dirs_data.splitlines():
        for d in line:
            dirs.append(Dir.from_char(d))
    return grid, dirs, start

def print_grid(grid, sx, sy):
    for y, _ in enumerate(grid):
        for x, l in enumerate(grid[y]):
            if (x, y) == (sx, sy):
                print("@", end="")
            else:
                print(l, end="")
        print()

def can_move(grid, x, y, dir): 
    dx, dy = dir.value

    nx, ny = x, y
    while (grid[ny][nx] != "#"):
        nx += dx
        ny += dy
        if grid[ny][nx] == ".":
            return (nx, ny)
    return None

def push(grid, x, y, dir):
    pos = can_move(grid, x, y, dir)
    if not pos:
        return False 

    dx, dy = dir.value
    nx, ny = pos
    while (nx, ny) != (x, y):
        if dy != 0 and grid[ny][nx] == "[":
            pushed = push(grid, nx + 1, ny, dir)
            if not pushed:
                return False
        elif dy != 0 and grid[ny][nx] == "]":
            pushed = push(grid, nx - 1, ny, dir)
            if not pushed:
                return False 
        grid[ny][nx] = grid[ny - dy][nx - dx]
        ny -= dy
        nx -= dx
    grid[ny][nx] = "."
    return True

def move(grid, x, y, dir, pair=False):
    dx, dy = dir.value
    val = grid[y + dy][x + dx]

    new_grid = deepcopy(grid)
    pushed = push(new_grid, x, y, dir)
    if pushed:
        x += dx
        y += dy
        grid = new_grid
    return grid, x, y

def part1(data): 
    grid, dirs, (x, y) = parse_input()

    for dir in dirs:
        grid, x, y = move(grid, x, y, dir)

    r = 0
    for y in range(len(grid)):
        for x, l in enumerate(grid[y]):
            if l == "O":
                r += 100 * y + x
    return r

def expand_grid(grid):
    new_grid = []
    for y in range(len(grid)):
        new_grid.append([])
        for x, l in enumerate(grid[y]):
            if l == "#":
                new_grid[y].append("#")
                new_grid[y].append("#")
            elif l == ".":
                new_grid[y].append(".")
                new_grid[y].append(".")
            else:
                new_grid[y].append("[")
                new_grid[y].append("]")
    return new_grid

def part2(data):
    grid, dirs, (sx, sy) = parse_input()
    grid = expand_grid(grid)

    x = sx * 2
    y = sy

    # print_grid(grid, x, y)
    for dir in dirs:
        grid, x, y = move(grid, x, y, dir)
        # print_grid(grid, x, y)

    r = 0
    for y in range(len(grid)):
        for x, l in enumerate(grid[y]):
            if l == "[":
                r += 100 * y + x
    return r

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
