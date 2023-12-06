from functools import reduce


def parse_input(data):
    time, distance = data.strip().split("\n")

    time = map(int, time.strip().split(":")[1].split())
    distance = map(int, distance.strip().split(":")[1].split())

    return time, distance


def solve(t, distance):
    for i in range(t):
        d = (t - i) * i
        if d > distance:
            return t - (i * 2) + 1


def part1(data):
    times, distances = parse_input(data)

    s = 1
    for t, d in zip(times, distances):
        s *= solve(t, d)
    return s


def part2(data):
    times, distances = parse_input(data)

    t = int(reduce(lambda a, b: str(a) + str(b), times))
    d = int(reduce(lambda a, b: str(a) + str(b), distances))

    return solve(t, d)


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
    assert p1 == 288, f"Part1 does not match example, {p1} != {288}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(ex.input_data)
    assert p2 == 71503, f"Part2 does not match example, {p2} != {71503}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
