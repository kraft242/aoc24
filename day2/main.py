from aocd import get_data
from itertools import pairwise


def parse_data(data):
    reports = []
    for line in data.splitlines():
        numbers = [int(n) for n in line.split()]
        reports.append(numbers)
    return reports


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def is_safe(report):
    diffs = [l - r for l, r in pairwise(report)]
    first_sign = sign(diffs[0])

    return all((
        all(sign(d) == first_sign for d in diffs),
        all(1 <= abs(d) <= 3 for d in diffs)
    ))


def part_one(data):
    reports = parse_data(data)
    return sum(is_safe(r) for r in reports)


def part_two(data):
    reports = parse_data(data)
    safe = []
    candidates = []
    for r in reports:
        if is_safe(r):
            safe.append(r)
        else:
            candidates.append(r)
    for c in candidates:
        excluded = [c[:i] + c[i + 1:] for i in range(len(c))]
        if any(is_safe(e) for e in excluded):
            safe.append(c)
    return len(safe)


def main():
    data = get_data(day=2, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()