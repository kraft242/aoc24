from aocd import get_data
from itertools import pairwise


def parse_line(line):
    return [int(n) for n in line.split()]


def parse_data(data):
    return [parse_line(l) for l in data.splitlines()]


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def is_safe(report):
    diffs = [l - r for l, r in pairwise(report)]
    signs = [sign(d) for d in diffs]

    monotone = all(s == signs[0] for s in signs)
    in_range = all(1 <= abs(d) <= 3 for d in diffs)

    return monotone and in_range


def part_one(data):
    reports = parse_data(data)
    return sum(is_safe(r) for r in reports)


def exclude(values, i):
    return values[:i] + values[i + 1:]


def is_safe_with_dampening(report):
    if is_safe(report):
        return True
    candidates = (exclude(report, i) for i in range(len(report)))
    return any(is_safe(c) for c in candidates)


def part_two(data):
    reports = parse_data(data)
    return sum(is_safe_with_dampening(r) for r in reports)


def main():
    data = get_data(day=2, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
