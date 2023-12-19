import re
from functools import reduce


def parse_input(data):
    return [step for step in data.strip().split(",")]


def part1(data):
    a = parse_input(data)

    return sum(reduce(lambda acc, c: (acc + ord(c)) * 17 % 256, step, 0) for step in a)


def part2(data):
    a = parse_input(data)

    boxes = [dict() for _ in range(256)]
    s = 0
    for step in a:
        m = re.split(r"(\=|\-)", step)
        label = m[0]

        h = 0
        for c in label:
            h += ord(c)
            h *= 17
            h %= 256

        if m[1].startswith("="):
            boxes[h][label] = int(m[2])
        else:
            if label in boxes[h]:
                del boxes[h][label]

    for i, box in enumerate(boxes):
        for j, slot in enumerate(box):
            s += (i + 1) * (j + 1) * box[slot]
    return s


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
    assert p2 == 145, f"Part2 does not match example, {p2} != {145}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
