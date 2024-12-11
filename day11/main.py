from aocd import get_data
from collections import defaultdict

FACTOR = 2024


def parse_data(data):
    return list(map(int, data.split()))


def has_even_digits(n):
    return len(str(n)) % 2 == 0


def blink(n):
    if n == 0:
        return [1]
    if has_even_digits(n):
        s = str(n)
        l = len(s)
        return [int(s[:l // 2]), int(s[l // 2:])]
    return [n * FACTOR]


def solve(data, steps):
    data = parse_data(data)
    counts = defaultdict(int)

    for n in data:
        counts[n] += 1

    for _ in range(steps):
        delta = defaultdict(int)

        for n, c in counts.items():
            delta[n] -= c
            for m in blink(n):
                delta[m] += c

        for k, v in delta.items():
            counts[k] += v

    return sum(counts.values())


def part_one(data):
    return solve(data, 25)


def part_two(data):
    return solve(data, 75)


def main():
    data = get_data(day=11, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
