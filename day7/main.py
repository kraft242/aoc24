from aocd import get_data
from math import log10 as log, floor
import multiprocessing as mp
from time import perf_counter


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

    length = len(values)

    stack = [(values[0], 1)]

    while stack:
        acc, depth = stack.pop()

        if acc > target:
            continue

        if depth == length:
            if acc == target:
                return True
            continue

        stack.extend(
            (op(acc, values[depth]), depth + 1)
            for op in ops
        )

    return False


def solve(data, part_two=False):
    parsed = [parse_line(line) for line in data.splitlines()]
    args = ((t, vs, part_two) for t, vs in parsed)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        possible = pool.starmap(is_possible, args)

    return sum(
        t * p for (t, _), p in zip(parsed, possible)
    )


def part_one(data):
    return solve(data)


def part_two(data):
    return solve(data, part_two=True)


def main():
    data = get_data(day=7, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
