from aocd import get_data
from collections import Counter
import networkx as nx

DELTA = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_data(data):
    lines = data.splitlines()

    nodes = {
        (x, y) for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c != "#"
    }
    start = next(node for node in nodes if lines[node[1]][node[0]] == "S")
    end = next(node for node in nodes if lines[node[1]][node[0]] == "E")

    return nodes, start, end


def build_graph(data):
    nodes, start, end = parse_data(data)
    G = nx.Graph()

    for node in nodes:
        x, y = node
        for dx, dy in DELTA:
            new_node = (x + dx, y + dy)
            if new_node in nodes:
                G.add_edge(node, new_node)

    return G, start, end


def get_width_height(data):
    lines = data.splitlines()
    return len(lines[0]), len(lines)


def get_possible_cheats(data):
    m = [list(line) for line in data.splitlines()]

    cheats = set()

    # Single wall
    for y, line in enumerate(m[1:-1], 1):
        for x, c in enumerate(line[1:-1], 1):
            # Horizontal
            if m[y][x - 1] != "#" and m[y][x] == "#" and m[y][x + 1] != "#":
                cheats.add(((x, y), (x + 1, y)))
                cheats.add(((x - 1, y), (x, y)))
            # Vertical
            if m[y - 1][x] != "#" and m[y][x] == "#" and m[y + 1][x] != "#":
                cheats.add(((x, y), (x, y + 1)))
                cheats.add(((x, y - 1), (x, y)))

    return cheats


def time_saved(nodes, distance_to_end, cheat):
    (x1, y1), (x2, y2) = cheat

    def get_best_time(srcs, dst):
        src_times = [distance_to_end[s] for s in srcs]
        dst_time = distance_to_end[dst]
        diffs = {src_time - dst_time - 2 for src_time in src_times}
        return max(diffs)

    if (x1, y1) in nodes:
        # Cheat goes l <- r
        dst = (x1, y1)
        srcs = {(x2 + dx, y2 + dy) for dx, dy in DELTA} & nodes
        return get_best_time(srcs, dst)
    if (x2, y2) in nodes:
        # Cheat goes l -> r
        dst = (x2, y2)
        srcs = {(x1 + dx, y1 + dy) for dx, dy in DELTA} & nodes
        return get_best_time(srcs, dst)


def part_one(data):
    G, start, end = build_graph(data)

    distance_to_end = dict(nx.single_source_shortest_path_length(G, end))

    nodes = set(G.nodes)

    cheats = get_possible_cheats(data)

    times = [time_saved(nodes, distance_to_end, cheat) for cheat in cheats]

    counts = Counter(times)

    """
    ts = sorted(
        ((c, t) for t, c in counts.items()),
        key=lambda x: x[1]
    )

    for count, time in ts:
        print(f"There are {count} cheats that save {time} time")
    """

    return sum(c for t, c in counts.items() if t >= 100)


def part_two(data):
    return 0


def main():
    data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    data = get_data(day=20, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
