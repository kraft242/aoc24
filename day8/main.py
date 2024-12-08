from aocd import get_data
from collections import defaultdict
from itertools import combinations
import numpy as np


def rotate(fixed, p):
    """
    Revolve p one half-turn around fixed.
    """
    fx, fy = fixed
    px, py = p
    return (2 * fx - px, 2 * fy - py)


def debug_print(grid):
    for line in grid:
        for c in line:
            match c:
                case 0:
                    print(".", end="")
                case _:
                    print("#", end="")
        print("\n", end="")


def solve(data, part_two=False):
    antennas = defaultdict(list)
    lines = data.splitlines()
    nx, ny = len(lines[0]), len(lines)
    grid = np.zeros((ny, nx))

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != ".":
                antennas[c].append((x, y))

    stack = []

    for ls in antennas.values():
        pairs = combinations(ls, 2)
        for l, r in pairs:
            stack.append((l, rotate(l, r)))
            stack.append((r, rotate(r, l)))
            if part_two:
                stack.append((l, r))
                stack.append((r, l))

    def in_bounds(x, y):
        return 0 <= x < nx and 0 <= y < ny

    while stack:
        reference, antinode = stack.pop()

        x, y = antinode

        if not in_bounds(x, y):
            continue

        grid[y][x] += 1

        if part_two:
            stack.append((antinode, rotate(antinode, reference)))

    return np.count_nonzero(grid)


def part_one(data):
    return solve(data)


def part_two(data):
    return solve(data, part_two=True)


def main():
    data = get_data(day=8, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
