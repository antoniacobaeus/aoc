import time
import re
import numpy as np

def get_input():
    with open("input/2024/13.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();

    config = []
    for group in data.strip().split("\n\n"):
        buttons = []
        for button in re.finditer(r"Button \w: X\+(\d+), Y\+(\d+)", group):
            buttons.append((int(button.group(1)), int(button.group(2))))
        prize = re.search(r"Prize: X=(\d+), Y=(\d+)", group)

        config.append((buttons, (int(prize.group(1)), int(prize.group(2)))))
    return config

def solve(buttons, prize, max_steps, offset=0):
    (Ax, Ay), (Bx, By) = buttons
    Px, Py = prize
    Px += offset
    Py += offset

    a = np.array([
        [Ax, Bx],
        [Ay, By]
    ])
    b = np.array([Px, Py])

    R = np.linalg.solve(a, b)

    eps = 10e-04
    if not np.all((np.mod(R, 1) <= eps) | (1 - np.mod(R, 1) <= eps)):
        return 0
    A, B = R
    A = round(A)
    B = round(B)

    if max_steps is not None and (A > max_steps or B > max_steps):
        return 0
    return A * 3 + B * 1

def part1(data): 
    m = parse_input()

    return sum(
        solve(b, p, 100) for b, p in m
    )
                
def part2(data):
    m = parse_input()

    offset = 10000000000000

    return sum(
        solve(b, p, None, offset) for b, p in m
    )

if __name__ == "__main__":
    data = get_input()

    t1 = time.perf_counter()
    p1 = part1(data)    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2(data)
    print(f"p2: {p2} after {time.perf_counter() - t1} s")


