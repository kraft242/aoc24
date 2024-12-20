from aocd import get_data
from time import perf_counter_ns
import multiprocessing as mp


def parse_data(data):
    patterns, towels = data.split("\n\n")

    towels = tuple(t.strip() for t in towels.split("\n"))

    patterns = tuple(p.strip() for p in patterns.split(","))
    pattern_lengths = tuple(len(p) for p in patterns)

    return towels, patterns, pattern_lengths


def ways_to_construct(towel, patterns, pattern_lengths):
    tl = len(towel) + 1

    ways = [0 for _ in range(tl)]
    ways[0] = 1

    for i in range(1, tl):
        ways[i] = sum(
            ways[i - pl]
            for pl, p in zip(pattern_lengths, patterns)
            if i >= pl and towel[i - pl: i] == p
        )

    return ways[-1]


def ways_to_solve(data):
    towels, patterns, pattern_lengths = parse_data(data)

    args = ((t, patterns, pattern_lengths) for t in towels)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        ways = pool.starmap(ways_to_construct, args)

    return ways


def part_one(data):
    ways = ways_to_solve(data)

    return sum(w > 0 for w in ways)


def part_two(data):
    ways = ways_to_solve(data)

    return sum(ways)


def main():
    data = get_data(day=19, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
