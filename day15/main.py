from aocd import get_data
import numpy as np


class Objects:
    EMPTY = 0
    WALL = 1
    ROBOT = 2
    BOX = 3


def parse_warehouse(raw, part_two=False):
    raw = raw.split("\n")
    raw = [list(row) for row in raw]
    ny, nx = len(raw), len(raw[0])
    if not part_two:
        warehouse = np.zeros((ny, nx), dtype=int)
        for y, row in enumerate(raw):
            for x, c in enumerate(row):
                match c:
                    case ".":
                        warehouse[y, x] = Objects.EMPTY
                    case "#":
                        warehouse[y, x] = Objects.WALL
                    case "O":
                        warehouse[y, x] = Objects.BOX
                    case "@":
                        warehouse[y, x] = Objects.ROBOT
    else:
        warehouse = np.zeros((ny, 2 * nx), dtype=int)
        for y, row in enumerate(raw):
            for x, c in enumerate(row):
                match c:
                    case ".":
                        warehouse[y, 2 * x] = Objects.EMPTY
                        warehouse[y, 2 * x + 1] = Objects.EMPTY
                    case "#":
                        warehouse[y, 2 * x] = Objects.WALL
                        warehouse[y, 2 * x + 1] = Objects.WALL
                    case "O":
                        warehouse[y, 2 * x] = Objects.BOX
                        warehouse[y, 2 * x + 1] = Objects.BOX
                    case "@":
                        warehouse[y, 2 * x] = Objects.ROBOT
                        warehouse[y, 2 * x + 1] = Objects.EMPTY
    return warehouse


def parse_data(data, part_two=False):
    warehouse, moves = data.split("\n\n")
    warehouse = parse_warehouse(warehouse, part_two)
    moves = list(m for mss in moves.split("\n") for m in mss)
    return warehouse, moves


def move_to_delta(m):
    match m:
        case ">":
            return (0, 1)
        case "<":
            return (0, -1)
        case "^":
            return (-1, 0)
        case "v":
            return (1, 0)
        case _:
            raise ValueError(f"Unknown move {m}")


def in_bounds(warehouse, pos):
    y, x = pos
    return 0 <= y < warehouse.shape[0] and 0 <= x < warehouse.shape[1]


def move(warehouse, pos, delta):
    y, x = pos
    dy, dx = delta
    ny, nx = y + dy, x + dx
    possible = (ny, nx)
    impossible = (y, x)
    if not in_bounds(warehouse, (ny, nx)):
        return impossible
    match warehouse[ny, nx]:
        case Objects.EMPTY:
            warehouse[ny, nx] = warehouse[y, x]
            warehouse[y, x] = Objects.EMPTY
            return possible
        case Objects.ROBOT:
            raise ValueError("Fish cannot move")
        case Objects.WALL:
            return impossible
        case Objects.BOX:
            if move(warehouse, (ny, nx), delta) == (ny + dy, nx + dx):
                warehouse[ny, nx] = warehouse[y, x]
                warehouse[y, x] = Objects.EMPTY
                return possible
            return impossible


def num_to_char(n, part_two=False, even=False):
    match n:
        case Objects.WALL:
            return "#"
        case Objects.EMPTY:
            return "."
        case Objects.BOX:
            if not part_two:
                return "O"
            elif even:
                return "["
            else:
                return "]"
        case Objects.ROBOT:
            if not part_two:
                return "@"
            elif even:
                return "@"
            else:
                return "."


def pretty_print(warehouse, part_two=False):
    if not part_two:
        for row in warehouse:
            print("".join(num_to_char(c) for c in row))
    else:
        for row in warehouse:
            print("".join(num_to_char(c, part_two, i % 2 == 0)
                  for i, c in enumerate(row)))


def part_one(data):
    warehouse, moves = parse_data(data)

    pos = None
    for y, row in enumerate(warehouse):
        for x, c in enumerate(row):
            if c == Objects.ROBOT:
                pos = (y, x)

    for m in moves:
        delta = move_to_delta(m)
        warehouse[pos] = Objects.EMPTY
        pos = move(warehouse, pos, delta)
        warehouse[pos] = Objects.ROBOT
        print(f"Move {m}")
        # pretty_print(warehouse)
        # print()

    boxes = np.where(warehouse == Objects.BOX)

    box_coords = list(zip(boxes[0], boxes[1]))

    return sum(100 * y + x for y, x in box_coords)


def part_two(data):

    warehouse, moves = parse_data(data, part_two=True)

    pos = None
    for y, row in enumerate(warehouse):
        for x, c in enumerate(row):
            if c == Objects.ROBOT:
                pos = (y, x)

    pretty_print(warehouse, part_two=True)

    return 8


def main():
    data = get_data(day=15, year=2024)
    data = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
