def parse_input(data):
    a = []
    lines = data.strip().split("\n\n")
    seeds = list(map(int, lines[0].strip().split(":")[1].strip().split()))
    maps: dict[(str, str), list[(range, range)]] = {}

    for line in lines[1:]:
        line = line.strip().split("\n")
        types = line[0].strip().split("-to-")
        to = types[0].strip()
        fr = types[1].split(" ")[0].strip()

        maps[(to, fr)] = []

        for l in line[1:]:
            dest, source, hop = map(int, l.strip().split())
            maps[(to, fr)].append((dest - source, range(source, source + hop)))
        maps[(to, fr)] = tuple(maps[(to, fr)])
    return seeds, maps


def find_dest(maps, dest):
    for k in maps:
        if dest == k[1]:
            return k


def lookup(mappings, val):
    if isinstance(val, int):
        val = range(val, val + 1)

    queue = [val]
    ranges = []
    while queue:
        r = queue.pop(0)

        for diff, s in mappings:
            if r.stop <= s.start or r.start >= s.stop:
                # r is before s or after s
                continue
            elif r.start < s.start and r.stop > s.stop:
                # r covers s
                queue.append(range(r.start, s.start))
                queue.append(range(s.stop, r.stop))

                ranges.append(range(s.start + diff, s.stop + diff))
                break
            elif r.start < s.start:
                # r overflows left and is partially covered by s
                queue.append(range(r.start, s.start))

                ranges.append(range(s.start + diff, r.stop + diff))
                break
            elif r.stop > s.stop:
                # r overflows right and is partially covered by s
                queue.append(range(s.stop, r.stop))

                ranges.append(range(r.start + diff, s.stop + diff))
                break
            else:
                # s covers r
                ranges.append(range(r.start + diff, r.stop + diff))
                break
        else:
            ranges.append(r)
    return ranges


def solve(seeds, maps):
    def inner(seed, dest):
        source, dest = find_dest(maps, dest)

        if source == "seed":
            return lookup(maps[("seed", dest)], seed)
        ranges = []
        res = inner(seed, source)
        for r in res:
            ranges.extend(lookup(maps[(source, dest)], r))
        return ranges

    res = []
    for seed in seeds:
        res.extend(inner(seed, "location"))
    return min(r.start for r in res)


def part1(data):
    seeds, maps = parse_input(data)

    return solve(seeds, maps)


def part2(data):
    seeds, maps = parse_input(data)

    range_seeds = []
    for i in range(0, len(seeds), 2):
        range_seeds.append(range(seeds[i], seeds[i] + seeds[i + 1]))

    return solve(range_seeds, maps)


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
    # submit(p2, part="b", day=DAY, year=YEAR)
