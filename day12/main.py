from aocd import get_data
import networkx as nx
import numpy as np

DELTA = [
    (-1, 0),  # North
    (0, 1),   # East
    (1, 0),   # South
    (0, -1),  # West
]

MAX_NEIGHBORS = 4


def parse_data(data):
    return [list(row) for row in data.split("\n")]


def in_bounds(y, x, height, width):
    return 0 <= y < height and 0 <= x < width


def is_different(y, x, c, data):
    if not in_bounds(y, x, len(data), len(data[0])):
        return False
    return data[y][x] != c


def flood_fill(data, p, visited):
    y, x = p
    Q = [(y, x)]
    c = data[y][x]
    shape = set()
    height, width = len(data), len(data[0])
    while Q:
        y, x = Q.pop()
        if in_bounds(y, x, height, width) and not visited[y, x] and data[y][x] == c:
            visited[y, x] = True
            shape.add((y, x))
            Q.extend((y + dy, x + dx) for dy, dx in DELTA)
    return shape


def get_shapes(data):
    height, width = len(data), len(data[0])

    visited = np.zeros((height, width), dtype=np.bool)

    shapes = []
    for y in range(height):
        for x in range(width):
            if not visited[y, x]:
                shape = flood_fill(data, (y, x), visited)
                shapes.append(shape)

    return shapes


def get_area(shape):
    return len(shape)


def get_open_faces(shape, direction):
    dy, dx = direction
    return {(y, x) for y, x in shape if (y + dy, x + dx) not in shape}


def get_perimeter(shape):
    return sum(
        len(get_open_faces(shape, d))
        for d in DELTA
    )


def part_one(data):
    data = parse_data(data)

    shapes = get_shapes(data)

    return sum(get_area(s) * get_perimeter(s) for s in shapes)


def get_sides(G, shape, direction):
    open_faces = get_open_faces(shape, direction)

    sub = nx.induced_subgraph(G, open_faces)

    return list(nx.connected_components(sub))


def count_sides(G, shape):
    sides = (
        get_sides(G, shape, d)
        for d in DELTA
    )
    side_lens = map(len, sides)
    return sum(side_lens)


def build_graph(shapes):
    G = nx.Graph()

    for shape in shapes:
        G.add_nodes_from(shape)
        edges = (
            ((y, x), (y + dy, x + dx))
            for y, x in shape
            for dy, dx in DELTA
            if (y + dy, x + dx) in shape
        )
        G.add_edges_from(edges)

    return G


def part_two(data):
    data = parse_data(data)

    shapes = get_shapes(data)

    G = build_graph(shapes)

    return sum(get_area(s) * count_sides(G, s) for s in shapes)


def main():
    data = get_data(day=12, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
