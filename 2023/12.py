def parse_input(data):
    a = []
    for line in data.strip().split("\n"):
        values, groups = line.split(" ")
        groups = list(map(int, groups.split(",")))
        a.append((values, groups))
    return a


def solve(values, groups):
    values += "."
    n = len(values)
    m = len(groups)
    p = max(groups)

    dp = [[[0 for _ in range(p + 2)] for _ in range(m + 2)] for _ in range(n + 1)]
    dp[0][0][0] = 1

    for i, v in enumerate(values):
        for j in range(m + 1):
            for k in range(p + 1):
                c = dp[i][j][k]

                if not c:
                    continue

                if v in "?#":
                    if k == 0:
                        dp[i + 1][j + 1][k + 1] += c  # start new group
                    else:
                        dp[i + 1][j][k + 1] += c  # continue group
                if v in "?.":
                    g = groups[j - 1]
                    if k == 0 or k == g:
                        dp[i + 1][j][0] += c  # end group
    return dp[n][m][0]


def part1(data):
    groups = parse_input(data)
    s = 0
    for values, group in groups:
        v = solve(values, tuple(group))
        # print(values, group, v)
        s += v
    return s


def part2(data):
    groups = []
    for values, group in parse_input(data):
        groups.append(("?".join([values] * 5), group * 5))

    s = 0
    for values, group in groups:
        s += solve(values, tuple(group))
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
    p1 = part1(
        """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    )
    assert (
        str(p1) == ex.answer_a
    ), f"Part1 does not match example, {p1} != {ex.answer_a}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(
        """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    )
    assert p2 == 525152, f"Part2 does not match example, {p2} != {525152}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
