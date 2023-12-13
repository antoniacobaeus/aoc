import numpy as np


def parse_input(data):
    groups = data.strip().split("\n\n")
    grids = []
    for group in groups:
        grid = []

        for line in group.strip().split("\n"):
            grid.append(["1" if l == "#" else "0" for l in line])
        grids.append(np.array(grid))
    return grids


def differ_by_one(a, b):
    x = a ^ b
    return x and (not (x & (x - 1)))


def to_edge(i, grid, fix):
    l, r = i, i + 1
    while l >= 0 and r < len(grid):
        a = int("".join(grid[l]), 2)
        b = int("".join(grid[r]), 2)
        if a != b:
            if fix and differ_by_one(a, b):
                fix = False
            else:
                return False
        l -= 1
        r += 1
    return not fix


def find_reflection(grid, fix):
    r, c = None, None
    for i, _ in enumerate(grid[:-1]):
        if to_edge(i, grid, fix):
            return i, None

    for j, _ in enumerate(grid.T[:-1]):
        if to_edge(j, grid.T, fix):
            return None, j

    return r, c


def solve(grids, fix=False):
    s = 0
    for grid in grids:
        r, c = find_reflection(grid, fix)
        if r is not None:
            s += (r + 1) * 100
        elif c is not None:
            s += c + 1
    return s


def part1(data):
    grids = parse_input(data)

    return solve(grids)


def part2(data):
    grids = parse_input(data)

    return solve(grids, fix=True)


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
    p1 = part1(ex.input_data)
    assert (
        str(p1) == ex.answer_a
    ), f"Part1 does not match example, {p1} != {ex.answer_a}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(ex.input_data)
    assert p2 == 400, f"Part2 does not match example, {p2} != {400}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
