from enum import Enum
import time
from itertools import permutations
import math
from heapq import heappush, heappop
from functools import cache

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        match self:
            case Dir.north:
                return "^"
            case Dir.west:
                return "<"
            case Dir.south:
                return "v"
            case Dir.east:
                return ">"

    def __repr__(self):
        return str(self)

    def from_tuple(t):
        dx, dy = t

        return [Dir.north for _ in range(dy, 0)] + \
            [Dir.south for _ in range(0, dy)] + \
            [Dir.east for _ in range(0, dx)] + \
            [Dir.west for _ in range(dx, 0)]


def get_input():
    with open("input/2024/21.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    return data.splitlines()

num_pad = frozenset({
    "A": (2, 3),
    "0": (1, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
}.items())

dir_pad = frozenset({
    Dir.north: (1, 0),
    "A": (2, 0),
    Dir.west: (0, 1),
    Dir.south: (1, 1),
    Dir.east: (2, 1),
}.items())

def check_valid(start, dirs, pad):
    x, y = start
    for dir in dirs:
        dx, dy = dir.value
        x += dx
        y += dy

        if (x, y) not in dict(pad).values():
            return False
    return True

@cache
def min_length(pad, seq, depth):
    if depth == 0:
        return len(seq)

    x, y = dict(pad)["A"]

    res = []
    for t in seq:
        tx, ty = dict(pad)[t]
        dx, dy = tx - x, ty - y

        dirs = Dir.from_tuple((dx, dy))

        inner = math.inf
        for s in set(permutations(dirs)):
            if not check_valid((x, y), s, pad):
                continue
            inner = min(inner, min_length(dir_pad, s + ("A", ),depth - 1))
        x, y = tx, ty
        res.append(inner)
    return sum(res)

def part1(): 
    codes = parse_input()

    res = 0
    for c in codes:
        l = min_length(num_pad, c, 3)
        n = int(c[:-1])
        res += l * n
    return res
    # You (dir_pad) -> dir_pad * 2 -> num_pad => depth = 3

def part2():
    codes = parse_input()

    res = 0
    for c in codes:
        l = min_length(num_pad, c, 26)
        n = int(c[:-1])
        res += l * n
    return res
    # You (dir_pad) -> dir_pad * 25 -> num_pad => depth = 26

if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
