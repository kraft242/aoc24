from aocd import get_data
from time import perf_counter_ns
from collections import Counter
from itertools import product


def transpose(m):
    return list(map(list, zip(*m)))


def parse_entry(e):
    return tuple(Counter(line)["#"] - 1 for line in transpose(e))


def parse_data(data):
    entries = data.split("\n\n")
    return {
        "keys": [parse_entry(e.splitlines()) for e in entries if e[0] != "#"],
        "locks": [parse_entry(e.splitlines()) for e in entries if e[0] == "#"],
    }


def overlap(key, lock):
    return any(k + l > 5 for k, l in zip(key, lock))


def part_one(data):
    parsed = parse_data(data)
    return sum(
        not overlap(k, l)
        for k, l in product(parsed["keys"], parsed["locks"])
    )


def part_two(data):
    return 0


def main():
    data = get_data(day=25, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
