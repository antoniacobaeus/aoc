import time
import re
from collections import defaultdict
from os import system, name

def clear():
    if name == 'nt': # windows
        _ = system('cls')
    else:
        _ = system('clear')

filled_symbol = "#"
empty_symbol = "."

def get_input():
    with open("input/2024/14.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    robots = defaultdict(list)
    for match in re.finditer(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", data):
        x, y = int(match.group(1)), int(match.group(2))
        dx, dy = int(match.group(3)), int(match.group(4))
        robots[(x, y)].append((dx, dy))

    return robots

def step(robots, w, h):
    new_robots = defaultdict(list)
    for x, y in robots:
        while(robots[(x, y)]):
            dx, dy = robots[(x, y)].pop()
            # assert(((x + dx) % w, (y + dy) % h) != (x, y))
            new_robots[((x + dx) % w, (y + dy) % h)].append((dx, dy))
    return new_robots

def count_quadrant(robots, min_x, min_y, max_x, max_y):
    return sum(len(robots[(x, y)]) for x, y in robots if min_x <= x < max_x and min_y <= y < max_y)

def count_quadrants(robots, w, h):
    mid_x = w // 2
    mid_y = h // 2

    return (
        count_quadrant(robots, 0, 0, mid_x, mid_y),
        count_quadrant(robots, mid_x + 1, 0, w, mid_y),
        count_quadrant(robots, 0, mid_y + 1, mid_x, h),
        count_quadrant(robots, mid_x + 1, mid_y + 1, w, h)
    )

def print_grid(robots, w, h):
    for y in range(h):
        for x in range(w):
            if (x, y) in robots:
                print("#", end="")
            else:
                print(".", end="")
        print()

def grid_string(robots, w, h):
    s = "" 
    for y in range(h):
        for x in range(w):
            if (x, y) in robots:
                s += filled_symbol
            else:
                s += empty_symbol
        s += "\n"
    return s

def part1(): 
    robots = parse_input()
    w, h = 101, 103
    for _ in range(100):
        robots = step(robots, w, h)

    r = 1
    for c in count_quadrants(robots, w, h):
        r *= c
    return r

def check_cross(robots, x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx != 0 and dy != 0):
                continue
            if not (x + dx, y + dy) in robots:
                return False
    return True
                
def part2():
    robots = parse_input()
    w, h = 101, 103
    i = 0
    while (True):
        i += 1
        robots = step(robots, w, h)
        if any(check_cross(robots, x, y) for x, y in robots):
            clear() 
            print(i)
            print(grid_string(robots, w, h))
            time.sleep(1)

if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
