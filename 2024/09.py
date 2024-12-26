from enum import Enum
import time
from itertools import combinations
import math

def get_input():
    with open("input/2024/09.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();

    disks = []
    for j, c in enumerate((data.strip())[::2]):
        d = int(c)
        i = j * 2
        f = 0
        if (i + 1 < len(data.strip())):
            f = int(data[i + 1])
        disks.append((d, f, j))

    return disks

def print_disks(disks):
    for (d, f, i) in disks:
        for _ in range(d):
            print(i, end="")
        for _ in range(f):
            print(".", end="")
    print()

# 6283665299144 too high
def part1(): 
    disks = parse_input()
    for i, (di, fi, ii) in enumerate(disks[::-1]):
        if (di == 0):
            continue
        for j, (dj, fj, ij) in enumerate(disks):
            if fj == 0:
                continue
            if len(disks) - (i + 1) <= j:
                break


            disks[j] = (dj, 0, ij)
            if fj > di:
                disks[-(i+1)] = (0, fi + di, ii)
                disks.insert(j+1, (di, fj - di, ii))
                break
            else: 
                disks[-(i+1)] = (di - fj, fi + fj, ii)
                di, fi, ii = disks[-(i+1)]
                disks.insert(j+1, (fj, 0, ii))
                # disks[j] = (dj, 0, ij)
 
    r = 0
    p = 0
    for (d, f, i) in disks:  
        for _ in range(d):
            r += (i * p)
            p += 1
    return r



def part2():
    disks = parse_input()
    for i, _ in enumerate(disks[::-1]):
        di, fi, ii = disks[-(i+1)] 
        if (di == 0):
            continue
        for j, (dj, fj, ij) in enumerate(disks):
            if fj == 0:
                continue
            if len(disks) - (i + 1) <= j:
                break

            if fj >= di:
                disks[j] = (dj, 0, ij)
                disks.insert(j+1, (di, fj - di, ii))
                disks[-(i+1)] = (0, fi + di, ii)
                break
    r = 0
    p = 0
    for (d, f, i) in disks:  
        for _ in range(d):
            r += (i * p)
            p += 1
        for _ in range(f):
            p += 1
    return r


if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
