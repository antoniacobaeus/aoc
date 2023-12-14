from enum import Enum


def parse_input(data):
    a = []
    for line in data.strip().split("\n"):
        a.append(list(line.strip()))
    return a


def part1(data):
    grid = parse_input(data)

    grid = tilt(grid, Dir.north)

    return calc_score(grid)


class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)


def find_first_rock(grid, x, y, dir: Dir):
    match dir:
        case Dir.north:
            for ny in range(y - 1, -1, -1):
                if grid[ny][x] in "#O":
                    return x, ny
            return x, -1
        case Dir.west:
            for nx in range(x - 1, -1, -1):
                if grid[y][nx] in "#O":
                    return nx, y
            return -1, y
        case Dir.south:
            for ny in range(y + 1, len(grid)):
                if grid[ny][x] in "#O":
                    return x, ny
            return x, len(grid)
        case Dir.east:
            for nx in range(x + 1, len(grid[y])):
                if grid[y][nx] in "#O":
                    return nx, y
            return len(grid[y]), y


def tilt(grid, dir: Dir):
    dx, dy = dir.value
    rows = enumerate(grid) if dy <= 0 else reversed(list(enumerate(grid)))

    for y, row in rows:
        columns = enumerate(row) if dx <= 0 else reversed(list(enumerate(row)))
        for x, c in columns:
            if c == "O":
                nx, ny = find_first_rock(grid, x, y, dir)
                grid[y][x] = "."
                grid[ny + (dy * -1)][nx + (dx * -1)] = "O"
    return grid


def to_tuple(grid):
    return tuple(tuple(r) for r in grid)


def calc_score(grid):
    s = 0
    for y, row in enumerate(grid):
        for c in row:
            if c == "O":
                s += len(grid) - y
    return s


def cycle_length(before, after, cache):
    s = 1  # include before -> after
    while after != before:
        after = cache[after]
        s += 1
    return s


def part2(data, cycles=1000000000):
    grid = parse_input(data)

    cache = {}
    i = 0
    cycle = 0
    while i < cycles:
        before = to_tuple(grid)
        for d in Dir:
            grid = tilt(grid, d)
        after = to_tuple(grid)

        if not cycle and after in cache:
            cycle = cycle_length(before, after, cache)
            i += cycle * ((1000000000 - i) // cycle)

        cache[before] = after
        i += 1
    return calc_score(grid)


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
    assert p2 == 64, f"Part2 does not match example, {p2} != {64}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
