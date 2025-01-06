from aocd import get_data
import networkx as nx

WIDTH, HEIGHT = 71, 71
INVALID = -1


def parse_line(line):
    x, y = line.split(",")
    return int(x), int(y)


def parse_data(data):
    return [parse_line(line) for line in data.split("\n") if line]


def precompute_edges():
    delta = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    return [
        ((x, y), (x + dx, y + dy))
        for y in range(HEIGHT)
        for x in range(WIDTH)
        for dx, dy in delta
        if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT
    ]


def solve(obstacles, n, edges):
    obstacles = set(obstacles[:n])

    edges = {
        (src, dst)
        for src, dst in edges
        if src not in obstacles and dst not in obstacles
    }

    G = nx.Graph(edges)

    path = nx.shortest_path(G, source=(0, 0), target=(WIDTH - 1, HEIGHT - 1))

    return len(path) - 1


def part_one(data):
    return solve(parse_data(data), 1024, precompute_edges())


def get_first_blocking_byte(edges, obstacles):
    lo, hi = 1024, len(obstacles)
    while lo < hi:
        mid = (lo + hi) // 2
        try:
            solve(obstacles, mid, edges)
            lo = mid + 1
        except nx.NetworkXNoPath:
            hi = mid
    return lo - 1


def part_two(data):
    edges = precompute_edges()
    obstacles = parse_data(data)

    i = get_first_blocking_byte(edges, obstacles)

    x, y = obstacles[i]
    return f"{x},{y}"


def main():
    data = get_data(day=18, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
