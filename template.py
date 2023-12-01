def parse_input(data):
    return [line.strip() for line in data.strip().split("\n")]


def part1(data):
    a = parse_input(data)

    pass


def part2(data):
    a = parse_input(data)

    pass


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
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    # p2 = part2(ex.input_data)
    # assert str(p2) == ex.answer_b, f"Part2 does not match example, {p2} != {ex.answer_b}"

    # s = time.perf_counter()
    # p2 = part2(data)
    # print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
