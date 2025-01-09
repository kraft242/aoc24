from aocd import get_data
from time import perf_counter_ns
import networkx as nx
import numpy as np
from itertools import pairwise
from collections import defaultdict

DELTA = [
    (0, -1),  # North
    (1, 0),   # East
    (0, 1),   # South
    (-1, 0),  # West
]


def parse_data(data):
    grid = data.splitlines()
    nodes = {
        ((x, y), c)
        for y, row in enumerate(grid)
        for x, c in enumerate(row)
        if c != "#"
    }
    start = next((pos for pos, c in nodes if c == "S"))
    end = next((pos for pos, c in nodes if c == "E"))
    nodes = {(pos, d) for pos, _ in nodes for d in DELTA}
    return nodes, start, end


def build_graph(nodes, start):
    G = nx.DiGraph()

    G.add_nodes_from(nodes)

    Q = [(start, DELTA[1])]

    heading_to_index = {delta: i for i, delta in enumerate(DELTA)}

    visited = set()

    def add_edge(src, dst, c):
        if dst in nodes:
            G.add_edge(src, dst, cost=c)
            Q.append(dst)

    while Q:
        pos, heading = Q.pop()
        src = (pos, heading)
        if src in visited:
            continue
        visited.add(src)

        i = heading_to_index[heading]

        left = DELTA[(i - 1) % 4]
        right = DELTA[(i + 1) % 4]

        cdsts = [(pos, left), (pos, right)]

        for cdst in cdsts:
            add_edge(src, cdst, 1000)

        x, y = pos
        hx, hy = heading

        ldst = ((x + hx, y + hy), heading)

        rdst = ((x + hx, y + hy), heading)

        add_edge(src, ldst, 1)
        add_edge(src, rdst, 1)

    return G


def print_path(path, data):
    m = [list(row) for row in data.splitlines()]
    for (l, _), (r, _) in pairwise(path):
        lx, ly = l
        rx, ry = r
        m[ly][lx] = "X"
        m[ry][rx] = "X"

    for line in m:
        print("".join(line))


def get_shortest_paths(G, start, end):
    initial_heading = DELTA[1]

    start = ((start), initial_heading)

    ends = [((end), delta) for delta in DELTA]

    paths = []
    for end in ends:
        try:
            path = nx.all_shortest_paths(
                G, source=start, target=end, weight="cost"
            )
            paths.extend(path)
        except nx.NetworkXNoPath:
            pass

    return paths


def get_path_scores(G, paths):
    path_scores = defaultdict(list)

    for path in paths:
        score = sum(G[l][r]["cost"] for l, r in pairwise(path))
        path_scores[score].append(path)

    return path_scores


def part_one(data):
    nodes, start, end = parse_data(data)
    G = build_graph(nodes, start)
    paths = get_shortest_paths(G, start, end)
    score_paths = get_path_scores(G, paths)

    return min(score_paths.keys())


def part_two(data):
    nodes, start, end = parse_data(data)
    G = build_graph(nodes, start)
    paths = get_shortest_paths(G, start, end)
    score_paths = get_path_scores(G, paths)
    best_score = min(score_paths.keys())
    best_paths = score_paths[best_score]
    tiles = {e for path in best_paths for e, _ in path}

    return len(tiles)


def main():
    data = get_data(day=16, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
