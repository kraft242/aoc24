from aocd import get_data
from time import perf_counter_ns
from itertools import pairwise
import multiprocessing as mp


def parse_data(data):
    return list(map(int, data.splitlines()))


def mix(lhs, rhs):
    return lhs ^ rhs


def prune(secret):
    factor = 16777216
    return secret % factor


def next_secret(secret):
    one = prune(mix(secret << 6, secret))
    two = prune(mix(one >> 5, one))
    three = prune(mix(two << 11, two))
    return three


def get_nth_secret(secret, n):
    for _ in range(n):
        secret = next_secret(secret)
    return secret


def part_one(data):
    n = 2000
    args = [(secret, n) for secret in data]
    with mp.Pool(processes=mp.cpu_count()) as pool:
        res = pool.starmap(get_nth_secret, args)
    return sum(res)


def part_two(data):
    return 0


def main():
    data = get_data(day=22, year=2024)
    data = parse_data(data)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
