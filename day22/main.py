from aocd import get_data
from time import perf_counter_ns
from itertools import pairwise
from collections import defaultdict
import multiprocessing as mp


def parse_data(data):
    return list(map(int, data.splitlines()))


def mix(lhs, rhs):
    return lhs ^ rhs


def prune(secret):
    factor = 16777216
    return secret % factor


def next_secret(secret):
    a = prune(mix(secret << 6, secret))
    b = prune(mix(a >> 5, a))
    return prune(mix(b << 11, b))


def get_secrets(s, n):
    secrets = [s]
    for _ in range(n):
        s = next_secret(s)
        secrets.append(s)
    return secrets


def part_one(data):
    n = 2000
    args = [(secret, n) for secret in data]
    with mp.Pool(processes=mp.cpu_count()) as pool:
        secrets = pool.starmap(get_secrets, args)
    return sum(s[n - 1] for s in secrets)


def get_prices(secrets):
    return [s % 10 for s in secrets]


def get_differences(secrets):
    return [a - b for a, b in pairwise(secrets)]


def get_diff_prices(prices, diffs):
    n = 4
    res = []
    seen = set()
    for i in range(n - 1, len(diffs)):
        d = tuple(diffs[i - n + 1:i + 1])
        p = prices[i]
        if d in seen:
            continue
        seen.add(d)
        res.append((d, p))
    return res


def part_two(data):
    n = 2000
    args = [(secret, n) for secret in data]
    with mp.Pool(processes=mp.cpu_count()) as pool:
        secrets = pool.starmap(get_secrets, args)
        prices = pool.map(get_prices, secrets)
        diffs = pool.map(get_differences, prices)
        prices = [p[1:] for p in prices]
        diff_prices = pool.starmap(get_diff_prices, zip(prices, diffs))
    res = defaultdict(list)
    for dps in diff_prices:
        for d, p in dps:
            res[d].append(p)
    return max(
        sum(ps) for ps in res.values()
    )


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
