from functools import cache


def parse_input(data):
    a = []
    lines = data.strip().split("\n\n")
    seeds = list(map(int, lines[0].strip().split(":")[1].strip().split()))
    maps = {}

    for line in lines[1:]:
        line = line.strip().split("\n")
        types = line[0].strip().split("-to-")
        to = types[0].strip()
        fr = types[1].split(" ")[0].strip()

        maps[(to, fr)] = []

        for l in line[1:]:
            dest, source, hop = map(int, l.strip().split())
            maps[(to, fr)].append((dest, source, hop))
        maps[(to, fr)] = tuple(maps[(to, fr)])
    return seeds, maps


def find_dest(maps, dest):
    for k, v in maps.items():
        if dest in k:
            return k


@cache
def lookup(mappings, val):
    for d, s, h in mappings:
        src_r = range(s, s + h)
        if val in src_r:
            i = src_r.index(val)  # how many hops?
            return d + i
    return val


def solve(seeds, maps):
    print(f"searching for {len(seeds)} seeds...")

    @cache
    def inner(seed, dest):
        source, dest = find_dest(maps, dest)

        if source == "seed":
            return lookup(maps[("seed", dest)], seed)
        r = inner(seed, source)
        return lookup(maps[(source, dest)], r)

    locations = []
    for seed in seeds:
        print(f"searching for seed {seed}")
        locations.append(inner(seed, "location"))
    return min(locations)


def part1(data):
    seeds, maps = parse_input(data)

    return solve(seeds, maps)


def part2(data):
    seeds, maps = parse_input(data)

    pass


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
    assert p2 == 46, f"Part2 does not match example, {p2} != {46}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    submit(p2, part="b", day=DAY, year=YEAR)
