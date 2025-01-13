from aocd import get_data
from itertools import pairwise
from functools import lru_cache
import networkx as nx


coord_to_num = {
    (1, 0): 0,
    (2, 0): "A",
    (0, 1): 1,
    (1, 1): 2,
    (2, 1): 3,
    (0, 2): 4,
    (1, 2): 5,
    (2, 2): 6,
    (0, 3): 7,
    (1, 3): 8,
    (2, 3): 9,
}

num_to_coord = {v: k for k, v in coord_to_num.items()}

coord_to_button = {
    (0, 0): "<",
    (1, 0): "v",
    (2, 0): ">",
    (1, 1): "^",
    (2, 1): "A",
}
button_to_coord = {v: k for k, v in coord_to_button.items()}

char_to_delta = {
    "^": (0, 1),
    ">": (1, 0),
    "v": (0, -1),
    "<": (-1, 0),
    "A": (-1, -1),
}
delta_to_char = {v: k for k, v in char_to_delta.items()}

# Describes the best (shortest) path to get from the right key to the left key
possible_paths = {
    # ^
    ("^", "^"): [""],
    ("^", "A"): [">"],
    ("^", "v"): ["v"],
    ("^", ">"): [">v", "v>"],
    ("^", "<"): ["v<"],
    # A
    ("A", "^"): ["<"],
    ("A", "A"): [""],
    ("A", "v"): ["<v", "v<"],
    ("A", ">"): ["v"],
    ("A", "<"): ["v<<"],
    # >
    (">", "^"): ["^<", "<^"],
    (">", "A"): ["^"],
    (">", "v"): ["<"],
    (">", ">"): [""],
    (">", "<"): ["<<"],
    # v
    ("v", "^"): ["^"],
    ("v", "A"): [">^", "^>"],
    ("v", "v"): [""],
    ("v", ">"): [">"],
    ("v", "<"): ["<"],
    # <
    ("<", "^"): [">^"],
    ("<", "A"): [">>^"],
    ("<", "v"): [">"],
    ("<", ">"): [">>"],
    ("<", "<"): [""],
    # A
    ("A", "0"): ["<"],
    ("A", "1"): ["^<<"],
    ("A", "2"): ["^<", "<^"],
    ("A", "3"): ["^"],
    ("A", "4"): ["^^<<"],
    ("A", "5"): ["<^^", "^^<"],
    ("A", "6"): ["^^"],
    ("A", "7"): ["^^^<<"],
    ("A", "8"): ["<^^^", "^^^<"],
    ("A", "9"): ["^^^"],
    ("A", "A"): [""],
    # 0
    ("0", "0"): [""],
    ("0", "1"): ["^<"],
    ("0", "2"): ["^"],
    ("0", "3"): ["^>", ">^"],
    ("0", "4"): ["^^<"],
    ("0", "5"): ["^^"],
    ("0", "6"): [">^^", "^^>"],
    ("0", "7"): ["^^^<"],
    ("0", "8"): ["^^^"],
    ("0", "9"): ["^^^>", ">^^^"],
    ("0", "A"): [">"],
    # 1
    ("1", "0"): [">v"],
    ("1", "1"): [""],
    ("1", "2"): [">"],
    ("1", "3"): [">>"],
    ("1", "4"): ["^"],
    ("1", "5"): [">^", "^>"],
    ("1", "6"): [">>^", "^>>"],
    ("1", "7"): ["^^"],
    ("1", "8"): ["^^>", ">^^"],
    ("1", "9"): ["^^>>", ">>^^"],
    ("1", "A"): [">>v"],
    # 2
    ("2", "0"): ["v"],
    ("2", "1"): ["<"],
    ("2", "2"): [""],
    ("2", "3"): [">"],
    ("2", "4"): ["<^", "^<"],
    ("2", "5"): ["^"],
    ("2", "6"): [">^", "^>"],
    ("2", "7"): ["^^<", "<^^"],
    ("2", "8"): ["^^"],
    ("2", "9"): ["^^>", ">^^"],
    ("2", "A"): [">v", "v>"],
    # 3
    ("3", "0"): ["<v", "v<"],
    ("3", "1"): ["<<"],
    ("3", "2"): ["<"],
    ("3", "3"): [""],
    ("3", "4"): ["<<^", "^<<"],
    ("3", "5"): ["^<", "<^"],
    ("3", "6"): ["^"],
    ("3", "7"): ["^^<<", "<<^^"],
    ("3", "8"): ["^^<", "<^^"],
    ("3", "9"): ["^^"],
    ("3", "A"): ["v"],
    # 4
    ("4", "0"): [">vv"],
    ("4", "1"): ["v"],
    ("4", "2"): [">v", "v>"],
    ("4", "3"): [">>v", "v>>"],
    ("4", "4"): [""],
    ("4", "5"): [">"],
    ("4", "6"): [">>"],
    ("4", "7"): ["^"],
    ("4", "8"): ["^>", ">^"],
    ("4", "9"): ["^>>", ">>^"],
    ("4", "A"): [">>vv"],
    # 5
    ("5", "0"): ["vv"],
    ("5", "1"): ["<v", "v<"],
    ("5", "2"): ["v"],
    ("5", "3"): [">v", "v>"],
    ("5", "4"): ["<"],
    ("5", "5"): [""],
    ("5", "6"): [">"],
    ("5", "7"): ["^<", "<^"],
    ("5", "8"): ["^"],
    ("5", "9"): ["^>", ">^"],
    ("5", "A"): [">vv", "vv>"],
    # 6
    ("6", "0"): ["<vv", "vv<"],
    ("6", "1"): ["<<v", "v<<"],
    ("6", "2"): ["v<", "<v"],
    ("6", "3"): ["v"],
    ("6", "4"): ["<<"],
    ("6", "5"): ["<"],
    ("6", "6"): [""],
    ("6", "7"): ["^<<", "<<^"],
    ("6", "8"): ["^<", "<^"],
    ("6", "9"): ["^"],
    ("6", "A"): ["vv"],
    # 7
    ("7", "0"): [">vvv"],
    ("7", "1"): ["vv"],
    ("7", "2"): [">vv", "vv>"],
    ("7", "3"): [">>vv", "vv>>"],
    ("7", "4"): ["v"],
    ("7", "5"): [">v", "v>"],
    ("7", "6"): ["v>>", ">>v"],
    ("7", "7"): [""],
    ("7", "8"): [">"],
    ("7", "9"): [">>"],
    ("7", "A"): [">>vvv"],
    # 8
    ("8", "0"): ["vvv"],
    ("8", "1"): ["<vv", "vv<"],
    ("8", "2"): ["vv"],
    ("8", "3"): ["vv>", ">vv"],
    ("8", "4"): ["<v", "v<"],
    ("8", "5"): ["v"],
    ("8", "6"): ["v>", ">v"],
    ("8", "7"): ["<"],
    ("8", "8"): [""],
    ("8", "9"): [">"],
    ("8", "A"): [">vvv", "vvv>"],
    # 9
    ("9", "0"): ["<vvv", "vvv<"],
    ("9", "1"): ["<<vv", "vv<<"],
    ("9", "2"): ["<vv", "vv<"],
    ("9", "3"): ["vv"],
    ("9", "4"): ["<<v", "v<<"],
    ("9", "5"): ["v<", "<v"],
    ("9", "6"): ["v"],
    ("9", "7"): ["<<"],
    ("9", "8"): ["<"],
    ("9", "9"): [">"],
    ("9", "A"): ["vvv"],
}


