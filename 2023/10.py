from math import ceil


def parse_input(data):
    grid = []
    for line in data.strip().split("\n"):
        grid.append(list(line.strip()))

    pipes = {}
    start = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            match grid[y][x]:
                case "|":
                    pipes[(x, y)] = ((x, y - 1), (x, y + 1))
                case "-":
                    pipes[(x, y)] = ((x + 1, y), (x - 1, y))
                case "L":
                    pipes[(x, y)] = ((x, y - 1), (x + 1, y))
                case "J":
                    pipes[(x, y)] = ((x, y - 1), (x - 1, y))
                case "7":
                    pipes[(x, y)] = ((x, y + 1), (x - 1, y))
                case "F":
                    pipes[(x, y)] = ((x + 1, y), (x, y + 1))
                case "S":
                    start = (x, y)
                case _:
                    continue
    pipes[start] = tuple(
        (start[0] + dir[0], start[1] + dir[1])
        for dir in [(0, -1), (1, 0), (0, 1), (-1, 0)]
        if (start[0] + dir[0], start[1] + dir[1]) in pipes
        and start in pipes[(start[0] + dir[0], start[1] + dir[1])]
    )

    return grid, pipes, start


def find_cycle(pipes, start):
    visited = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        visited.add(node)
        for dir in pipes[node]:
            if dir is None or dir in visited:
                continue
            stack.append(dir)
    return visited


def part1(data):
    _, pipes, start = parse_input(data)

    visited = find_cycle(pipes, start)
    depth = len(visited)
    return ceil(depth / 2)


def count_dir(fr, dir, loop, grid, pipes):
    x, y = fr
    s = 0
    last = None
    l, r = 0, 0
    while 0 < x < (len(grid[0]) - 1) and 0 < y < (len(grid) - 1):
        x += dir[0]
        y += dir[1]

        if (x, y) in loop:
            if last is None or not (x, y) in pipes[last]:
                # new line
                s += l % 2 == 1 and r % 2 == 1
                l, r = 0, 0

            if dir[0]:
                l += (x, y - 1) in pipes[(x, y)]
                r += (x, y + 1) in pipes[(x, y)]
            else:
                l += (x - 1, y) in pipes[(x, y)]
                r += (x + 1, y) in pipes[(x, y)]
            last = (x, y)
    s += l % 2 == 1 and r % 2 == 1
    return s


def find_enclosed(grid, pipes, loop):
    s = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in loop:
                continue
            if count_dir((x, y), (0, -1), loop, grid, pipes) % 2 == 1:
                s.add((x, y))
    return s


def part2(data):
    grid, pipes, start = parse_input(data)

    loop = find_cycle(pipes, start)
    enclosed = find_enclosed(grid, pipes, loop)
    return len(enclosed)


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
        """.....
.S-7.
.|.|.
.L-J.
....."""
    )
    assert p1 == 4, f"Part1 does not match example, {p1} != {4}"

    p1 = part1(
        """..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ..."""
    )
    assert p1 == 8, f"Part1 does not match example, {p1} != {8}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(
        """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    )
    assert p2 == 4, f"Part2 does not match example, {p2} != {4}"

    p2 = part2(
        """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
    )
    assert p2 == 8, f"Part2 does not match example, {p2} != {8}"

    p2 = part2(
        """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    )
    assert p2 == 10, f"Part2 does not match example, {p2} != {10}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
