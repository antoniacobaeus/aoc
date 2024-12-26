from enum import Enum
import time
from functools import cache

def get_input():
    with open("input/2024/11.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    return list(map(int, data.strip().split()))

@cache
def transform(stone):
    if (stone == 0):
        return (1, )
    elif (len(str(stone)) % 2 == 0):
        l = str(stone)
        left = int(l[:len(l)//2])
        right = int(l[len(l)//2:])
        return (left, right)
    else:
        return (stone * 2024, )

@cache
def blink(stone, t):
    if t == 0:
        return 1
    return sum(map(lambda s: blink(s, t-1), transform(stone)))

def part1(): 
    stones = tuple(parse_input())
    
    return sum(map(lambda s: blink(s, 25), stones))

def part2(): 
    stones = tuple(parse_input())

    return sum(map(lambda s: blink(s, 75), stones))

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
