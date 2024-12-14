from aocd import get_data
from time import perf_counter_ns
import numpy as np
import re


def parse_line(line):
    number_pattern = r"[-\d]+"
    numbers = re.findall(number_pattern, line)
    px, py, vx, vy = map(int, numbers)
    return px, py, vx, vy


def part_one(data):
    width, height = 101, 103
    steps = 100
    grid = np.zeros((height, width), dtype=int)

    parsed = [parse_line(line) for line in data.split("\n")]

    xs = ((px + steps * vx) % width for px, _, vx, _ in parsed)
    ys = ((py + steps * vy) % height for _, py, _, vy in parsed)

    for x, y in zip(xs, ys):
        grid[y, x] += 1

    x_mid, y_mid = width // 2, height // 2

    q0 = grid[0: y_mid, 0: x_mid]
    q1 = grid[0: y_mid, x_mid + 1:]
    q2 = grid[y_mid + 1:, 0: x_mid]
    q3 = grid[y_mid + 1:, x_mid + 1:]

    quadrants = [q0, q1, q2, q3]

    return np.prod([np.sum(q) for q in quadrants])


def part_two(data):
    return 8


def main():
    data = get_data(day=14, year=2024)
#    data = """p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3"""
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
