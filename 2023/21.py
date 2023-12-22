from enum import Enum
import numpy as np


def parse_input(data):
    grid = []
    for line in data.strip().split("\n"):
        grid.append(list(line.strip()))
    return grid


class Dir(Enum):
    east = (1, 0)
    south = (0, 1)
    west = (-1, 0)
    north = (0, -1)


def move(curr, dir):
    x, y = curr
    dx, dy = dir.value
    return (x + dx, y + dy)


def reachable(grid, start, max_steps):
    even, odd = set(), set()

    Q = [(start, 0)]
    while Q:
        curr, steps = Q.pop(0)

        if curr in even or curr in odd:
            continue

        if steps % 2 == 0:
            even.add(curr)
        else:
            odd.add(curr)

        if steps == max_steps:
            continue

        for dir in [Dir.east, Dir.south, Dir.west, Dir.north]:
            nx, ny = move(curr, dir)
            c = grid[ny % len(grid)][nx % len(grid[0])]

            if c in ".S":
                Q.append(((nx, ny), steps + 1))
    return even if max_steps % 2 == 0 else odd


def print_grid(grid, visited):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y) in visited:
                print("O", end="")
            else:
                print(c, end="")
        print()


def part1(data, max_steps):
    grid = parse_input(data)

    start = next(
        (x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == "S"
    )

    r = reachable(grid, start, max_steps)
    return len(r)


def quadratic_interpolation(r1, r2, r3, x):
    # what is the function that fits the data points?
    # what is the value of the function at x?

    x0, y0 = r1
    x1, y1 = r2
    x2, y2 = r3

    """
    y0 = ax0^2 + bx0 + c
    y1 = ax1^2 + bx1 + c
    y2 = ax2^2 + bx2 + c
    """

    # langrange basis polynomials
    l0 = (x - x1) * (x - x2) // ((x0 - x1) * (x0 - x2))
    l1 = (x - x0) * (x - x2) // ((x1 - x0) * (x1 - x2))
    l2 = (x - x0) * (x - x1) // ((x2 - x0) * (x2 - x1))

    return y0 * l0 + y1 * l1 + y2 * l2


def least_squares(r, n):
    x = np.array([x for x, _ in r])
    y = np.array([y for _, y in r])

    a, b, c = np.polyfit(x, y, 2)
    return int(a * n**2 + b * n + c)


def part2(data, max_steps):
    grid = parse_input(data)

    start = next(
        (x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == "S"
    )

    steps = len(grid) // 2

    r = [
        (steps + len(grid) * i, len(reachable(grid, start, steps + len(grid) * i)))
        for i in range(3)
    ]

    # print(quadratic_interpolation(*r, max_steps))
    return least_squares(r, max_steps)


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
    p1 = part1(ex.input_data, 6)
    assert p1 == 16, f"Part1 does not match example, {p1} != {16}"

    s = time.perf_counter()
    p1 = part1(data, 64)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    # p2 = part2(ex.input_data, 6)
    # assert p2 == 16, f"Part2 does not match example, {p2} != {16}"

    # p2 = part2(ex.input_data, 10)
    # assert p2 == 50, f"Part2 does not match example, {p2} != {50}"

    # p2 = part2(ex.input_data, 50)
    # assert p2 == 1594, f"Part2 does not match example, {p2} != {1594}"

    # p2 = part2(ex.input_data, 100)
    # assert p2 == 6536, f"Part2 does not match example, {p2} != {6536}"

    # p2 = part2(ex.input_data, 500)
    # assert p2 == 167004, f"Part2 does not match example, {p2} != {167004}"

    # p2 = part2(ex.input_data, 1000)
    # assert p2 == 668697, f"Part2 does not match example, {p2} != {668697}"

    # p2 = part2(ex.input_data, 5000)
    # assert p2 == 16733044, f"Part2 does not match example, {p2} != {16733044}"

    s = time.perf_counter()
    p2 = part2(data, 26501365)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
