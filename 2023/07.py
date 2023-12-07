from functools import cmp_to_key


def parse_input(data):
    a = []
    for line in data.strip().split("\n"):
        x, y = line.strip().split()
        a.append((x, int(y)))
    return a


def get_rank(hand, joker=False):
    if joker:
        no_jokers = hand.replace("J", "")
        if no_jokers:
            most_common = max(set(no_jokers), key=no_jokers.count)

            hand = hand.replace("J", most_common)

    l = len(set(hand))

    if l == 1:  # five of a kind
        return 6
    elif l == 2:
        if any(hand.count(x) == 4 for x in hand):  # four of a kind
            return 5
        else:  # full house
            return 4
    elif l == 3:
        if any(hand.count(x) == 3 for x in hand):  # three of a kind
            return 3
        else:  # two pair
            return 2
    elif l == 4:  # one pair
        return 1
    else:  # high card
        return 0


def compare(h1, h2, joker):
    labels = "AKQJT98765432"
    if joker:
        labels = "AKQT98765432J"

    r1 = get_rank(h1, joker)
    r2 = get_rank(h2, joker)

    if r1 > r2:
        return 1
    elif r1 < r2:
        return -1
    else:
        for x, y in zip(h1, h2):
            if labels.index(x) < labels.index(y):
                return 1
            elif labels.index(x) > labels.index(y):
                return -1


def part1(data):
    a = parse_input(data)

    def comp(h1, h2):
        return compare(h1[0], h2[0], joker=False)

    s = sorted(a, key=cmp_to_key(comp))

    return sum(bid * (i + 1) for i, (_hand, bid) in enumerate(s))


def part2(data):
    a = parse_input(data)

    def comp(h1, h2):
        return compare(h1[0], h2[0], joker=True)

    s = sorted(a, key=cmp_to_key(comp))

    return sum(bid * (i + 1) for i, (_hand, bid) in enumerate(s))


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
    assert (
        str(p2) == ex.answer_b
    ), f"Part2 does not match example, {p2} != {ex.answer_b}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
