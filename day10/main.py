from aocd import get_data
import numpy as np
import networkx as nx


def parse_data(data):
    return np.array([list(map(int, line)) for line in data.split("\n") if line])


def build_graph(data):
    heights = parse_data(data)

    G = nx.Graph()

    WIDTH, HEIGHT = heights.shape

    for x in range(WIDTH):
        for y in range(HEIGHT):
            G.add_node((y, x), height=heights[y, x])

    delta = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    for x in range(WIDTH):
        for y in range(HEIGHT):
            for dx, dy in delta:
                if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                    G.add_edge((y, x), (y + dy, x + dx))
    return G


def trailhead_score(G, start, unique=True):
    stack = [start]
    score = 0
    reached = set()
    while stack:
        curr = stack.pop()
        height = G.nodes[curr]["height"]
        if height == 9 and curr not in reached:
            score += 1
            if unique:
                reached.add(curr)
            continue
        for neighbor in G.neighbors(curr):
            if G.nodes[neighbor]["height"] == height + 1:
                stack.append(neighbor)
    return score


def solve(data, unique=True):
    G = build_graph(data)

    zero_height = [n for n, d in G.nodes(data=True) if d["height"] == 0]

    return sum(
        trailhead_score(G, n, unique) for n in zero_height
    )


def part_one(data):
    return solve(data)


def part_two(data):
    return solve(data, unique=False)


def main():
    data = get_data(day=10, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
