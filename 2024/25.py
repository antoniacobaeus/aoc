import time

def get_input():
    with open("input/2024/25.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    locks, keys = [], []
    for schematic in data.strip().split("\n\n"):
        lines = schematic.split("\n") 
        is_lock = lines[0] == "#"*len(lines[0])

        heights = [0 for _ in lines[0]]
        for l in lines[1:-1]:
            for i, c in enumerate(l):
                if c == "#":
                    heights[i] += 1
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)
    return locks, keys


def part1(): 
    locks, keys = parse_input()

    res = 0
    for lock in locks:
        for key in keys:
            for x, y in zip(lock, key):
                if y + x > len(lock): # len(lock) == len(key)
                    break
            else:
                res += 1
    return res

if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")