def parse_data(data):
    return data.split("\n")


@lru_cache(maxsize=None)
def get_shortest_path(sequence, depth, max_depth):
    ss = ["A"]

    if depth > max_depth:
        return sequence

    for src, dst in pairwise(sequence):
        paths = possible_paths[(src, dst)]

        if len(paths) == 1:
            ss = [r + paths[0] + "A" for r in ss]
        else:
            ss = [r + p + "A" for r in ss for p in paths]

    lengths = [len(s) for s in ss]

    print(f"Depth: {depth}, Lengths: {lengths}")

    return min((get_shortest_path(s, depth + 1, max_depth) for s in ss), key=len)


def extract_digits(s):
    return int("".join(str(n) for n in s if n.isdigit()))


def part_one(data):
    data = parse_data(data)

    codes = ["A" + line for line in data]
    shortest_paths = [get_shortest_path(code, 1, 3) for code in codes]
    trimmed_paths = [path[1:] for path in shortest_paths]
    lengths = [len(path) for path in trimmed_paths]
    numeric = [extract_digits(code) for code in codes]
    complexities = [a * numeric for a, numeric in zip(lengths, numeric)]
    return sum(complexities)


def part_two(data):
    data = parse_data(data)

    codes = ["A" + line for line in data]
    shortest_paths = [get_shortest_path(code, 1, 3) for code in codes]
    trimmed_paths = [path[1:] for path in shortest_paths]
    lengths = [len(path) for path in trimmed_paths]
    numeric = [
        int("".join(str(n) for n in code if n.isdigit()))
        for code in codes
    ]
    complexities = [a * numeric for a, numeric in zip(lengths, numeric)]
    return sum(complexities)


def main():
    data = """029A
980A
179A
456A
379A"""
    data = get_data(day=21, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
