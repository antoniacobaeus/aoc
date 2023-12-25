from itertools import combinations
import numpy as np


def parse_input(data):
    hails = []
    for line in data.strip().split("\n"):
        pos, vel = line.split(" @ ")
        pos = tuple(map(int, pos.split(", ")))
        vel = tuple(map(int, vel.split(", ")))
        hails.append((pos, vel))
    return hails


def get_slope(pos, vel):
    x, y, _ = pos
    dx, dy, _ = vel
    x2 = x + dx
    y2 = y + dy
    return (y2 - y) / (x2 - x)


def get_y_intercept(pos, m):
    x, y, _ = pos
    return y - m * x


def get_intersection(pos1, vel1, pos2, vel2):
    a = get_slope(pos1, vel1)
    b = get_slope(pos2, vel2)

    if a == b:
        # print("parallel")
        return None, None

    c = get_y_intercept(pos1, a)
    d = get_y_intercept(pos2, b)

    x, y = ((d - c) / (a - b), a * (int((d - c) / (a - b))) + c)
    x1 = (y - c) / a
    x2 = (y - d) / b

    if vel1[0] < 0 and x1 > pos1[0] or vel1[0] > 0 and x1 < pos1[0]:
        # print("collision occurs in the past for A")
        return None, None
    elif vel2[0] < 0 and x2 > pos2[0] or vel2[0] > 0 and x2 < pos2[0]:
        # print("collision occurs in the past for B")
        return None, None

    return x, y


def part1(data, start, end):
    hails = parse_input(data)

    s = 0
    for (pos1, vel1), (pos2, vel2) in combinations(hails, 2):
        x, y = get_intersection(pos1, vel1, pos2, vel2)

        if x is None or y is None:
            # print(f"intersection out of bounds at {x} {y}")
            continue

        if start <= x <= end and start <= y <= end:
            # print(f"intersection at {x} {y}")

            s += 1
        else:
            pass
            # print(f"intersection out of bounds at {x} {y}")

    return s


def part2(data):
    hails = parse_input(data)

    potential = [set(), set(), set()]  # x  # y  # z
    for (pos1, vel1), (pos2, vel2) in combinations(hails, 2):
        for i, ((p1, v1), (p2, v2)) in enumerate(zip(zip(pos1, vel1), zip(pos2, vel2))):
            if v1 == v2:
                temp = set()
                diff = p2 - p1
                for v in range(-1000, 1000):
                    if v == v1:
                        continue
                    if diff % (v - v1) == 0:
                        temp.add(v)

                if not potential[i]:
                    potential[i] |= temp
                else:
                    potential[i] &= temp
    assert all(len(p) == 1 for p in potential)
    dxr, dyr, dzr = (p.pop() for p in potential)

    pos1, (dx1, dy1, dz1) = hails[0]
    pos2, (dx2, dy2, dz2) = hails[1]
    vel1 = (dx1 - dxr, dy1 - dyr, dz1 - dzr)
    vel2 = (dx2 - dxr, dy2 - dyr, dz2 - dzr)

    x, y = get_intersection(pos1, vel1, pos2, vel2)

    t = (x - pos1[0]) / vel1[0]
    z = pos1[2] + vel1[2] * t

    print(x, y, z)
    return sum(map(int, (x, y, z)))


if __name__ == "__main__":
    import time
    import os
    from aocd.models import Puzzle
    from aocd import submit

    DAY = int(os.path.basename(__file__).removesuffix(".py"))
    YEAR = int(os.path.basename(os.path.dirname(__file__)))

    puzzle = Puzzle(year=YEAR, day=DAY)

    data = puzzle.input_data

    ex = puzzle.examples[0]

    # Part 1
    p1 = part1(ex.input_data, 7, 27)
    assert p1 == 2, f"Part1 does not match example, {p1} != {2}"

    s = time.perf_counter()
    p1 = part1(data, 200000000000000, 400000000000000)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    # p2 = part2(ex.input_data)
    # assert p2 == 47, f"Part2 does not match example, {p2} != {47}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    submit(p2, part="b", day=DAY, year=YEAR)
