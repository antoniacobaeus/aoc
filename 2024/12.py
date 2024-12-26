from enum import Enum
import time

def get_input():
    with open("input/2024/12.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    grid = []
    galaxy = []
    for y, line in enumerate(data.splitlines()):
        grid.append(list(line))
    return grid

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

    def opposite(self):
        match self:
            case Dir.north:
                return Dir.south
            case Dir.south:
                return Dir.north
            case Dir.east:
                return Dir.west
            case Dir.west:
                return Dir.east

def on_grid(grid, x, y):
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)

def flood(grid, sx, sy):
    seen = set()
    stack = [(sx, sy)]
    letter = grid[sy][sx]

    while (stack):
        x, y = stack.pop()
        l = grid[y][x]

        if l != letter:
            continue
        if (x, y) in seen:
            continue
        seen.add((x, y))

        for dir in Dir:
            dx, dy = dir.value
            if (on_grid(grid, x + dx, y + dy)):
                stack.append((x + dx, y + dy))
    return seen

def area(seen):
    return len(seen)

def perimeter(grid, seen, dirs):
    per = set()
    p = 0
    for (x, y) in list(seen):
        for dir in dirs:
            dx, dy = dir.value
            if ((x + dx, y + dy) not in seen):
                p += 1
                per.add((x + dx, y + dy))
    return p, per

def perimeter_split(grid, seen):
    for dir in Dir:
        yield perimeter(grid, seen, [dir])[1]

def print_grid(grid, seen, per):
    for y in range(-1, len(grid) + 1):
        for x in range(-1, len(grid[0]) + 1):
            if (x, y) in per:
                print("o", end="")
            elif (x, y) in seen:
                print("x", end="")
            else:
                print(".", end="")
        print()
    print()

def count_lines(grid, seen, per, used, dirs):
    lines = 0
    for (x, y) in per:
        if (x, y) in used:
            continue
        line = set()
        for dir in dirs:
            dx, dy = dir.value
            nx, ny = x + dx, y + dy
            while (nx, ny) in per:
                line.add((nx, ny))
                nx += dx
                ny += dy
        if line:
            lines += 1
            used |= line
            used.add((x, y))
    return lines

def count_singles(per):
    r = 0
    for (x, y) in per:
        for dir in Dir:
            dx, dy = dir.value
            if (x + dx, y + dy) in per:
                break
        else: # if not break (not found)
            r += 1
    return r 

def sides(grid, seen):
    r = 0
    for per in perimeter_split(grid, seen):
        used = set()
        r += count_lines(grid, seen, per, used, [Dir.south, Dir.north])
        r += count_lines(grid, seen, per, used, [Dir.east, Dir.west])
        r += count_singles(per)
    return r

def part1(data): 
    grid = parse_input()

    used = set()
    r = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in used:
                continue
            seen = flood(grid, x, y)
            used |= seen
            r += area(seen) * perimeter(grid, seen, list(Dir))[0]
    return r


def part2(data):
    grid = parse_input()

    used = set()
    r = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in used:
                continue
            seen = flood(grid, x, y)
            used |= seen
            r += area(seen) * sides(grid, seen)
    return r

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
