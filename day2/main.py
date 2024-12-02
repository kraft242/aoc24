from aocd import get_data
from itertools import pairwise


def parse_data(data):
    reports = []
    for line in data.splitlines():
        numbers = [int(n) for n in line.split()]
        reports.append(numbers)
    return reports


def is_safe(report):
    diffs = [l - r for l, r in pairwise(report)]

    lo, hi = 1, 3
    return any((
        all(lo <= d <= hi for d in diffs),
        all(-lo >= d >= -hi for d in diffs)
    ))


def part_one(data):
    reports = parse_data(data)
    return sum(is_safe(r) for r in reports)


def exclude(values, i):
    return values[:i] + values[i + 1:]


def part_two(data):
    reports = parse_data(data)
    report_candidates = (
        (exclude(r, i) for i in range(len(r)))
        for r in reports
    )
    return sum(
        any(map(is_safe, rc))
        for rc in report_candidates
    )


def main():
    data = get_data(day=2, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
