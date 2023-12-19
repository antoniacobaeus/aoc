import re
from collections import defaultdict
from functools import reduce


def parse_input(data):
    workflow_string, ratings_string = data.strip().split("\n\n")

    workflows = defaultdict(list)
    for workflow in workflow_string.split("\n"):
        name, rules = workflow.split("{")
        rules = rules[:-1].split(",")

        for rule in rules[:-1]:
            cond, dest = rule.split(":")
            var, ltgt, val = re.split(r"(\<|\>)", cond.strip())

            workflows[name].append((var, ltgt, int(val), dest))
        workflows[name].append((None, None, None, rules[-1]))

    ratings = []
    for rating in ratings_string.split("\n"):
        rating = rating.strip()[1:-1].split(",")
        sub_rating = defaultdict(int)
        for r in rating:
            name, rating = r.split("=")
            sub_rating[name] = int(rating)
        ratings.append(sub_rating)

    return workflows, ratings


def sort_parts(workflows, rating):
    pos = "in"
    while not pos in "AR":
        workflow = workflows[pos]
        for rule in workflow:
            var, ltgt, val, dest = rule

            if (
                var is None
                or (ltgt == "<" and rating[var] < val)
                or (ltgt == ">" and rating[var] > val)
            ):
                pos = dest
                break
    return pos


def part1(data):
    workflows, ratings = parse_input(data)
    s = 0
    for rating in ratings:
        pos = sort_parts(workflows, rating)
        if pos == "A":
            s += sum(rating.values())
    return s


def calc_combinations(pos, workflows, rating):
    if pos == "A":
        return reduce(lambda a, b: a * b, (r.stop - r.start for r in rating.values()))

    if pos == "R":
        return 0

    s = 0
    workflow = workflows[pos]
    for rule in workflow:
        var, ltgt, val, dest = rule
        if var is None:
            s += calc_combinations(dest, workflows, rating)

        if ltgt == "<":
            if rating[var].start < val:
                s += calc_combinations(
                    dest, workflows, {**rating, var: range(rating[var].start, val)}
                )
            rating[var] = range(val, rating[var].stop)
        elif ltgt == ">":
            if rating[var].stop > val:
                s += calc_combinations(
                    dest, workflows, {**rating, var: range(val + 1, rating[var].stop)}
                )
            rating[var] = range(rating[var].start, val + 1)
    return s


def part2(data):
    workflows, _ = parse_input(data)

    rating = {var: range(1, 4000 + 1) for var in "xmas"}

    return calc_combinations("in", workflows, rating)


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
        p2 == 167409079868000
    ), f"Part2 does not match example, {p2} != {167409079868000}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
