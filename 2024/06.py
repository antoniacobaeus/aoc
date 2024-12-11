from enum import Enum
import time

class Dir(Enum):
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

    def from_char(c):
        match c:
            case ">":
                return Dir.east
            case "v":
                return Dir.south
            case "<":
                return Dir.west
            case "^":
                return Dir.north

    def turn(self, clockwise=True):
        match self:
            case Dir.north:
                dir = Dir.east
            case Dir.east:
                dir = Dir.south
            case Dir.south:
                dir = Dir.west
            case Dir.west:
                dir = Dir.north
        return dir if clockwise else dir.opposite()

def get_input():
    with open("input/2024/06.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();

    m = []
    start = None
    dir = None
    for y, line in enumerate(data.strip().split("\n")):
        m.append([])
        for x, v in enumerate(line.strip()):
            if v in ["<", ">", "v", "^"]:
                start = x, y
                dir = Dir.from_char(v)
            m[y].append(1 if v == "#" else 0)
    return m, start, dir

def on_grid(grid, x, y):
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)

def check_cycle(m, start, dir, obstacle = None):
    seen = set()
    x, y = start
    while (True):
        if ((x, y, dir) in seen):
            return seen, True
        seen.add((x, y, dir))
        dx, dy = dir.value 

        if not on_grid(m, x + dx, y + dy):
            return seen, False
        if m[y + dy][x + dx] or (x + dx, y + dy) == obstacle:
            dir = dir.turn()
        else:
            x += dx
            y += dy

def part1(data): 
    m, start, dir = parse_input()

    seen, _ = check_cycle(m, start, dir)
    return len(set((x, y) for x, y, _ in seen))

def part2(data):
    m, start, start_dir = parse_input()

    seen, _ = check_cycle(m, start, start_dir)
    positions = list(set((x, y) for x, y, _ in seen))

    r = 0
    for p in positions: 
        if (check_cycle(m, start, start_dir, p)[1]):
            r += 1
    return r

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
