def parse_input(data):
    game = {}
    for line in data.strip().split("\n"):
        g, numbers = map(str.strip, line.split(":"))
        g = int(g.split()[1])

        winning, numbers = numbers.split("|")
        winning = list(map(int, winning.strip().split()))
        numbers = list(map(int, numbers.strip().split()))

        game[g] = (winning, numbers)

    return game


def part1(data):
    games = parse_input(data)

    s = 0
    for game, (winning, numbers) in games.items():
        g = 0
        for number in numbers:
            if number in winning:
                if g == 0:
                    g = 1
                else:
                    g *= 2
        s += g
    return s


def part2(data):
    games = parse_input(data)

    cards = [1 for _ in range(len(games))]
    for game, (winning, numbers) in games.items():
        wins = len([n for n in numbers if n in winning])

        for i in range(wins):
            cards[game + i] += cards[game - 1]
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
