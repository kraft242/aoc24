from aocd import get_data
from time import perf_counter_ns
import numpy as np
from PIL import Image
import multiprocessing as mp
import re

WIDTH, HEIGHT = 101, 103


def parse_line(line):
    number_pattern = r"[-\d]+"
    numbers = re.findall(number_pattern, line)
    px, py, vx, vy = map(int, numbers)
    return px, py, vx, vy


def parse_data(data):
    return [parse_line(line) for line in data.splitlines()]


def get_coordinates_at(parsed, step):
    xs = [(px + step * vx) % WIDTH for px, _, vx, _ in parsed]
    ys = [(py + step * vy) % HEIGHT for _, py, _, vy in parsed]

    return xs, ys


def get_safety_score(xs, ys):
    x_mid, y_mid = WIDTH // 2, HEIGHT // 2
    q0 = sum(1 for x, y in zip(xs, ys) if x < x_mid and y < y_mid)
    q1 = sum(1 for x, y in zip(xs, ys) if x > x_mid and y < y_mid)
    q2 = sum(1 for x, y in zip(xs, ys) if x < x_mid and y > y_mid)
    q3 = sum(1 for x, y in zip(xs, ys) if x > x_mid and y > y_mid)
    return q0 * q1 * q2 * q3


def part_one(data):
    parsed = parse_data(data)

    xs, ys = get_coordinates_at(parsed, step=100)

    return get_safety_score(xs, ys)


def write_array_to_image(array, filename):
    binary_image = np.where(array > 0, 255, 0).astype(np.uint8)

    image = Image.fromarray(binary_image, mode="L")

    image.save(filename)


def part_two(data):
    lo, hi = 0, 10000

    steps = list(range(lo, hi))

    parsed = parse_data(data)

    grid_args = [(parsed, step) for step in steps]

    with mp.Pool(processes=mp.cpu_count()) as pool:
        coords = pool.starmap(get_coordinates_at, grid_args)
        safety_score_args = [(xs, ys) for xs, ys in coords]

        safety_scores = pool.starmap(
            get_safety_score, safety_score_args
        )

    tuples = zip(safety_scores, steps)

    def score(t):
        s, _ = t
        return s

    _, n = min(tuples, key=score)
    return n


def main():
    data = get_data(day=14, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
