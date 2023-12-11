import re
from itertools import combinations


def parse_input(data):
    grid = []
    galaxy = []
    for y, line in enumerate(data.splitlines()):
        grid.append(list(line))
        for match in re.finditer(r"\#", line):
            galaxy.append((match.start(), y))
    empty_rows = []
    for y, row in enumerate(grid):
        if all(c == "." for c in row):
            empty_rows.append(y)
    empty_cols = []
    for x in range(len(grid[0])):
        if all(grid[y][x] == "." for y in range(len(grid))):
            empty_cols.append(x)
    return galaxy, empty_rows, empty_cols


def distances(galaxy, empty_rows, empty_cols, mult=2):
    distances = []

    for pg, ng in combinations(galaxy, 2):
        x, y = pg
        nx, ny = ng

        xr = range(min(x, nx), max(x, nx))
        yr = range(min(y, ny), max(y, ny))
        ex = sum(x in xr for x in empty_cols)
        ey = sum(y in yr for y in empty_rows)

        d = abs(nx - x) + (abs(ny - y)) + (ex * (mult - 1)) + (ey * (mult - 1))
        distances.append(d)
    return distances


def part1(data):
    galaxy, empty_rows, empty_cols = parse_input(data)

    return sum(distances(galaxy, empty_rows, empty_cols))


def part2(data, mult):
    galaxy, empty_rows, empty_cols = parse_input(data)

    return sum(distances(galaxy, empty_rows, empty_cols, mult))


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
    p2 = part2(ex.input_data, 10)
    assert p2 == 1030, f"Part2 does not match example, {p2} != {1030}"

    p2 = part2(ex.input_data, 100)
    assert p2 == 8410, f"Part2 does not match example, {p2} != {8410}"

    s = time.perf_counter()
    p2 = part2(data, 1000000)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
