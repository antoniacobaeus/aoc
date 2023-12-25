from enum import Enum
from collections import defaultdict


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

    def __lt__(self, other):
        return self.value < other.value


def get_move_dir(grid, curr, slip):
    x, y = curr

    if not slip:
        match grid[y][x]:
            case "#":
                return []
            case _:
                return [Dir.north, Dir.south, Dir.east, Dir.west]
    else:
        match grid[y][x]:
            case ">":
                return [Dir.east]
            case "<":
                return [Dir.west]
            case "^":
                return [Dir.north]
            case "v":
                return [Dir.south]
            case "#":
                return []
            case _:
                return [Dir.north, Dir.south, Dir.east, Dir.west]


def move(curr, dir: Dir):
    x, y = curr
    dx, dy = dir.value
    x += dx
    y += dy
    return (x, y)


def in_bounds(grid, curr):
    x, y = curr
    return x >= 0 and y >= 0 and y < len(grid) and x < len(grid[y])


def get_valid_moves(grid, curr, visited, slip):
    moves = []
    dirs = get_move_dir(grid, curr, slip)
    for dir in dirs:
        nx, ny = move(curr, dir)

        if (nx, ny) in visited:
            continue

        if not in_bounds(grid, (nx, ny)):
            continue

        if grid[ny][nx] == "#":
            continue

        if not dir in get_move_dir(grid, (nx, ny), slip):
            continue
        moves.append((nx, ny))
    return moves


def gen_graph(grid, start, end, slip):
    graph = defaultdict(set)
    piss = set()

    def add_to_graph(origin, begin, curr, steps):
        graph[origin].add((curr, steps))
        piss.add((origin, begin))

    Q = [(start, start, 0)]

    while Q:
        visited = set()

        origin, begin, steps = Q.pop()

        visited.add(origin)
        visited.add(begin)

        curr = begin
        moves = get_valid_moves(grid, curr, visited, slip)
        while len(moves) == 1:
            curr = moves[0]
            steps += 1
            visited.add(curr)

            if curr == end:
                break

            moves = get_valid_moves(grid, curr, visited, slip)

        if curr == end:
            add_to_graph(origin, begin, curr, steps)
            continue

        if len(moves) == 0:
            continue

        add_to_graph(origin, begin, curr, steps + 1)
        for m in moves:
            if (curr, m) in piss:
                continue
            Q.append((curr, m, 0))
    return graph


def dfs(graph, curr, end, visited=set()):
    if curr == end:
        return 0

    visited.add(curr)

    walk = 0
    for d, s in graph[curr]:
        if not d in visited:
            walk = max(walk, s + dfs(graph, d, end, visited))
    visited.remove(curr)
    return walk


def part1(data):
    grid = parse_input(data)

    start = next(
        (x, y)
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if grid[y][x] == "."
    )

    end = next(
        (x, y)
        for y in reversed(range(len(grid)))
        for x in reversed(range(len(grid[y])))
        if grid[y][x] == "."
    )

    graph = gen_graph(grid, start, end, True)
    return dfs(graph, start, end)


def part2(data):
    grid = parse_input(data)

    start = next(
        (x, y)
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if grid[y][x] == "."
    )

    end = next(
        (x, y)
        for y in reversed(range(len(grid)))
        for x in reversed(range(len(grid[y])))
        if grid[y][x] == "."
    )

    graph = gen_graph(grid, start, end, False)
    return dfs(graph, start, end)


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
    assert p1 == 94, f"Part1 does not match example, {p1} != {94}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2
    p2 = part2(ex.input_data)
    assert p2 == 154, f"Part2 does not match example, {p2} != {154}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
