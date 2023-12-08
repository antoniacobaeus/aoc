from math import lcm


def parse_input(data):
    steps, rest = map(str.strip, data.split("\n\n"))
    a = {}
    for line in rest.splitlines():
        here, there = line.split(" = ")
        l, r = there.split(", ")
        a[here] = (l[1:], r[:-1])
    return steps, a


def solve(steps, mapping, start, end):
    curr = 0
    while start != end:
        step = steps[curr % len(steps)]
        if step == "R":
            start = mapping[start][1]
        elif step == "L":
            start = mapping[start][0]
        curr += 1

    return curr


def find_end(steps, mapping, start, ends):
    curr = 0
    while start not in ends:
        step = steps[curr % len(steps)]
        if step == "R":
            start = mapping[start][1]
        elif step == "L":
            start = mapping[start][0]
        curr += 1

    return curr


def part1(data):
    steps, a = parse_input(data)

    return solve(steps, a, "AAA", "ZZZ")


def part2(data):
    steps, a = parse_input(data)

    starts = list(filter(lambda x: x.endswith("A"), a))
    ends = list(filter(lambda x: x.endswith("Z"), a))

    e = [find_end(steps, a, s, ends) for s in starts]

    return lcm(*e)


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
    assert p1 == 2, f"Part1 does not match example, {p1} != {2}"

    p1 = part1(
        """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    )
    assert p1 == 6, f"Part1 does not match example, {p1} != {6}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(
        """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    )
    assert p2 == 6, f"Part2 does not match example, {p2} != {6}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
