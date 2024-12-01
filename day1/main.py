from aocd import get_data
from collections import Counter
from io import StringIO
import numpy as np


def parse_data(data):
    return np.loadtxt(StringIO(data), dtype=int).T


def part_one(data):
    lhs, rhs = parse_data(data)
    return np.sum(np.abs(np.sort(lhs) - np.sort(rhs)))


def part_two(data):
    lhs, rhs = parse_data(data)
    rhs_counts = Counter(rhs)
    return np.sum(
        lhs * np.array([rhs_counts.get(l, 0) for l in lhs])
    )


def main():
    data = get_data(day=1, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
