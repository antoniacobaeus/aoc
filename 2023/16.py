from enum import Enum


def parse_input(data):
    grid = []
    for line in data.strip().split("\n"):
        grid.append(list(line.strip()))
    return grid


class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)


def get_new_dir(grid, x, y, dir: Dir):
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[y]):
        return []

    c = grid[y][x]

    match (dir, c):
        case (Dir.east, "\\") | (Dir.west, "/"):
            return [Dir.south]
        case (Dir.east, "/") | (Dir.west, "\\"):
            return [Dir.north]
        case (Dir.north, "\\") | (Dir.south, "/"):
            return [Dir.west]
        case (Dir.north, "/") | (Dir.south, "\\"):
            return [Dir.east]
        case (Dir.east, "|") | (Dir.west, "|"):
            return [Dir.north, Dir.south]
        case (Dir.north, "-") | (Dir.south, "-"):
            return [Dir.east, Dir.west]
        case (_, ".") | (_, "|") | (_, "-"):
            return [dir]
        case _:
            assert False, f"Unknown char {c}"


def traverse(grid, start=(0, 0, Dir.east)):
    path = set()

    stack = [start]

    while stack:
        x, y, dir = stack.pop()

        if (x, y, dir) in path or x < 0 or y < 0 or y >= len(grid) or x >= len(grid[y]):
            continue

        path.add((x, y, dir))

        new_dirs = get_new_dir(grid, x, y, dir)
        for new_dir in new_dirs:
            dx, dy = new_dir.value
            stack.append((x + dx, y + dy, new_dir))
    return path


def calc_score(visited):
    return len({(x, y) for (x, y, _) in visited})


def print_grid(grid, visited):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y) in {(x, y) for (x, y, _) in visited}:
                print("X", end="")
            else:
                print(c, end="")
        print()


def print_path(grid, visited):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y, Dir.north) in visited:
                print("^", end="")
            elif (x, y, Dir.south) in visited:
                print("v", end="")
            elif (x, y, Dir.east) in visited:
                print(">", end="")
            elif (x, y, Dir.west) in visited:
                print("<", end="")
            else:
                print(c, end="")
        print()


def part1(data):
    grid = parse_input(data)
    visited = traverse(grid)
    return calc_score(visited)


def part2(data):
    grid = parse_input(data)

    directions = [
        (Dir.north, None, len(grid) - 1),
        (Dir.west, len(grid[0]), None),
        (Dir.south, None, 0),
        (Dir.east, 0, None),
    ]
    m = 0

    for dir, sx, sy in directions:
        for p in range(len(grid[0]) if sx is None else len(grid)):
            start = (sx, p, dir) if sx is not None else (p, sy, dir)
            m = max(m, calc_score(traverse(grid, start)))
    return m


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
    assert p2 == 51, f"Part2 does not match example, {p2} != {51}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
