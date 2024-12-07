from aocd import get_data
from math import log10 as log, floor


def parse_line(line):
    lhs, values = line.split(": ")
    values = tuple(int(v) for v in values.split())
    return int(lhs), values


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concat(a, b):
    return a * 10 ** (floor(log(b)) + 1) + b


def is_possible(target, values, part_two=False):
    ops = (add, mul, concat) if part_two else (add, mul)

    curr = {0}

    for v in values:
        curr = {
            op(c, v)
            for c in curr
            for op in ops
            if c <= target
        }

    return target in curr


def part_one(data):
    parsed = (parse_line(line) for line in data.splitlines())
    return sum(
        t * is_possible(t, values) for t, values in parsed
    )


def part_two(data):
    parsed = (parse_line(line) for line in data.splitlines())
    return sum(
        t * is_possible(t, values, part_two=True) for t, values in parsed
    )


def main():
    data = get_data(day=7, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
