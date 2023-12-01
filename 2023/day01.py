import regex as re


def parse_input(data):
    return [line.strip() for line in data.strip().split("\n")]


def part1(data):
    a = parse_input(data)

    s = 0
    for l in a:
        x = list(filter(lambda y: y.isnumeric(), l))
        s += int(x[0] + x[-1])
    return s


def part2(data):
    a = parse_input(data)

    translate = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    s = 0
    for l in a:
        c = re.findall(
            r"one|two|three|four|five|six|seven|eight|nine|\d", l, overlapped=True
        )

        x = list(map(lambda y: y if y.isnumeric() else translate[y], c))
        s += int(x[0] + x[-1])
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
    p2 = part2(
        """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    )
    assert (
        str(p2) == ex.answer_b
    ), f"Part2 does not match example, {p2} != {ex.answer_b}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    submit(p2, part="b", day=DAY, year=YEAR)
