from math import lcm


def parse_input(data):
    modules = {}
    state = {}
    for line in data.strip().split("\n"):
        name, dest = line.split(" -> ")
        dest = dest.split(", ") if "," in dest else [dest]
        if name[0] == "%":
            # flip flop
            modules[name[1:]] = ("%", dest)
            state[name[1:]] = False
        elif name[0] == "&":
            # conjunction
            modules[name[1:]] = ("&", dest)
            state[name[1:]] = {}
        else:
            modules[name] = (None, dest)

    for name, (_, dest) in modules.items():
        for d in dest:
            if d in state and isinstance(state[d], dict):
                state[d][name] = False
    return modules, state


def press_button(modules, state, parent_highs=None, parent=None, i=None):
    queue = [("button", "broadcaster", False)]

    highs, lows = 0, 0

    while queue:
        fr, name, pulse = queue.pop(0)
        # print(f"{fr} {"-high" if pulse else "-low"} -> {name}")

        if pulse:
            highs += 1
        else:
            lows += 1

        if not name in modules:
            continue

        _type, dest = modules[name]

        if _type is None:
            for d in dest:
                queue.append((name, d, pulse))
        elif _type == "%":
            if not pulse:
                state[name] = not state[name]
                for d in dest:
                    queue.append((name, d, state[name]))
        elif _type == "&":
            state[name][fr] = pulse
            if parent is not None and name == parent and pulse:
                parent_highs[fr] = i

            b = all(state[name].values())
            for d in dest:
                queue.append((name, d, not b))

    return highs, lows, state, parent_highs


def part1(data):
    modules, state = parse_input(data)

    highs, lows = 0, 0
    for _ in range(1000):
        dh, dl, state, _ = press_button(modules, state)
        highs += dh
        lows += dl
    return highs * lows


def part2(data):
    modules, state = parse_input(data)

    parent = next(name for name, (_, dest) in modules.items() if "rx" in dest)
    parent_highs = {name: None for name in state[parent]}

    i = 0
    while not all(parent_highs.values()):
        i += 1
        _, _, state, parent_highs = press_button(
            modules, state, parent_highs, parent, i
        )
    return lcm(*parent_highs.values())


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
        """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    )
    assert p1 == 32000000, f"Part1 does not match example, {p1} != {32000000}"

    p1 = part1(
        """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    )
    assert p1 == 11687500, f"Part1 does not match example, {p1} != {11687500}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)

    # Part 2

    s = time.perf_counter()
    p2 = part2(data)
    print(f"Part2: {p2}, in {time.perf_counter() - s}")
    # submit(p2, part="b", day=DAY, year=YEAR)
