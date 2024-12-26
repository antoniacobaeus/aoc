from enum import Enum
import time
from itertools import combinations
import math
import re
from functools import cache

def get_input():
    with open("input/2024/19.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    patterns, designs = data.split("\n\n")
    patterns = tuple(patterns.split(", "))
    designs = designs.splitlines()
    return patterns, designs

@cache
def check_design(design, patterns):
    if not design:
        return 1
    return sum(design[:i+1] in patterns and check_design(design[i+1:], patterns) for i in range(len(design)))


def part1(data): 
    patterns, designs = parse_input()
    
    return len(list(filter(lambda d: check_design(d, patterns), designs)))
                
def part2(data):
    patterns, designs = parse_input()

    return sum(map(lambda d: check_design(d, patterns), designs))

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
