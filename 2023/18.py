from math import ceil
from enum import Enum


class Dir(Enum):
    east = (1, 0)
    south = (0, 1)
    west = (-1, 0)
    north = (0, -1)

    def from_char(c):
        match c:
            case "R":
                return Dir.east
            case "D":
                return Dir.south
            case "L":
                return Dir.west
            case "U":
                return Dir.north


def parse_input(data):
    a = []
    for line in data.strip().split("\n"):
        dir, dist, hex = line.strip().split(" ")
        dist = int(dist)
        hex = hex[1:-1]
        a.append((dir, dist, hex))
    return a


def calc_area(instructions: list[tuple[Dir, int]]):
    curr = (0, 0)

    A = 1  # include the origin

    def sub_area(x1, y1, x2, y2):
        return x1 * y2 - x2 * y1 + abs(x2 - x1) + abs(y2 - y1)

    for dir, dist in instructions:
        x, y = curr
        dx, dy = dir.value
        curr = (x + (dx * dist), y + (dy * dist))
        A += sub_area(x, y, *curr)
    return ceil(A / 2)


def part1(data):
    a = parse_input(data)

    return calc_area([(Dir.from_char(dir), dist) for dir, dist, _ in a])


def part2(data):
    a = parse_input(data)

    dirs = ["R", "D", "L", "U"]

    return calc_area(
        [(Dir.from_char(dirs[int(hex[-1])]), int(hex[1:-1], 16)) for _, _, hex in a]
    )


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
    assert p2 == 952408144115, f"Part2 does not match example, {p2} != {952408144115}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
