from aocd import get_data
from operator import add, mul
from math import log10 as log


def parse_line(line):
    lhs, values = line.split(": ")
    values = tuple(int(v) for v in values.split())
    return int(lhs), values


def concat(a, b):
    b_digits = int(log(b))
    return a * 10 ** (b_digits + 1) + b


def is_possible(target, values, part_two=False):
    prev = {0}

    for v in values:
        curr = set()
        for p in prev:
            curr.add(add(p, v))
            curr.add(mul(p, v))
            if part_two:
                curr.add(concat(p, v))

        prev = curr

    return target in prev


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
