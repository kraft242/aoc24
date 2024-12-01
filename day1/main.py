from aocd import get_data
from collections import Counter


def parse_data(data):
    lhs, rhs = [], []
    for line in data.splitlines():
        parts = line.split()
        l, r = int(parts[0]), int(parts[1])
        lhs.append(l)
        rhs.append(r)
    return lhs, rhs


def part_one(data):
    lhs, rhs = parse_data(data)
    distances = [abs(l - r) for l, r in zip(sorted(lhs), sorted(rhs))]
    return sum(distances)


def part_two(data):
    lhs, rhs = parse_data(data)
    rhs_counts = Counter(rhs)
    similarity = [l * rhs_counts.get(l, 0) for l in sorted(lhs)]
    return sum(similarity)


def main():
    data = get_data(day=1, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
