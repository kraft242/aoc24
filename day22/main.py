# from aocd import get_data
from time import perf_counter_ns


def get_data(filename):
    with open(filename) as f:
        return [int(l) for l in f.readlines()]


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


def part_one(data):
    res = []
    for secret in data:
        for _ in range(2000):
            secret = next_secret(secret)
        res.append(secret)
        print(secret)
    print(res)
    return sum(res)


def part_two(data):
    return 0


def main():
    # data = get_data(day=19, year=2024)
    data = get_data("input.in")
    # data = [1, 10, 100, 2024]
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
