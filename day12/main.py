from aocd import get_data
import numpy as np

delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_data(data):
    return [list(row) for row in data.split("\n")]


def in_bounds(y, x, height, width):
    return 0 <= y < height and 0 <= x < width


def on_bound(y, x, height, width):
    return (y == 0) + (y == height - 1) + (x == 0) + (x == width - 1)


def is_different(y, x, c, data):
    if not in_bounds(y, x, len(data), len(data[0])):
        return False
    return data[y][x] != c


def flood_fill(p, shape, data, visited):
    y, x = p
    Q = [(y, x)]
    c = data[y][x]
    height, width = len(data), len(data[0])
    while Q:
        y, x = Q.pop()
        if in_bounds(y, x, height, width) and not visited[y, x] and data[y][x] == c:
            visited[y, x] = True
            shape.add((y, x))
            Q.extend((y + dy, x + dx) for dy, dx in delta)


def get_shapes(data):
    height, width = len(data), len(data[0])

    visited = np.zeros((height, width), dtype=np.bool)

    shapes = []
    for y in range(height):
        for x in range(width):
            if visited[y, x]:
                continue
            shape = set()
            flood_fill((y, x), shape, data, visited)
            shapes.append(shape)

    return shapes


def get_perimeters(data, shapes):
    height, width = len(data), len(data[0])

    perimeters = np.zeros((height, width))

    for shape in shapes:
        for y, x in shape:
            perimeters[y, x] = sum(
                (y + dy, x + dx) not in shape
                for dy, dx in delta
            )

    return perimeters


def part_one(data):
    data = parse_data(data)

    shapes = get_shapes(data)

    areas = [len(shape) for shape in shapes]

    perimeters = get_perimeters(data, shapes)

    ps = [sum(perimeters[y, x] for y, x in shape) for shape in shapes]

    areas = [int(a) for a in areas]
    ps = [int(p) for p in ps]

    return sum(a * p for a, p in zip(areas, ps))


def part_two(data):
    return 8


def main():
    data = get_data(day=12, year=2024)
#    data = """RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE"""
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
