from enum import Enum
import time
from itertools import combinations
import math
import re

def get_input():
    with open("input/2024/08.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    grid = []
    galaxy = []
    for y, line in enumerate(data.splitlines()):
        grid.append(list(line))
        for match in re.finditer(r"(\d|[a-z]|[A-Z])", line):
            galaxy.append(((match.start(), y), match.group(1)))
    return galaxy, grid
        
def dist(a, b):
    x, y = a
    nx, ny = b
    return nx - x, ny - y

def on_grid(grid, x, y):
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)

def print_grid(grid, n):
    for y, _ in enumerate(grid):
        for x, l in enumerate(grid[y]):
            if (x, y) in n:
                print("#", end="")
            else:
                print(l, end="")
        print()


def part1(data): 
    galaxy, grid = parse_input()
    
    nodes = set()
    for a, aa in galaxy:
        for b, bb in galaxy:
            if (aa != bb or a == b):
                continue

            dx, dy = dist(a, b)
            ax, ay = a
            bx, by = b

            if (on_grid(grid, ax - dx, ay - dy)):
                nodes.add((ax - dx, ay - dy))

            if (on_grid(grid, bx + dx, by + dy)):
                nodes.add((bx + dx, by + dy))
    return len(nodes)
                
def part2(data):
    galaxy, grid = parse_input()
    
    nodes = set()
    for a, aa in galaxy:
        for b, bb in galaxy:
            if (aa != bb or a == b):
                continue

            dx, dy = dist(a, b)
            x, y = a
            while on_grid(grid, x, y):
                nodes.add((x, y))
                x += dx
                y += dy
    return len(nodes)

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
