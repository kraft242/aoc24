from aocd import get_data
from time import perf_counter_ns
import numpy as np
from PIL import Image
import multiprocessing as mp
import re


def parse_line(line):
    number_pattern = r"[-\d]+"
    numbers = re.findall(number_pattern, line)
    px, py, vx, vy = map(int, numbers)
    return px, py, vx, vy


def get_grid_at(parsed, steps):
    width, height = 101, 103

    grid = np.zeros((height, width), dtype=int)

    xs = ((px + steps * vx) % width for px, _, vx, _ in parsed)
    ys = ((py + steps * vy) % height for _, py, _, vy in parsed)

    for x, y in zip(xs, ys):
        grid[y, x] += 1

    return grid


def get_safety_score(grid):
    height, width = grid.shape

    x_mid, y_mid = width // 2, height // 2

    q0 = grid[0: y_mid, 0: x_mid]
    q1 = grid[0: y_mid, x_mid + 1:]
    q2 = grid[y_mid + 1:, 0: x_mid]
    q3 = grid[y_mid + 1:, x_mid + 1:]

    quadrants = [q0, q1, q2, q3]

    return np.prod([np.sum(q) for q in quadrants])


def part_one(data):

    parsed = [parse_line(line) for line in data.split("\n")]

    grid = get_grid_at(parsed, steps=100)

    return get_safety_score(grid)


def write_array_to_image(array, filename):
    binary_image = np.where(array > 0, 255, 0).astype(np.uint8)

    image = Image.fromarray(binary_image, mode="L")

    image.save(filename)


def part_two(data):
    lo, hi = 0, 10000

    steps = list(range(lo, hi))

    parsed = [parse_line(line) for line in data.split("\n")]

    grid_args = [(parsed, step) for step in steps]

    nprocs = mp.cpu_count()

    with mp.Pool(processes=nprocs) as pool:
        grids = pool.starmap(get_grid_at, grid_args)
        safety_scores = pool.map(get_safety_score, grids)
        tuples = list(zip(safety_scores, steps, grids))
        image_args = [
            (grid, f"images/score{score}step{step:08d}.png") for score, step, grid in tuples
        ]
        pool.starmap(write_array_to_image, image_args)

    return 0


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
