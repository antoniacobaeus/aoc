from enum import Enum
from heapq import heappush, heappop


def parse_input(data):
    grid = []
    for line in data.strip().split("\n"):
        grid.append(list(map(int, line.strip())))
    return grid


class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

    def __lt__(self, other):
        return self.value < other.value


def get_turn_dir(dir: Dir):
    match dir:
        case Dir.north:
            return [Dir.west, Dir.east]
        case Dir.west:
            return [Dir.south, Dir.north]
        case Dir.south:
            return [Dir.east, Dir.west]
        case Dir.east:
            return [Dir.north, Dir.south]


def move(curr, dir: Dir, m=1):
    x, y = curr
    dx, dy = dir.value
    x += dx * m
    y += dy * m
    return (x, y)


def in_bounds(grid, curr):
    x, y = curr
    return x >= 0 and y >= 0 and y < len(grid) and x < len(grid[y])


def h(curr, end):
    # manhattan distance
    x, y = curr
    ex, ey = end
    return abs(ex - x) + abs(ey - y)


def A_star(grid, min_steps, max_steps):
    start = (0, 0)
    end = (len(grid[0]) - 1, len(grid) - 1)

    Q = []

    heappush(Q, (h(start, end), 0, start, 0, Dir.east))
    heappush(Q, (h(start, end), 0, start, 0, Dir.south))

    visited = set()

    while Q:
        _, d, u, step, curr_dir = heappop(Q)

        if u == end and min_steps - 1 <= step:
            return d

        if (u, step, curr_dir) in visited:
            continue
        visited.add((u, step, curr_dir))

        new_dirs = get_turn_dir(curr_dir) if min_steps - 1 <= step else []
        if step < max_steps - 1:
            new_dirs.append(curr_dir)
        for dir in new_dirs:
            nx, ny = move(u, dir)

            if (len(grid[0]) - 1) < nx or nx < 0 or (len(grid) - 1) < ny or ny < 0:
                continue

            alt = d + grid[ny][nx]
            heappush(
                Q,
                (
                    alt + h((nx, ny), end),
                    alt,
                    (nx, ny),
                    step + 1 if dir == curr_dir else 0,
                    dir,
                ),
            )


def part1(data):
    grid = parse_input(data)

    return A_star(grid, 0, 3)


def part2(data):
    grid = parse_input(data)

    return A_star(grid, 4, 10)


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
    assert p2 == 94, f"Part2 does not match example, {p2} != {94}"

    p2 = part2(
        """111111111111
999999999991
999999999991
999999999991
999999999991"""
    )
    assert p2 == 71, f"Part2 does not match example, {p2} != {71}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
