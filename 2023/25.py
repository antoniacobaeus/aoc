import numpy as np
from collections import defaultdict


def parse_input(data):
    graph = defaultdict(set)
    for line in data.strip().split("\n"):
        src, neigh = line.split(": ")
        for n in neigh.split():
            graph[src].add(n)
            graph[n].add(src)
    return graph


def create_degree_matrix(graph, nodes):
    D = list(map(lambda n: len(graph[n]), nodes))
    return np.diag(D)


def create_adj_matrix(graph, nodes):
    A = np.zeros((len(nodes), len(nodes)))

    for src, neigh in graph.items():
        for n in neigh:
            A[nodes.index(src)][nodes.index(n)] = 1
    return A


def part1(data):
    graph = parse_input(data)
    nodes = list(graph.keys())

    D = create_degree_matrix(graph, nodes)
    A = create_adj_matrix(graph, nodes)

    L = D - A  # Laplacian matrix

    # The sparsest cut of a graph can be approximated through the Fiedler vector —
    # the eigenvector corresponding to the second smallest eigenvalue of the graph Laplacian
    eig = np.linalg.eig(L)
    eig_sort = np.argsort(eig.eigenvalues)
    eigenvectors = eig.eigenvectors.T[eig_sort]
    f = eigenvectors[1]  # fiedler

    return np.sum(f > 0) * np.sum(f < 0)


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
        """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
    )
    assert (
        str(p1) == ex.answer_a
    ), f"Part1 does not match example, {p1} != {ex.answer_a}"

    s = time.perf_counter()
    p1 = part1(data)
    print(f"Part1: {p1}, in {time.perf_counter() - s}")
    # submit(p1, part="a", day=DAY, year=YEAR)
