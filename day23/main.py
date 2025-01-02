from aocd import get_data
from time import perf_counter_ns
import networkx as nx


def parse_data(data):
    G = nx.Graph()

    edges = [line.split("-") for line in data.splitlines()]

    G.add_edges_from(edges)

    return G


def part_one(data):
    G = parse_data(data)

    triplets = (set(c) for c in nx.enumerate_all_cliques(G) if len(c) == 3)

    starts_with_t = set(n for n in G.nodes if n.startswith("t"))

    return sum(len(t & starts_with_t) > 0 for t in triplets)


def part_two(data):
    G = parse_data(data)

    cliques = nx.find_cliques(G)

    max_clique = max(cliques, key=len)

    return ",".join(sorted(max_clique))


def main():
    data = get_data(day=23, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
