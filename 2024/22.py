from enum import Enum
import time
from itertools import combinations
import math
import re
from heapq import heappush, heappop
from collections import defaultdict, deque
from functools import cache

def get_input():
    with open("input/2024/22.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    return list(map(int, data.splitlines()))

def mix(s, r):
    return s ^ r

def prune(s):
    return s % 16777216

def evolve(s):
    # 1.
    r = s * 64
    s = mix(s, r)
    s = prune(s)

    # 2.
    r = s // 32
    s = mix(s, r)
    s = prune(s)

    # 3.
    r = s * 2048
    s = mix(s, r)
    s = prune(s)

    return s

def last_digit(s):
    return s % 10

def part1(): 
    init_secrets = parse_input()
    evolved = []
    for s in init_secrets:
        for _ in range(2000):
            s = evolve(s)
        evolved.append(s)
    return sum(evolved)

def part2():
    init_secrets = parse_input()

    sequences = defaultdict(list)
    for s in init_secrets:
        diffs = []
        last_price = last_digit(s)
        used_sequences = set()
        last_sequence = None
        for i in range(2000):
            s = evolve(s)
            diffs.append(last_digit(s) - last_price)
            last_price = last_digit(s)
            if len(diffs) >= 4:
                sequence = tuple(diffs[len(diffs) - 4:])
                if sequence not in used_sequences:
                    sequences[sequence].append(last_digit(s))
                    used_sequences.add(sequence)
    return max(map(sum, sequences.values()))

if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
