from aocd import get_data
from math import pi, cos, sin
import numpy as np


class Guard:
    def __init__(self, grid, x, y):
        self.grid = grid
        shape = grid.shape
        self.x_min, self.x_max = 0, shape[0]
        self.y_min, self.y_max = 0, shape[1]
        self.x = x
        self.y = y
        self.angle = pi / 2
        self.path = np.zeros(shape)
        self.path[self.y][self.x] = 1

    def get_delta(self):
        return int(cos(self.angle)), int(sin(-self.angle))

    def in_range(self, new_x, new_y):
        return self.x_min <= new_x < self.x_max and self.y_min <= new_y < self.y_max

    def step(self):
        dx, dy = self.get_delta()

        new_x, new_y = self.x + dx, self.y + dy

        if not self.in_range(new_x, new_y):
            return False

        if self.grid[new_y][new_x]:
            self.angle = (self.angle - pi / 2) % (2 * pi)
        else:
            self.x = new_x
            self.y = new_y
            self.path[new_y][new_x] += 1

        return True


def get_initial_position(grid):
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "^":
                return (x, y)
    return (-1, -1)


def part_one(data):
    grid = [list(line) for line in data.splitlines()]
    obstacles = [[True if c == "#" else False for c in line] for line in grid]
    pos = get_initial_position(grid)
    grid = np.array(obstacles)
    guard = Guard(grid, *pos)
    loop = True
    while loop:
        loop = guard.step()
    return np.count_nonzero(guard.path)


def part_two(data):
    return 0


def main():
    data = get_data(day=6, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
