import re


def parse_input(data):
    numbers = []
    grid = []
    gears = []
    for y, line in enumerate(data.strip().split("\n")):
        grid.append(list(line.strip()))
        for match in re.finditer(r"\d+", line):
            numbers.append((int(match.group()), (match.start(), y)))
        for match in re.finditer(r"\*", line):
            gears.append((match.start(), y))

    return grid, numbers, gears


def find_adjacent(grid, x, y, l):
    adj = []

    sx = max(x - 1, 0)
    sy = max(y - 1, 0)
    ex = min(x + l, len(grid[0]) - 1)
    ey = min(y + 1, len(grid) - 1)

    for ny in range(sy, ey + 1):
        for nx in range(sx, ex + 1):
            if ny == y and nx in range(x, x + l):
                continue
            adj.append((nx, ny))
    return adj


def part1(data):
    grid, numbers, _ = parse_input(data)

    s = 0
    for number, start in numbers:
        x, y = start

        adj = find_adjacent(grid, x, y, len(str(number)))

        if not all(grid[a[1]][a[0]] == "." for a in adj):
            s += number

    return s


def part2(data):
    grid, numbers, gears = parse_input(data)

    s = 0
    for pos in gears:
        x, y = pos

        adj = find_adjacent(grid, x, y, 1)

        adj_numbers = []
        for number, start in numbers:
            for nx in range(start[0], start[0] + len(str(number))):
                if (nx, start[1]) in adj:
                    adj_numbers.append(number)
                    break
        if len(adj_numbers) == 2:
            s += adj_numbers[0] * adj_numbers[1]
    return s


if __name__ == "__main__":
    import time
    import os
    from aocd.models import Puzzle
    from aocd import submit

    DAY = int(os.path.basename(__file__)[3:5])
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
    submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(ex.input_data)
    assert (
        str(p2) == ex.answer_b
    ), f"Part2 does not match example, {p2} != {ex.answer_b}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    submit(p2, part="b", day=DAY, year=YEAR)
