from enum import Enum
import time
from itertools import combinations
import math

def get_input():
    with open("input/2024/07.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();

    m = []
    for line in data.strip().split("\n"):
        line = line.strip().split(":")
        m.append((int(line[0].strip()), list(map(int, line[1].strip().split(" ")))))

    return m

def merge(v1, v2):
    return v1 * (10 ** (math.floor(math.log10(v2) + 1))) + v2

def solve(res, values, val, can_merge=False):
    if val == res and not values:
        return True
    elif not values or val > res:
        return False
    
    v, rest = values[0], values[1:]
    return any((
        solve(res, rest, val + v, can_merge),
        solve(res, rest, val * v, can_merge),
        solve(res, rest, merge(val, v), can_merge) if can_merge else False
    ))

def part1(data): 
    m = parse_input()
    return sum(res if solve(res, values[1:], values[0]) else 0 for res, values in m)

def part2(data):
    m = parse_input()
    return sum(res if solve(res, values[1:], values[0], True) else 0 for res, values in m)

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
