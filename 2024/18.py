from enum import Enum
import time
import math
from heapq import heappush, heappop
from collections import defaultdict, deque

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

def get_input():
    with open("input/2024/18.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    failing_bytes = []
    for line in data.splitlines():
        failing_bytes.append(tuple(map(int, line.strip().split(","))))
    return failing_bytes 

def on_grid(x, y, N):
    return 0 <= x <= N and 0 <= y <= N

def check_safe(x, y, failing_bytes, fallen, N):
    return (x, y) not in failing_bytes[:fallen] and on_grid(x, y, N)

def print_grid(N, failing_bytes, fallen, positions):
    for y in range(N+1):
        for x in range(N+1):
            if (x, y) in failing_bytes[:fallen + 1]:
                print("#", end="")
            elif positions and (x, y) in positions:
                print("O", end="")
            else:
                print(".", end="")
        print()
    print()

def dijkstra(start, end, failing_bytes, fallen, N):
    Q = []

    heappush(Q, (0, start))
    prev = {}
    dist = defaultdict(lambda: math.inf)
    dist[start] = 0

    while Q:
        d, (x, y) = heappop(Q)

        if (x, y) == end:
            return dist[end], backtrack(start, end, prev)

        for dir in Dir:
            dx, dy = dir.value
            nx = x + dx
            ny = y + dy

            if not check_safe(nx, ny, failing_bytes, fallen, N):
                continue

            alt = d + 1 
            if alt < dist[(nx, ny)]:
                prev[(nx, ny)] = (x, y)
                dist[(nx, ny)] = alt
                heappush(
                    Q,
                    (
                        alt,
                        (nx, ny)
                    )
                )
    return None, None

def backtrack(start, end, prev):
    path = []
    curr = end
    while curr in prev:
        path.append(curr)
        curr = prev[curr]
    path.append(start)
    path.reverse()
    return path

def part1(): 
    failing_bytes = parse_input()
    N = 70
    fallen = 1024
    steps, path = dijkstra((0, 0), (N, N), failing_bytes, fallen, N)
    return steps

def part2():
    failing_bytes = parse_input()
    N = 70
    fallen = 1024
    _, path = dijkstra((0, 0), (N, N), failing_bytes, fallen, N)

    i = fallen
    while i < len(failing_bytes):
        if failing_bytes[i-1] in path:
            steps, path_2 = dijkstra((0, 0), (N, N), failing_bytes, i, N)
            if steps:
                path = path_2
            else:
                return f"{failing_bytes[i-1][0]},{failing_bytes[i-1][1]}"
        i += 1

if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
