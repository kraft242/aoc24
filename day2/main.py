from aocd import get_data
from itertools import pairwise

LO, HI = 1, 3


def parse_line(line):
    return [int(n) for n in line.split()]


def parse_data(data):
    return [parse_line(l) for l in data.splitlines()]


def differences(values):
    return [l - r for l, r in pairwise(values)]


def is_safe(report):
    diffs = differences(report)

    strict_increase = all(LO <= d <= HI for d in diffs)
    strict_decrease = all(-LO >= d >= -HI for d in diffs)
    return strict_increase or strict_decrease


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
