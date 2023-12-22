from collections import defaultdict


def parse_input(data):
    bricks = []
    for line in data.strip().split("\n"):
        start, end = line.strip().split("~")
        start = tuple(map(int, start.strip().split(",")))
        end = tuple(map(int, end.strip().split(",")))

        assert start[0] <= end[0]
        assert start[1] <= end[1]
        assert start[2] <= end[2]

        bricks.append((start, end))
    return bricks


def print_grid(grid, perspective):
    if perspective == "x":
        # print the grid with x as the width and z as the height
        for z in reversed(range(len(grid[0][0]))):
            for y in range(len(grid[0])):
                for x in range(len(grid)):
                    print(grid[x][y][z], end="")
                print(" ", end="")
            print()
    elif perspective == "y":
        # print the grid with y as the width and z as the height
        for z in reversed(range(len(grid[0][0]))):
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    print(grid[x][y][z], end="")
                print(" ", end="")
            print()


def build_dependency_graph(grid):
    depend = defaultdict(set)  # A: {B, C, D} means {B, C, D} depend on A

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for z in range(len(grid[0][0])):
                if grid[x][y][z] == ".":
                    continue

                # look at row above
                if (
                    z > 0
                    and grid[x][y][z - 1] != "."
                    and grid[x][y][z - 1] != grid[x][y][z]
                ):
                    depend[grid[x][y][z - 1]].add(grid[x][y][z])
    return depend


def print_dependency_graph(depend):
    for k, v in depend.items():
        print(f"{to_letter(k)}: {{{', '.join(to_letter(i) for i in v)}}}")


def place_brick(grid, brick, curr_z, i):
    start, end = brick

    coords = [
        (x, y, z)
        for x in range(start[0], end[0] + 1)
        for y in range(start[1], end[1] + 1)
        for z in range(curr_z, curr_z + (end[2] - start[2]) + 1)
    ]

    for x, y, z in coords:
        grid[x][y][z] = i
    return grid


def to_letter(i):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if i < len(alphabet):
        return alphabet[i]
    return alphabet[i % len(alphabet)] + f"{i // len(alphabet) + 1}"


def create_grid(bricks):
    max_x = max(b[1][0] for b in bricks)
    max_y = max(b[1][1] for b in bricks)
    max_z = max(b[1][2] for b in bricks)
    min_x = min(b[0][0] for b in bricks)
    min_y = min(b[0][1] for b in bricks)

    grid = [
        [["." for _ in range(0, max_z + 1)] for _ in range(min_y, max_y + 1)]
        for _ in range(min_x, max_x + 1)
    ]

    for i, brick in enumerate(sorted(bricks, key=lambda b: b[0][2])):
        start, end = brick

        curr_z = start[2]

        while curr_z > 0:
            coords = [
                (x, y, z)
                for x in range(start[0], end[0] + 1)
                for y in range(start[1], end[1] + 1)
                for z in range(curr_z, curr_z + (end[2] - start[2]) + 1)
            ]

            if any(grid[x][y][z] != "." for x, y, z in coords):
                place_brick(grid, brick, curr_z + 1, i)
                break
            curr_z -= 1
        else:
            place_brick(grid, brick, 1, i)

    return grid


def part1(data):
    bricks = parse_input(data)

    grid = create_grid(bricks)

    depend = build_dependency_graph(grid)
    # print_dependency_graph(depend)

    s = 0
    for i, brick in enumerate(bricks):
        if i not in depend:
            # print(f"{to_letter(i)} has no dependencies")
            s += 1
            continue

        other_sets = set()
        for k, v in depend.items():
            if k != i:
                other_sets |= v

        if all(a in other_sets for a in depend[i]):
            # print(f"{to_letter(i)} has covered dependencies")
            s += 1
    return s


def disintegrate(letter, depend):
    destroyed = set()
    stack = [letter]
    while stack:
        deps = depend[stack.pop()]
        other_sets = set()
        for k, v in depend.items():
            if not k in destroyed and k != letter:
                other_sets |= v

        for d in deps:
            if d not in other_sets:
                destroyed.add(d)
                stack.append(d)
    return destroyed


def part2(data):
    bricks = parse_input(data)

    grid = create_grid(bricks)

    depend = build_dependency_graph(grid)

    s = 0
    for i, brick in enumerate(bricks):
        disintegrated = disintegrate(i, depend)
        # print(
        #     f"{to_letter(i)} disintegrated => {', '.join(to_letter(i) for i in disintegrated)}"
        # )
        s += len(disintegrated)
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
    p1 = part1(ex.input_data)
    assert (
        str(p1) == ex.answer_a
    ), f"Part1 does not match example, {p1} != {ex.answer_a}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # # Part 2
    p2 = part2(ex.input_data)
    assert p2 == 7, f"Part2 does not match example, {p2} != {7}"

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
