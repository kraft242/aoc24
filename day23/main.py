from aocd import get_data
from time import perf_counter_ns
import networkx as nx


def parse_data(data):
    edges = (line.split("-") for line in data.splitlines())

    return nx.Graph(edges)


def part_one(data):
    G = parse_data(data)

    starts_with_t = {n for n in G.nodes if n.startswith("t")}

    return sum(
        1 for c in nx.enumerate_all_cliques(G)
        if len(c) == 3
        and set(c) & starts_with_t
    )


def part_two(data):
    G = parse_data(data)

    return ",".join(
        sorted(
            max(nx.find_cliques(G), key=len)
        )
    )


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
