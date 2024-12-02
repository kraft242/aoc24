from aocd import get_data
from itertools import pairwise


def parse_line(line):
    return list(
        map(int, line.split())
    )


def parse_data(data):
    return list(
        map(parse_line, data.splitlines())
    )


def is_safe(report):
    diffs = [l - r for l, r in pairwise(report)]

    lo, hi = 1, 3
    return any(
        (
            all(lo <= d <= hi for d in diffs),
            all(-lo >= d >= -hi for d in diffs)
        )
    )


def part_one(data):
    reports = parse_data(data)
    return sum(
        map(is_safe, reports)
    )


def exclude(values, i):
    return values[:i] + values[i + 1:]


def is_safe_with_dampening(report):
    candidates = (
        exclude(report, i) for i in range(len(report))
    )
    return any(
        map(is_safe, candidates)
    )


def part_two(data):
    reports = parse_data(data)
    return sum(
        map(is_safe_with_dampening, reports)
    )


def main():
    data = get_data(day=2, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
