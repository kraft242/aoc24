from aocd import get_data
from collections import Counter
from itertools import combinations
from scipy.spatial import KDTree
import networkx as nx
import multiprocessing as mp

DELTA = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_data(data):
    lines = data.splitlines()

    nodes = {
        (x, y) for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c != "#"
    }
    end = next(node for node in nodes if lines[node[1]][node[0]] == "E")

    return nodes, end


def build_graph(data):
    nodes, end = parse_data(data)
    G = nx.Graph()

    for node in nodes:
        x, y = node
        for dx, dy in DELTA:
            new_node = (x + dx, y + dy)
            if new_node in nodes:
                G.add_edge(node, new_node)

    return G, end


def get_width_height(data):
    lines = data.splitlines()
    return len(lines[0]), len(lines)


def manhattan_distance(l, r):
    lx, ly = l
    rx, ry = r
    return abs(lx - rx) + abs(ly - ry)


def time_saved(distance_to_end, cheat):
    src, dst = cheat

    return distance_to_end[src] - distance_to_end[dst] - manhattan_distance(src, dst)


def get_cheats(G, max_distance):
    nodes = sorted(G.nodes)
    tree = KDTree(nodes)
    cheats = set()
    min_distance = 2

    for node in nodes:
        indices = tree.query_ball_point(node, max_distance)
        for i in indices:
            m = nodes[i]
            if m != node and min_distance <= manhattan_distance(node, m) <= max_distance:
                cheats.add((node, m))

    return cheats


def get_time_counts(distances, cheats):
    times = (time_saved(distances, cheat) for cheat in cheats)

    return Counter(times)


def get_results(time_counts):
    return sum(c for t, c in time_counts.items() if t >= 100)


def part_one(data):
    G, end = build_graph(data)

    distances = dict(nx.single_source_shortest_path_length(G, end))

    cheats = get_cheats(G, 2)

    time_counts = get_time_counts(distances, cheats)

    return get_results(time_counts)


def part_two(data):
    G, end = build_graph(data)

    distances = dict(nx.single_source_shortest_path_length(G, end))

    cheats = get_cheats(G, 20)

    time_counts = get_time_counts(distances, cheats)

    return get_results(time_counts)


def main():
    data = get_data(day=20, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
