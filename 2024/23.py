import time
from collections import defaultdict 

def get_input():
    with open("input/2024/23.txt", "r") as f:
        return f.read()

def parse_input():
    data = get_input();
    pairs = []
    adj = defaultdict(list)
    for line in data.strip().splitlines():
        a, b = line.strip().split("-")
        pairs.append((a, b))
        adj[a].append(b)
        adj[b].append(a)
    return pairs, adj

def bron_kerbosch(R, P, X, adj):
    # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(
            R | {v},
            P & set(adj[v]),
            X & set(adj[v]),
            adj
        )
        P -= {v}
        X |= {v}


def part1(): 
    pairs, adj = parse_input()
    triples = set()
    for a, b in pairs:
        for c in adj[a]:
            if c in adj[b]:
                triples.add(tuple(sorted((a, b, c))))

    r = 0
    for triple in triples:
        if any(t.startswith("t") for t in triple):
            r += 1
    return r

def part2():
    pairs, adj = parse_input()

    all_cliques = list(bron_kerbosch(set(), set(adj.keys()), set(), adj))

    return ",".join(sorted(max(all_cliques, key=len)))

if __name__ == "__main__":
    t1 = time.perf_counter()
    p1 = part1()    
    print(f"p1: {p1} after {time.perf_counter() - t1} s")

    t1 = time.perf_counter()
    p2 = part2()
    print(f"p2: {p2} after {time.perf_counter() - t1} s")
