def parse_input(data):
    wins = []
    for line in data.strip().split("\n"):
        _, numbers = map(str.strip, line.split(":"))

        winning, numbers = numbers.split("|")
        winning = set(map(int, winning.strip().split()))
        numbers = set(map(int, numbers.strip().split()))

        wins.append(len(winning & numbers))

    return wins


def part1(data):
    wins = parse_input(data)

    return sum(2 ** (w - 1) if w > 0 else 0 for w in wins)


def part2(data):
    wins = parse_input(data)

    cards = [1 for _ in range(len(wins))]
    for c, w in enumerate(wins):
        for i in range(w):
            cards[c + i] += cards[c - 1]
    return sum(cards)


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
    submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(ex.input_data)
    assert p2 == 30, f"Part2 does not match example, {p2} != {30}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    submit(p2, part="b", day=DAY, year=YEAR)
