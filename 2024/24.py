from enum import Enum
import time
from itertools import permutations
import math
import re
from heapq import heappush, heappop
from collections import defaultdict, deque
from copy import deepcopy
import graphviz

def get_input():
    with open("input/2024/24.txt", "r") as f:
        return f.read()

def parse_input(data):
    values = {}
    for match in re.finditer(r"(\w+): (\d)", data):
        values[match.group(1)] = int(match.group(2))
    functions = {}
    for match in re.finditer(r"(\w+) (\w+) (\w+) -> (\w+)", data):
        functions[match.group(4)] = (match.group(1), match.group(2), match.group(3))
    return values, functions

operations = {
    "XOR": lambda x, y: x ^ y,
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y
}

def solve(k, values, seen):
    if isinstance(values[k], int):
        return values[k]

    if k in seen:
        return -1
    seen.add(k)

    l, op, r = values[k]
    left = solve(l, values, seen)
    right = solve(r, values, seen)

    if left == -1 or right == -1:
        return -1
    values[k] = operations[op](left, right)

    return values[k]

def build_graph(values, functions):
    dot = graphviz.Digraph(comment="graph")

    for k, (left, op, right) in functions.items():
        dot.node(op + k)
        dot.edge(left, op + k)
        dot.edge(right, op + k)
        dot.edge(op + k, k)
    with open("graph.dot", "w") as f:
        f.write(str(dot))

def get_num(values, c):
    zs = sorted((k for k in values if k.startswith(c)), reverse=True)
    return int("".join((str(values[z])) for z in zs), 2)

def part1(data): 
    values, functions = parse_input(data)
    merged = values | functions

    for k in merged:
        solve(k, merged, set())

    return get_num(merged, "z")

def part2(data):
    values, functions = parse_input(data)

    # creates graph.dot
    build_graph(values, functions)
    # dot -Tsvg graph.dot > graph.svg
    
    x = get_num(values, "x")
    y = get_num(values, "y")

    merged = values | functions

    for k in merged:
        solve(k, merged, set())
    z = get_num(merged, "z")

    print("invalid bits:")
    for i, (z1, z2) in enumerate(zip(bin(x + y)[::-1], bin(z)[::-1])):
        if z1 != z2:
            print(f"z{i}") 



if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
