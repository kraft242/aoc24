from aocd import get_data
from time import perf_counter_ns
import networkx as nx


def part_one(data):
    nodes = set()

    for line in data.splitlines():
        l, r = line.split("-")
        nodes.add(l)
        nodes.add(r)

    node_to_id = {n: i for i, n in enumerate(nodes)}
    id_to_node = {i: n for n, i in node_to_id.items()}

    G = nx.Graph()

    for line in data.splitlines():
        l, r = line.split("-")
        lid, rid = node_to_id[l], node_to_id[r]
        G.add_edge(lid, rid)

    triplets = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]

    starts_with_t = set(
        i for node, i in node_to_id.items()
        if node.startswith("t")
    )

    found = set(
        (a, b, c) for a, b, c in triplets
        if a in starts_with_t or b in starts_with_t or c in starts_with_t
    )

    return len(found)


def part_two(data):
    nodes = set()
    for line in data.splitlines():
        l, r = line.split("-")
        nodes.add(l)
        nodes.add(r)
    node_to_id = {n: i for i, n in enumerate(nodes)}
    id_to_node = {i: n for n, i in node_to_id.items()}

    G = nx.Graph()

    for line in data.splitlines():
        l, r = line.split("-")
        lid, rid = node_to_id[l], node_to_id[r]
        G.add_edge(lid, rid)

    cliques = nx.find_cliques(G)
    max_clique = max(cliques, key=len)
    computers = [id_to_node[i] for i in max_clique]
    return ",".join(sorted(computers))


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
