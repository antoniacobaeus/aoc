def parse_input(data):
    history = []
    for line in data.strip().split("\n"):
        history.append(list(map(int, line.strip().split())))
    return history


def differences(a):
    prev = a[0]
    for x in a[1:]:
        yield x - prev
        prev = x


def solve(history, right):
    s = 0

    for h in history:
        extrapolate = [h]
        d = h
        while any(d):
            d = list(differences(d))
            extrapolate.append(d)

        if right:
            extrapolate[-1].append(0)
            for i in range(len(extrapolate) - 2, 0, -1):
                extrapolate[i].append(extrapolate[i][-1] + extrapolate[i + 1][-1])
            s += extrapolate[0][-1] + extrapolate[1][-1]
        else:
            extrapolate[-1].insert(0, 0)
            for i in range(len(extrapolate) - 2, 0, -1):
                extrapolate[i].insert(0, extrapolate[i][0] - extrapolate[i + 1][0])
            s += extrapolate[0][0] - extrapolate[1][0]
    return s


def part1(data):
    history = parse_input(data)

    return solve(history, True)


def part2(data):
    history = parse_input(data)

    return solve(history, False)


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
    assert p2 == 2, f"Part2 does not match example, {p2} != {2}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
